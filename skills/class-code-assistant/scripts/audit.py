#!/usr/bin/env python3
"""Deterministic allocation from evidence-backed normalized JSON; no source prose execution."""
import argparse
from collections import Counter, defaultdict
import csv
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
# Contractor field trades described by the company guide; business evidence must
# still establish which of these the employer actually performs.
FIELD_TRADE_CODES = {'R-310', 'R-320', 'L-620', 'H-420', 'E-510'}


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
        self.guide_paragraphs = set(re.findall(r'\*\*(CG-\d+)\.', guide))
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

    def csv_records(self, check):
        """Read the independently captured source, never an inventory of normalized rows."""
        self.evidence([check['source']])
        source = self.sources[check['source']]
        with (self.base / source['path']).open(newline='', encoding='utf-8-sig') as stream:
            reader = csv.DictReader(stream)
            columns = reader.fieldnames
            require(columns and len(set(columns)) == len(columns), 'Missing/duplicate CSV headers')
            require(set(check['columns'].values()) <= set(columns), 'Missing reconciliation CSV columns')
            if check.get('work_column'):
                require(check['work_column'] in columns, 'Missing roofing work column')
            rows = list(reader)
        require(all(None not in row and all(v is not None for v in row.values()) for row in rows),
                'Malformed reconciliation CSV: ' + check['source'])
        if 'data_rows' in source:
            require(len(rows) == source['data_rows'], 'Captured CSV row count mismatch: ' + check['source'])
        return rows

    def check_completeness(self):
        required = dict(people=('id', 'name', 'pay'), signin=('person', 'date'),
                        roofing=('person', 'date', 'hours'), route_weeks=('person', 'start', 'pay'),
                        allowances=('person', 'amount', 'days'), sub_invoices=('id', 'name', 'date', 'amount'),
                        certificates=('name', 'start', 'end'))
        c = self.case
        controls = c.get('completeness')
        require(isinstance(controls, dict), 'Source-backed completeness declarations required')
        for name in required:
            require(name in c and isinstance(c[name], list), 'Explicit record array required: ' + name)
        people = {p['id']: p for p in c['people']}
        dispatchers = {pid for pid, p in people.items() if p['role'] == 'dispatcher'}
        off_register = {pid for pid, p in people.items() if p.get('off_register') is True}
        for name, fields in required.items():
            control = controls.get(name, {})
            require(isinstance(control, dict), 'Invalid completeness declaration: ' + name)
            status = control.get('status')
            if status in ('not_applicable', 'unavailable'):
                self.evidence(control.get('evidence'))
                require(not c[name], 'Empty-evidence declaration conflicts with records: ' + name)
                require(status != 'unavailable' or name == 'certificates',
                        'Unavailable mandatory records: ' + name)
                require(name != 'people' and not (name == 'route_weeks' and dispatchers),
                        'Required records cannot be not applicable: ' + name)
                continue
            require(status == 'complete', 'Explicit completeness status required: ' + name)
            checks = control.get('checks')
            require(isinstance(checks, list) and checks, 'Source CSV reconciliation required: ' + name)
            require(all(isinstance(check, dict) and isinstance(check.get('columns'), dict) for check in checks),
                    'Invalid source reconciliation mapping: ' + name)
            keys = tuple(sorted(checks[0]['columns']))
            require(set(fields) <= set(keys), 'Missing reconciliation fields: ' + name)
            allowed = set(fields) | ({'id', 'date'} if name == 'allowances' else set())
            require(set(keys) <= allowed, 'Unsupported reconciliation fields: ' + name)
            if name == 'allowances' and any(r.get('date') for r in c[name]):
                require('date' in keys, 'Dated allowances require source date reconciliation')

            def values(row):
                return tuple('' if row.get(k) is None else str(row[k]) for k in keys)

            expected = Counter()
            seen_sources = set()
            for check in checks:
                require(tuple(sorted(check['columns'])) == keys, 'Inconsistent reconciliation mappings: ' + name)
                require(check['source'] not in seen_sources, 'Duplicate reconciliation source: ' + name)
                seen_sources.add(check['source'])
                for raw in self.csv_records(check):
                    row = {key: raw[column] for key, column in check['columns'].items()}
                    if name == 'people' and row['id'] in off_register and row['pay'] == '':
                        continue
                    if name == 'signin' and row['person'] == '':
                        continue  # Nonemployee visitors remain in the captured record.
                    if name == 'roofing' and check.get('work_column') and raw[check['work_column']] != check.get('roof_value', 'roofing'):
                        continue
                    if name == 'route_weeks' and row['person'] not in dispatchers:
                        require(row['person'] in people, 'Unknown employee in weekly source')
                        continue
                    if name == 'allowances' and money(row['amount']) == ZERO:
                        continue
                    expected[values(row)] += 1
            normalized = [r for r in c[name] if not (name == 'people' and r['id'] in off_register)]
            require(all(all(k in r for k in fields) for r in normalized), 'Missing normalized fields: ' + name)
            actual = Counter(values(r) for r in normalized)
            require(expected == actual,
                    'Source reconciliation failed for ' + name + ': missing ' + str(list((expected - actual).elements())[:5]) +
                    '; extra/changed ' + str(list((actual - expected).elements())[:5]))
        if 'receipts' in c or any(p['role'] == 'catering' for p in people.values()):
            control = controls.get('receipts', {})
            require(control.get('status') == 'complete' and control.get('checks'),
                    'Source receipts reconciliation required')
            gross, catering, seen = ZERO, ZERO, set()
            for check in control['checks']:
                mapping = check['columns']
                require(set(mapping) in ({'gross', 'catering'}, {'dine_in', 'catering'}),
                        'Receipts require gross/catering or dine_in/catering columns')
                require(check['source'] not in seen, 'Duplicate receipts reconciliation source')
                seen.add(check['source'])
                for row in self.csv_records(check):
                    offsite = money(row[mapping['catering']])
                    amount = money(row[mapping['gross']]) if 'gross' in mapping else money(row[mapping['dine_in']]) + offsite
                    require(offsite <= amount, 'Invalid source receipts totals')
                    gross += amount
                    catering += offsite
            require(gross == money(c['receipts']['gross']) and catering == money(c['receipts']['catering']),
                    'Source reconciliation failed for receipts totals')
        if dispatchers:
            check = controls['route_weeks'].get('route_log')
            require(isinstance(check, dict) and set(check.get('columns', {})) == {'person', 'date'},
                    'Independent route-log reconciliation required')
            rides = defaultdict(set)
            for raw in self.csv_records(check):
                pid, when = (raw[check['columns'][k]] for k in ('person', 'date'))
                if pid:
                    require(pid in people, 'Unknown route-log rider')
                    if pid in dispatchers:
                        rides[pid].add(day(when))
            matched = defaultdict(set)
            for week in c['route_weeks']:
                start = day(week['start'])
                expected = {d for d in rides[week['person']] if start <= d <= start + timedelta(days=6)}
                require(expected == {day(d) for d in week['ride_dates']}, 'Route dates do not match captured log')
                matched[week['person']].update(expected)
            require(all(dates == matched[pid] for pid, dates in rides.items()), 'Route rides lack a matching pay week')

    def run(self):
        c = self.case
        self.check_completeness()
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
            require(p['role'] in ('direct', 'roofing', 'office', 'dispatcher', 'owner', 'catering', 'split'),
                    'Unmapped employee role: ' + str(p['role']))
            require('allocations' not in p or p['role'] == 'split',
                    'CG-07 allocations cannot override a specific house-rule role')
            if p.get('code') is None:
                require(p['role'] == 'split' or (p['role'] == 'owner' and p.get('off_register') is True),
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
        self.split_rows = self.read_split_records()
        pending = []
        for p in self.people.values():
            refs = p['evidence']
            if p.get('exception_issue'):
                refs = refs + next(i['evidence'] for i in self.issues if i['id'] == p['exception_issue'])
            pay, code, reason = p['_pay'], p['code'], 'Explicit evidence-backed work mapping'
            role = p['role']
            if role == 'split':
                self.split_payroll(p)
                continue
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
                status = p.get('election_status')
                require(status in ('unverified', 'included', 'excluded'), 'Explicit owner election_status required')
                if 'election_valid' in p:
                    require(type(p['election_valid']) is bool and p['election_valid'] == (status == 'excluded'),
                            'Contradictory owner election evidence')
                if status == 'excluded':
                    self.evidence(p.get('election_evidence'))
                    refs += p['election_evidence']
                    require(day(p['election_start']) <= self.start and day(p['election_end']) >= self.end,
                            'Owner election must cover audit period')
                    pay = ZERO
                    reason = 'Valid exclusion election; proposed election-first precedence (P4)'
                    self.issue(p['id'] + '-owner-precedence', p['name'], reason, refs,
                               '0.00', None)
                elif status == 'unverified':
                    self.issue(p['id'] + '-owner-election', p['name'],
                               'P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero.', refs)
                    require(p.get('off_register') is True and pay is None,
                            'Unverified owner requires explicit unresolved off-register treatment; known register pay needs reviewed resolution')
                    self.decisions.append(dict(subject=p['name'], reason='Unquantified completeness gap', evidence=refs))
                    continue
                else:
                    refs += self.evidence(p.get('inclusion_evidence'))
                    require(type(p.get('field_work')) is bool, 'Included owner field_work required')
                    if p['field_work']:
                        require(code is not None and code != 'C-110', 'Field-working owner requires a supported trade code')
                        pay = Decimal('63700.00')
                        reason = 'Included working owner with field duties: fixed period basis'
                    else:
                        require(pay is not None, 'Included non-field owner remuneration is unknown; resolve before allocation')
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
        eligible = None
        eligibility_refs = []
        if any(count >= 5 for _, count, _ in pending):
            eligible = c.get('governing_eligibility')
            require(isinstance(eligible, dict), 'Reviewed governing field-code eligibility required')
            for code, support in eligible.items():
                self.code(code)
                require(code in FIELD_TRADE_CODES, 'Code is not a supported governing field trade')
                require(isinstance(support.get('reason'), str) and support['reason'].strip(),
                        'Field-code eligibility requires a reviewed business/guide explanation')
                refs = self.evidence(support.get('evidence'))
                require(c['guide_source'] in refs and any(ref != c['guide_source'] for ref in refs),
                        'Field eligibility requires guide and business evidence')
                eligibility_refs += refs
            observed_field_codes = {entry['code'] for entry in self.entries} & FIELD_TRADE_CODES
            require(observed_field_codes <= set(eligible),
                    'Governing eligibility omits an allocated field trade; review all field codes')
        direct = {}
        for entry in self.entries:
            if entry['code'] != 'C-110' and (eligible is None or entry['code'] in eligible):
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
                    refs = refs + eligibility_refs
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
            if 'factual_question' in note:
                require(isinstance(note['factual_question'], str) and note['factual_question'].strip(),
                        'Reviewed factual question must be nonempty text')
                notes[-1]['factual_question'] = note['factual_question']
        different = {k: v for k, v in totals.items() if v} != {k: v for k, v in reported.items() if v}
        return dict(slug=c['slug'], employer=c['employer'], audit_start=str(self.start), audit_end=str(self.end),
                    status='draft; final sign-off not established',
                    split_decision=('provisionally reject' if different else 'provisionally accept'),
                    reported={k: fmt(v) for k, v in reported.items()},
                    totals={k: fmt(v) for k, v in sorted(totals.items()) if v > 0},
                    rationale_refs=self.codes, baseline=fmt(self.total_baseline), net_adjustment=fmt(net),
                    governing_before_office={k: fmt(v) for k, v in sorted(direct.items())},
                    entries=self.entries, adjustments=self.adjustments, decisions=self.decisions,
                    issues=self.issues, case_notes=notes, rule_refs=self.rules, sources=list(self.sources.values()),
                    input_controls=dict(completeness=c['completeness'],
                        owners=[{k: p[k] for k in ('id', 'pay', 'off_register', 'field_work', 'election_status',
                                                  'inclusion_evidence', 'election_evidence') if k in p}
                                for p in c['people'] if p['role'] == 'owner'],
                        allowance_inputs=c['allowances'],
                        governing_eligibility=c.get('governing_eligibility'),
                        time_records=c.get('time_records'),
                        split_inputs=[{k: p[k] for k in ('id', 'allocations')} for p in c['people']
                                      if p['role'] == 'split']))

    def read_split_records(self):
        """Consume every captured time/pay row; no normalized subset can omit a row."""
        split_ids = {pid for pid, p in self.people.items() if p['role'] == 'split'}
        declaration = self.case.get('time_records')
        if not split_ids:
            require(declaration is None, 'Time records supplied without CG-07 employees')
            return {}
        require(isinstance(declaration, dict) and declaration.get('checks'),
                'CG-07 requires captured actual time/pay records')
        rows, ids, sources = defaultdict(list), set(), set()
        for check in declaration['checks']:
            require(set(check['columns']) == {'id', 'person', 'date', 'code', 'hours', 'pay'},
                    'CG-07 time/pay columns must include id, person, date, code, hours and pay')
            require(check['source'] not in sources, 'Duplicate CG-07 source')
            sources.add(check['source'])
            for source_row in self.csv_records(check):
                row = {key: source_row[column] for key, column in check['columns'].items()}
                require(row['id'].strip() and row['id'] not in ids, 'Duplicate/blank time-record id')
                ids.add(row['id'])
                require(row['person'] in split_ids, 'Time record requires a CG-07 employee')
                require(self.start <= day(row['date']) <= self.end, 'Time record outside audit period')
                try:
                    hours = Decimal(row['hours'])
                except InvalidOperation as exc:
                    raise InputError('Time-record hours must be numeric') from exc
                require(hours.is_finite() and hours > 0, 'Time-record hours must be finite and positive')
                self.code(row['code'])
                money(row['pay'])
                rows[row['person']].append(dict(row, source=check['source']))
        require(set(rows) == split_ids, 'Actual time/pay records missing for a CG-07 employee')
        return rows

    def split_payroll(self, p):
        rule = self.policy('division')
        require('CG-07' in self.guide_paragraphs and self.case['guide_source'] in rule
                and 'CG-07' in self.rules['division']['citation'],
                'Division provenance must cite current guide CG-07')
        after = {self.code(code): money(amount) for code, amount in p.get('allocations', {}).items()}
        require(len(after) >= 2 and all(amount > 0 for amount in after.values()),
                'CG-07 requires at least two positive code allocations')
        # These code families have scenario-specific rules; do not silently bypass them.
        require(not set(after).intersection({'C-110', 'R-310', 'R-320', 'T-610', 'F-710', 'F-720'}),
                'CG-07 split involving a special-rule code needs reviewed scenario handling')
        actual = defaultdict(lambda: ZERO)
        refs = p['evidence'] + rule
        for row in self.split_rows[p['id']]:
            actual[row['code']] += money(row['pay'])
            refs.append(row['source'])
        require(dict(actual) == after, 'CG-07 allocations do not reconcile to actual time/pay records')
        require(sum(after.values(), ZERO) == p['_pay'], 'CG-07 allocations do not reconcile to full employee wages')
        reason = 'CG-07: code-specific pay from actual time records reconciles to full employee wages'
        for code, amount in after.items():
            self.add(p['name'], code, amount, refs, reason)
        self.person_codes[p['id']] = set(after)
        self.adjust(p['name'], p['_before'], p['_pay'], after, refs, reason)
        self.decisions.append(dict(subject=p['name'], reason=reason, evidence=refs))

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
        dated, rows, aggregate_people, dated_people = {}, [], set(), set()
        for original in self.case['allowances']:
            row = dict(original)
            require(row['id'] not in ids, 'Duplicate allowance id')
            ids.add(row['id'])
            amount = money(row['amount'])
            days = row['days']
            require(type(days) is int and days >= 0, 'Allowance days must be nonnegative integer')
            require(type(row['documented_reimbursement']) is bool, 'Reimbursement basis must be explicit')
            if row.get('date'):
                require(self.start <= day(row['date']) <= self.end, 'Allowance date outside audit period')
            if row['documented_reimbursement'] or days == 0:
                rows.append(row)
            elif row.get('date'):
                require(days == 1, 'Dated allowance must cover exactly one day')
                dated_people.add(row['person'])
                dated.setdefault((row['person'], row['date']), []).append(row)
            else:
                require(row.get('basis') == 'uniform_daily', 'Aggregate allowance needs uniform daily evidence or dated payments')
                self.evidence(row.get('basis_evidence'))
                require(money(row.get('daily_rate')) * days == amount, 'Aggregate allowance does not reconcile to daily rate')
                require(row['person'] not in aggregate_people, 'Multiple aggregate allowances may overlap; provide dated payments')
                aggregate_people.add(row['person'])
                rows.append(row)
        require(not aggregate_people.intersection(dated_people), 'Aggregate and dated allowances may overlap; provide dated payments')
        for (_, when), payments in dated.items():
            if len(payments) == 1:
                rows.append(payments[0])
                continue
            require(len({r.get('code') for r in payments}) == 1, 'Same-day allowance allocation needs one reviewed class')
            combined = dict(payments[0])
            combined.update(id=' + '.join(sorted(r['id'] for r in payments)),
                            amount=fmt(sum((money(r['amount']) for r in payments), ZERO)),
                            evidence=list(dict.fromkeys(ref for r in payments for ref in r['evidence'])))
            combined['allocation_evidence'] = list(dict.fromkeys(ref for r in payments for ref in r.get('allocation_evidence', [])))
            combined['_group_reason'] = ('Combined payments on ' + when + ': ' +
                '; '.join(r['id'] + ' ' + r['amount'] for r in payments) + '; one $47 worker/day cap')
            rows.append(combined)
        for row in rows:
            p = self.people[row['person']]
            refs = row['evidence'] + p['evidence'] + self.policy('allowance')
            if row.get('basis_evidence'):
                refs += self.evidence(row['basis_evidence'])
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
                reason = row.get('_group_reason', '$47 per recorded out-of-town day; only excess included')
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
