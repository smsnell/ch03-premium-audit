#!/usr/bin/env python3
"""Deterministic allocation from evidence-backed normalized JSON; no source prose execution."""
import argparse
from datetime import date, timedelta, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import os

# Support both the CLI and file-based Skill/test loading.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reporting import render

CENT = Decimal('0.01')
ZERO = Decimal('0.00')


class InputError(ValueError):
    pass


def require(test, message):
    if not test:
        raise InputError(message)


def money(value):
    require(isinstance(value, str), 'Money must be a decimal string, never float/null')
    try:
        number = Decimal(value)
        require(number.is_finite() and number >= 0 and number == number.quantize(CENT),
                'Money must be finite, nonnegative and exact cents: ' + value)
        return number.quantize(CENT)
    except InvalidOperation as exc:
        raise InputError('Invalid money: ' + value) from exc


def fmt(value):
    return format(value, '.2f')


def day(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise InputError('Invalid ISO date: ' + str(value)) from exc


def roof_code(rows, start, end):
    dates = set()
    for row in rows:
        try:
            hours = Decimal(str(row['hours']))
        except (InvalidOperation, KeyError) as exc:
            raise InputError('Roofing hours required and numeric') from exc
        require(hours.is_finite() and hours >= 0, 'Invalid roofing hours')
        value = day(row['date'])
        if start <= value <= end and hours > 0:
            dates.add(value)
    return ('R-310' if len(dates) >= 15 else 'R-320'), len(dates)


def invoice_basis(amount):
    return (amount * Decimal('0.60')).quantize(CENT, rounding=ROUND_HALF_UP)


class Audit:
    def __init__(self, case, base=Path('.')):
        self.case = case
        self.base = Path(base)
        self.start, self.end = day(case['audit_start']), day(case['audit_end'])
        require(self.start <= self.end, 'Audit period reversed')
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', case['slug']), 'Invalid slug')
        require(bool(case['employer'].strip()), 'Employer required')
        self.sources = {}
        for source in case['sources']:
            sid = source['id']
            require(source.get('audience', 'employer') in ('employer', 'internal'), 'Invalid source audience')
            require(sid not in self.sources, 'Duplicate source id: ' + sid)
            require(source['url'] and source['retrieved_at'], 'Source URL/retrieval time required')
            try:
                datetime.fromisoformat(source['retrieved_at'].replace('Z', '+00:00'))
            except ValueError as exc:
                raise InputError('Invalid retrieval time') from exc
            path = self.base / source['path']
            require(path.is_file(), 'Missing source: ' + str(path))
            require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'],
                    'Source fingerprint mismatch: ' + sid)
            self.sources[sid] = dict(source)
        guide_id = case['guide_source']
        self.evidence([guide_id])
        guide = (self.base / self.sources[guide_id]['path']).read_text()
        self.codes = dict((code, paragraph) for paragraph, code in re.findall(
            r'\*\*(CG-\d+)\.\s+([A-Z]-\d{3})\s', guide))
        require(self.codes, 'No code-description paragraphs found in guide')
        self.rules = case['rule_refs']
        for rule in self.rules.values():
            self.evidence(rule['sources'])
            require(bool(rule['citation'].strip()), 'Rule citation required')
        self.entries, self.adjustments, self.issues, self.decisions = [], [], [], []
        self.people = {}
        self.person_codes = {}
        self.total_baseline = ZERO

    def evidence(self, refs):
        require(isinstance(refs, list) and refs, 'Nonempty evidence list required')
        require(all(ref in self.sources for ref in refs), 'Unknown evidence source')
        return list(dict.fromkeys(refs))

    def policy(self, key):
        require(key in self.rules, 'Missing rule provenance: ' + key)
        return self.rules[key]['sources']

    def code(self, value):
        require(value in self.codes, 'Unmapped code: ' + str(value))
        return value

    def issue(self, ident, subject, treatment, evidence, amount=None, alternative=None):
        require(not any(item['id'] == ident for item in self.issues), 'Duplicate issue: ' + ident)
        self.issues.append(dict(id=ident, subject=subject, treatment=treatment,
                                evidence=self.evidence(evidence), amount=amount,
                                alternative_amount=alternative, status='open', confirmations=[]))

    def add(self, subject, code, amount, evidence, reason):
        self.entries.append(dict(subject=subject, code=self.code(code), amount=fmt(amount),
                                 evidence=self.evidence(evidence), reason=reason))

    def adjust(self, subject, before_code, before, after, evidence, reason):
        """after is code->Decimal; preserve reclassifications even when net is zero."""
        before_map = ({before_code or 'code not specified in application': fmt(before)}
                      if before or before_code else {})
        after_map = {key: fmt(value) for key, value in after.items() if value}
        if before_map != after_map:
            self.adjustments.append(dict(id='adjustment-' + str(len(self.adjustments) + 1),
                subject=subject, before=before_map, after=after_map,
                kind='baseline_allocation' if before and before_code is None else 'adjustment',
                net=fmt(sum(after.values(), ZERO) - before),
                evidence=self.evidence(evidence), reason=reason))

    def run(self):
        c = self.case
        for item in c.get('open_issues', []):
            self.issue(item['id'], item['subject'], item['treatment'], item['evidence'],
                       None if item.get('amount') is None else fmt(money(item['amount'])),
                       None if item.get('alternative_amount') is None else fmt(money(item['alternative_amount'])))
        reported = {self.code(code): money(amount) for code, amount in c['reported'].items()}
        require(c['people'], 'Payroll people required')
        for p in c['people']:
            require(p['id'] not in self.people, 'Duplicate person id')
            self.evidence(p['evidence'])
            require(bool(p['name'].strip()), 'Person name required')
            require(p['role'] in ('direct', 'roofing', 'office', 'dispatcher', 'owner', 'catering'),
                    'Unmapped employee role: ' + str(p['role']))
            if p.get('code') is None:
                require(p['role'] == 'owner' and p.get('off_register') is True,
                        'Missing work code requires an off-register owner with unknown duties')
            else:
                self.code(p['code'])
            p = dict(p)
            p['_pay'] = None if p.get('pay') is None else money(p['pay'])
            require(p['_pay'] is not None or (p['role'] == 'owner' and p.get('off_register') is True),
                    'Missing employee amount')
            p['_before'] = None
            if p.get('reported_code') is not None:
                p['_before'] = self.code(p['reported_code'])
                p['evidence'] = p['evidence'] + self.evidence(p.get('reported_code_evidence'))
            if p.get('exception_issue'):
                require(any(i['id'] == p['exception_issue'] for i in self.issues),
                        'Exception requires explicit open issue')
            self.total_baseline += p['_pay'] or ZERO
            self.people[p['id']] = p
        reported_total = sum(reported.values(), ZERO)
        if reported_total != self.total_baseline:
            self.issue('application-register-total', c['employer'],
                       'Application total ' + fmt(reported_total) + ' differs from known register total ' +
                       fmt(self.total_baseline) + '; use evidence-backed register provisionally and obtain reconciliation.',
                       list(self.sources), fmt(self.total_baseline), fmt(reported_total))
        # Validate all normalized record references, including records outside the period.
        for name in ('signin', 'roofing', 'route_weeks', 'allowances'):
            for row in c.get(name, []):
                require(row['person'] in self.people, 'Unknown record employee: ' + row['person'])
                self.evidence(row['evidence'])
        for name in ('signin', 'roofing'):
            for row in c.get(name, []):
                day(row['date'])
        pending = []
        for p in self.people.values():
            refs = p['evidence']
            if p.get('exception_issue'):
                refs = refs + next(i['evidence'] for i in self.issues if i['id'] == p['exception_issue'])
            pay, code, reason = p['_pay'], p['code'], 'Explicit evidence-backed work mapping'
            role = p['role']
            if role == 'office' and not p.get('contractor'):
                visits = {day(r['date']) for r in c.get('signin', []) if r['person'] == p['id']
                          and self.start <= day(r['date']) <= self.end}
                require(len(visits) < 5 or p.get('exception_issue'),
                        'Noncontractor office employee with five or more visits requires explicit proposed exception')
            if role == 'office' and p.get('contractor'):
                require('signin' in c, 'Contractor office sign-in records required')
                refs = refs + self.policy('office') + self.policy('governing')
                rows = [r for r in c['signin'] if r['person'] == p['id']]
                refs += [ref for r in rows for ref in r['evidence']]
                days = {day(r['date']) for r in rows if self.start <= day(r['date']) <= self.end}
                require(code == 'C-110', 'Contractor office base code must be C-110')
                pending.append((p, len(days), refs))
                continue
            if role == 'roofing':
                require('roofing' in c, 'Roofing records required')
                rows = [r for r in c['roofing'] if r['person'] == p['id']]
                if not rows:
                    refs = refs + self.evidence(p.get('roofing_evidence'))
                refs = refs + self.policy('roofing') + self.policy('governing')
                refs += [ref for r in rows for ref in r['evidence']]
                code, count = roof_code(rows, self.start, self.end)
                reason = str(count) + ' unique in-period positive roof days; whole-person allocation'
            elif role == 'dispatcher':
                self.dispatcher(p)
                continue
            elif role == 'owner':
                refs = refs + self.policy('owner')
                require(type(p.get('election_valid')) is bool, 'Owner election_valid must be explicit boolean')
                if p['election_valid']:
                    self.evidence(p.get('election_evidence'))
                    refs += p['election_evidence']
                    require(day(p['election_start']) <= self.start and day(p['election_end']) >= self.end,
                            'Owner election must cover audit period')
                    pay = ZERO
                    reason = 'Valid exclusion election; proposed election-first precedence (P4)'
                    self.issue(p['id'] + '-owner-precedence', p['name'], reason, refs,
                               '0.00', None)
                elif p.get('off_register'):
                    self.issue(p['id'] + '-owner-election', p['name'],
                               'P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero.', refs)
                    require(pay is None, 'Off-register missing-election owner amount must remain null')
                    self.decisions.append(dict(subject=p['name'], reason='Unquantified completeness gap', evidence=refs))
                    continue
                else:
                    require(type(p.get('field_work')) is bool, 'Included owner field_work required')
                    if p['field_work']:
                        require(code != 'C-110', 'Field-working owner requires a supported trade code')
                        pay = Decimal('63700.00')
                        reason = 'Included working owner with field duties: fixed period basis'
                    else:
                        reason = 'Included non-field owner: evidence-backed actual remuneration'
            elif role == 'catering':
                code, more, reason = self.catering()
                refs = refs + more
            if p.get('exception_issue'):
                require(any(i['id'] == p['exception_issue'] for i in self.issues), 'Exception requires explicit open issue')
                reason += '; provisional exception ' + p['exception_issue']
            self.person_codes[p['id']] = {code} if pay > 0 else set()
            if pay > 0:
                self.add(p['name'], code, pay, refs, reason)
            self.adjust(p['name'], p['_before'], p['_pay'] or ZERO, {code: pay}, refs, reason)
            self.decisions.append(dict(subject=p['name'], reason=reason, evidence=refs))
        # Supported trade additions precede governing-code comparison and office transfers.
        self.subcontractors()
        self.allowances()
        direct = {}
        for entry in self.entries:
            if entry['code'] != 'C-110':
                direct[entry['code']] = direct.get(entry['code'], ZERO) + money(entry['amount'])
        positive = {key: value for key, value in direct.items() if value > 0}
        winners = [key for key, value in positive.items() if value == max(positive.values())] if positive else []
        governing = winners[0] if len(winners) == 1 else None
        for p, count, refs in pending:
            code = 'C-110'
            reason = str(count) + ' unique in-period site days'
            if count >= 5:
                if governing:
                    code = governing
                    reason += '; entire pay to governing field code before office transfers (P2)'
                else:
                    require(p.get('exception_issue'),
                            'No unique governing field code; explicit proposed fallback issue required')
                    reason += '; unresolved governing destination; provisional C-110'
            self.add(p['name'], code, p['_pay'], refs, reason)
            self.adjust(p['name'], p['_before'], p['_pay'], {code: p['_pay']}, refs, reason)
            self.decisions.append(dict(subject=p['name'], reason=reason, evidence=refs))
        for confirmation in c.get('confirmations', []):
            require(confirmation.get('case_slug') == c['slug'], 'Confirmation case_slug must match this employer')
            require(confirmation.get('kind') in ('employer_fact', 'internal_decision'),
                    'Confirmation kind must distinguish employer_fact from internal_decision')
            matches = [i for i in self.issues if i['id'] == confirmation['issue_id']]
            require(len(matches) == 1, 'Confirmation must identify exactly one existing issue')
            self.evidence(confirmation['evidence'])
            require(all(confirmation.get(key) for key in ('by', 'at', 'scope')), 'Confirmation details required')
            day(confirmation['at'][:10])
            matches[0]['confirmations'].append(dict(confirmation))
            matches[0]['status'] = 'confirmation_recorded'
        totals = {}
        for entry in self.entries:
            totals[entry['code']] = totals.get(entry['code'], ZERO) + money(entry['amount'])
        net = sum((Decimal(a['net']) for a in self.adjustments), ZERO)
        require(self.total_baseline + net == sum(totals.values(), ZERO), 'Payroll/adjustment conservation failure')
        require(any(value > 0 for value in totals.values()), 'No supported positive payroll; incomplete allocation')
        for decision in self.decisions:
            decision['evidence'] = self.evidence(decision['evidence'])
        notes = []
        for note in c.get('case_notes', []):
            require(all(isinstance(note.get(key), str) and note[key].strip()
                        for key in ('subject', 'detail', 'question')), 'Case evidence requires subject, detail and question')
            notes.append(dict(subject=note['subject'], detail=note['detail'],
                              question=note['question'], evidence=self.evidence(note['evidence'])))
            if 'audience' in note:
                require(note['audience'] in ('employer', 'internal'), 'Invalid note audience')
                notes[-1]['audience'] = note['audience']
        different = {k: v for k, v in totals.items() if v} != {k: v for k, v in reported.items() if v}
        return dict(slug=c['slug'], employer=c['employer'], audit_start=str(self.start), audit_end=str(self.end),
                    status='draft; final sign-off not established',
                    split_decision=('provisionally reject' if different else 'provisionally accept'),
                    reported={k: fmt(v) for k, v in reported.items()},
                    totals={k: fmt(v) for k, v in sorted(totals.items()) if v > 0},
                    rationale_refs=self.codes, baseline=fmt(self.total_baseline), net_adjustment=fmt(net),
                    governing_before_office={k: fmt(v) for k, v in sorted(direct.items())},
                    entries=self.entries, adjustments=self.adjustments, decisions=self.decisions,
                    issues=self.issues, case_notes=notes, rule_refs=self.rules, sources=list(self.sources.values()))

    def dispatcher(self, p):
        require('route_weeks' in self.case, 'Dispatcher weekly payroll/route records required')
        require(p['code'] == 'C-110', 'Dispatcher base code must be C-110')
        rows = [r for r in self.case['route_weeks'] if r['person'] == p['id']]
        require(rows, 'Weekly records missing for ' + p['name'])
        weeks, after, refs = set(), {}, list(p['evidence']) + self.policy('dispatcher')
        total = ZERO
        for row in rows:
            start = day(row['start'])
            require(start.weekday() == 0 and start not in weeks, 'Unique Monday week starts required')
            require(self.start <= start and start + timedelta(days=6) <= self.end,
                    'Weekly period must fall wholly within audit; partial weeks need agent resolution')
            weeks.add(start)
            dates = {day(d) for d in row['ride_dates']}
            require(all(start <= d <= start + timedelta(days=6) for d in dates), 'Route date outside pay week')
            code = 'T-610' if len(dates) >= 2 else 'C-110'
            pay = money(row['pay'])
            total += pay
            after[code] = after.get(code, ZERO) + pay
            refs += row['evidence']
            self.add(p['name'] + ' week ' + str(start), code, pay, row['evidence'] + self.policy('dispatcher'),
                     str(len(dates)) + ' unique ride days; whole week; independent of site sign-in')
        self.person_codes[p['id']] = {key for key, value in after.items() if value > 0}
        require(total == p['_pay'], 'Weekly payroll does not reconcile to employee register: ' + p['name'])
        self.adjust(p['name'], p['_before'], p['_pay'], after, refs, 'Whole-week route-day rule')
        self.decisions.append(dict(subject=p['name'], reason='Weekly payroll reconciled; route days control', evidence=refs))

    def subcontractors(self):
        invoices = self.case.get('sub_invoices', [])
        if not invoices:
            return
        require('certificates' in self.case, 'Certificate records/search result required')
        rule = self.policy('subcontractors')
        certs = self.case['certificates']
        for cert in certs:
            self.evidence(cert['evidence'])
            require(day(cert['start']) <= day(cert['end']), 'Certificate period reversed')
        ids = set()
        for row in invoices:
            require(row['id'] not in ids, 'Duplicate invoice id')
            ids.add(row['id'])
            require(self.start <= day(row['date']) <= self.end,
                    'Invoice outside audit period; resolve normalization before allocation')
            self.code(row['code'])
            refs = self.evidence(row['evidence']) + rule
            amount = money(row['amount'])
            covered = False
            for cert in certs:
                alias = (cert['name'] != row['name'] and cert.get('alias_for') == row['name']
                         and cert.get('alias_approved') is True)
                if alias:
                    self.evidence(cert.get('alias_evidence'))
                    refs += cert['alias_evidence']
                if cert['name'] == row['name'] or alias:
                    refs += cert['evidence']
                    if day(cert['start']) <= self.start and day(cert['end']) >= self.end:
                        covered = True
            addition = ZERO if covered else invoice_basis(amount)
            reason = ('Verified matching full-period certificate; no addition' if covered else
                      'No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7)')
            subject = row['name'] + ' invoice ' + row['id']
            if addition:
                self.add(subject, row['code'], addition, refs, reason)
                self.adjust(subject, None, ZERO, {row['code']: addition}, refs, reason)
                self.issue(row['id'] + '-coverage', subject, 'Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence.', refs, fmt(addition), '0.00')
            self.decisions.append(dict(subject=subject, reason=reason, evidence=refs))

    def allowances(self):
        ids = set()
        for row in self.case.get('allowances', []):
            require(row['id'] not in ids, 'Duplicate allowance id')
            ids.add(row['id'])
            p = self.people[row['person']]
            refs = row['evidence'] + p['evidence'] + self.policy('allowance')
            amount = money(row['amount'])
            days = row['days']
            require(type(days) is int and days >= 0, 'Allowance days must be nonnegative integer')
            require(type(row['documented_reimbursement']) is bool, 'Reimbursement basis must be explicit')
            allocated = self.person_codes.get(p['id'], set())
            if row.get('code') is not None:
                code = self.code(row['code'])
                refs += self.evidence(row.get('allocation_evidence'))
            else:
                require(len(allocated) == 1, 'Allowance allocation needs a unique calculated class or explicit allocation evidence')
                code = self.code(next(iter(allocated)))
            if row['documented_reimbursement']:
                refs += self.evidence(row.get('reimbursement_evidence'))
                excess = ZERO
                reason = 'Documented expense reimbursement excluded under CG-03'
            else:
                excess = max(ZERO, amount - Decimal(47) * days)
                reason = '$47 per recorded out-of-town day; only excess included'
                if days == 0 and amount:
                    reason = 'P5: zero-day payment provisionally included absent documented expense basis'
                    self.issue(row['id'] + '-zero-days', p['name'] + ' payment ' + row['id'],
                               'Obtain purpose, expense log and corrected travel days; zero-day treatment is proposed.', refs, fmt(excess), '0.00')
            subject = p['name'] + ' payment ' + row['id']
            if excess:
                self.add(subject, code, excess, refs, reason)
                self.adjust(subject, None, ZERO, {code: excess}, refs, reason)
            self.decisions.append(dict(subject=subject, reason=reason, evidence=refs))

    def catering(self):
        require('receipts' in self.case, 'Catering receipts required')
        r = self.case['receipts']
        refs = self.evidence(r['evidence']) + self.policy('catering')
        gross, catering = money(r['gross']), money(r['catering'])
        require(gross > 0 and catering <= gross, 'Invalid receipts totals')
        rs, re_ = day(r['start']), day(r['end'])
        require(rs <= re_, 'Receipts period reversed')
        if (rs, re_) != (self.start, self.end) and not any(i['id'] == 'receipts-period' for i in self.issues):
            self.issue('receipts-period', 'Gross receipts ' + str(rs) + ' to ' + str(re_),
                       'P6: supplied-period proxy only. Obtain audit-period summary or boundary transactions; no daily proration.', refs)
        qualifies = catering * 100 >= gross * 40
        return ('F-720' if qualifies else 'F-710'), refs, (
            'Catering receipts ' + fmt(catering) + ' / ' + fmt(gross) +
            (' at/above' if qualifies else ' below') + ' 40%; threshold applies to catering crew, no proportional wage split')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', default=[], help='Normalized case JSON; repeatable')
    parser.add_argument('--bundle', help='JSON list of cases, or {"cases": [...]}')
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args(argv)
    try:
        output = Path(args.output_dir)
        require(not output.exists(), 'Output directory already exists; choose a new run directory')
        inputs = []
        for filename in args.case:
            path = Path(filename)
            inputs.append((json.loads(path.read_text()), path.parent))
        if args.bundle:
            path = Path(args.bundle)
            bundle = json.loads(path.read_text())
            cases = bundle['cases'] if isinstance(bundle, dict) else bundle
            require(isinstance(cases, list), 'Bundle cases must be a list')
            inputs.extend((case, path.parent) for case in cases)
        require(inputs, 'At least one --case or --bundle required')
        ledgers = [Audit(case, base).run() for case, base in inputs]
        require(len({l['slug'] for l in ledgers}) == len(ledgers), 'Duplicate employer slug')
        files = render(ledgers)
        # All cases validate before writing; publish the complete new directory at once.
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.audit-stage-', dir=output.parent) as staging:
            stage = Path(staging) / 'package'
            stage.mkdir()
            for name, content in files.items():
                dest = stage / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content)
            require(not output.exists(), 'Output directory appeared during run; refusing replacement')
            os.rename(stage, output)
        print('Draft package written for ' + str(len(ledgers)) + ' case(s): ' + str(output))
        return 0
    except (InputError, KeyError, TypeError, ValueError, OSError) as exc:
        print('INCOMPLETE: ' + str(exc) + '. Existing outputs were not intentionally deleted; no audit approval.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
