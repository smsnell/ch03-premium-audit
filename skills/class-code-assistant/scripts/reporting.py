"""Compact draft outputs from an allocation ledger; rendering never approves a case."""
import csv
from decimal import Decimal
import io
import json
import re


def _cell(value):
    return str(value).replace('|', '\\|').replace('\n', '<br>')


def _table(lines, headings, rows):
    lines.extend(['| ' + ' | '.join(headings) + ' |',
                  '| ' + ' | '.join('---' for _ in headings) + ' |'])
    lines.extend('| ' + ' | '.join(_cell(v) for v in row) + ' |' for row in rows)
    lines.append('')


def _money(value):
    return format(Decimal(value), '.2f')


def _amounts(mapping):
    return '; '.join(code + ' ' + amount for code, amount in mapping.items()) or '—'


def _source_audience(source):
    if source.get('audience'):
        return source['audience']
    ident = source['id'].lower()
    return 'internal' if ident == 'guide' or ident.startswith('interview') else 'employer'


def _internal_note(note):
    subject = note['subject'].lower()
    return (note.get('audience') == 'internal' or subject.startswith('application decision')
            or 'call priority' in subject or subject.startswith(('rule ', 'policy ', 'proposal ')))


def _subject(subject):
    """Group factual observations by person/company, retaining record IDs in trace rows."""
    subject = subject.split(' / ', 1)[0]
    return re.split(r' (?:payment|invoice|week) ', subject, maxsplit=1)[0]


def _request(subject, evidence, labels, reasons, facts, audit_start, audit_end):
    if 'source timing' in subject.lower():
        return ('Confirm the application and records apply to ' + audit_start + ' through ' + audit_end +
                '; identify omitted people, payments or records. Confirm whether later field-note observations '
                'describe duties during that audit period, and distinguish post-period visits from in-period site or ride dates.')
    text = 'Confirm audit-period duties, dates and amounts for ' + subject + '; identify missing or corrected records.'
    context = ' '.join(labels).lower()
    reason_context = ' '.join(reasons).lower()
    fact_context = ' '.join(facts).lower()
    if 'owner' in context or 'election' in context or 'owner' in reason_context:
        if re.search(r'\bno[ -]election(?! form| evidence| document)', fact_context):
            text += ' Confirm the reported absence of an election; if that report is wrong, provide any filed election and its effective dates.'
        else:
            text += ' Provide the election and its effective dates; if exclusion fails, provide duties and remuneration.'
    # Route from this subject's payment/decision, not from shared governing-code evidence.
    if 'invoice' in context or 'certificate' in reason_context:
        text += ' Confirm legal identity, trade, each payment and certificate authenticity; supply full-period coverage evidence.'
    if 'site days' in reason_context or 'office day count' in context:
        text += ' Confirm all listed site days, dates, duties and the completeness of the sign-in record.'
    if 'allowance' in context or 'travel' in context:
        text += ' Provide payment purpose, expense support and corrected out-of-town days.'
    if any('receipt' in ref for ref in evidence):
        text += ' Provide exact audit-period dining/catering receipts or daily sales at both period boundaries and confirm supplied totals.'
    if any('route' in ref or 'weekly' in ref for ref in evidence):
        text += ' Confirm every listed payroll week and ride date, including zero/one-day weeks and annual reconciliation.'
    return text


def render(ledgers):
    """Return relative filename -> text, preserving all ledger facts and CSV values."""
    files = {}
    report = ['# Draft audit report', '',
              'Provisional allocations. CSVs must accompany this report and audit-questions.md. '
              'Final audit sign-off is not established. Retrieval timestamps are provenance, not proof of a fresh live run.', '',
              'Case evidence appears once below; full notes, decisions, source paths and SHA-256 fingerprints remain in each linked ledger. '
              'Rule provenance and proposal approvals are in [internal-decisions.md](internal-decisions.md).', '']
    questions = ['# Audit questions', '',
                 'Employer factual confirmations only. Proposed allocations are for review against the underlying facts; '
                 'the auditor owns rule interpretation and treatment approval. Note IDs refer to audit-report.md and the ledger; '
                 'all adjustments and relied-on employer records are mapped below. No request or proposed amount records a confirmation.', '']
    internal = ['# Internal audit decisions', '',
                'For the auditor/owner: verify rule provenance, approve or revise proposals, and select call priorities. '
                'These are separate from employer factual confirmations. Software/package acceptance does not approve an audit. '
                'One suitable, scoped confirmation can resolve the relevant fact or treatment; it does not resolve other open items.', '']
    for ledger in ledgers:
        slug = ledger['slug']
        stream = io.StringIO(newline='')
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['class_code', 'payroll_allocated', 'rationale_ref'])
        for code, amount in ledger['totals'].items():
            writer.writerow([code, amount, ledger['rationale_refs'][code]])
        files['codes/' + slug + '.csv'] = stream.getvalue()
        files['ledgers/' + slug + '.json'] = json.dumps(ledger, indent=2, ensure_ascii=False) + '\n'
        sources = {s['id']: s for s in ledger['sources']}
        employer_sources = {sid for sid, source in sources.items() if _source_audience(source) == 'employer'}
        groups = {}

        def group(subject, evidence=(), label=None, ref=None, reason=None, fact=None):
            key = _subject(subject)
            item = groups.setdefault(key, dict(notes=[], adjustments=[], issues=[], sources=set(), labels=[], reasons=[], facts=[]))
            item['sources'].update(set(evidence) & employer_sources)
            item['labels'].append(subject)
            if reason:
                item['reasons'].append(reason)
            if fact:
                item['facts'].append(fact)
            if label:
                item[label].append(ref)
            return item

        report.extend(['## ' + ledger['employer'], '',
                       ledger['split_decision'].capitalize() + ' the reported payroll split; ' + ledger['status'] + '.', '',
                       'Audit period: ' + ledger['audit_start'] + ' through ' + ledger['audit_end'] + '. '
                       '[Full ledger](ledgers/' + slug + '.json).', ''])
        _table(report, ['Code', 'Reported', 'Allocated', 'Difference'], [
            [code, ledger['reported'].get(code, '0.00'), ledger['totals'].get(code, '0.00'),
             _money(Decimal(ledger['totals'].get(code, '0')) - Decimal(ledger['reported'].get(code, '0')))]
            for code in sorted(set(ledger['reported']) | set(ledger['totals']))])
        report.extend(['Known register ' + ledger['baseline'] + ' + net adjustments ' + ledger['net_adjustment'] +
                       ' = allocated ' + _money(sum((Decimal(v) for v in ledger['totals'].values()), Decimal(0))) +
                       '. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.', '',
                       'Allocations and adjustments (application person-level code may be unspecified):', ''])
        rows = []
        for adjustment in ledger['adjustments']:
            rows.append([adjustment['id'], adjustment['subject'], _amounts(adjustment['before']),
                         _amounts(adjustment['after']), adjustment['net'], adjustment['reason'], ', '.join(adjustment['evidence'])])
            group(adjustment['subject'], adjustment['evidence'], 'adjustments', adjustment['id'], reason=adjustment['reason'])
        entry_totals, adjustment_totals = {}, {}
        for entry in ledger['entries']:
            key = (_subject(entry['subject']), entry['code'])
            entry_totals[key] = entry_totals.get(key, Decimal(0)) + Decimal(entry['amount'])
        for adjustment in ledger['adjustments']:
            for code, amount in adjustment['after'].items():
                key = (_subject(adjustment['subject']), code)
                adjustment_totals[key] = adjustment_totals.get(key, Decimal(0)) + Decimal(amount)
        # Collapse detailed rows only when the aggregate adjustment accounts for every
        # entry in that subject group, including all codes. Same-name extras stay visible.
        adjusted = {subject for subject, _ in adjustment_totals
                    if {code: amount for (name, code), amount in entry_totals.items() if name == subject}
                    == {code: amount for (name, code), amount in adjustment_totals.items() if name == subject}}
        for entry in ledger['entries']:
            group(entry['subject'], entry['evidence'], reason=entry['reason'])
            if _subject(entry['subject']) not in adjusted:
                rows.append(['allocation', entry['subject'], '—', entry['code'] + ' ' + entry['amount'],
                             '—', entry['reason'], ', '.join(entry['evidence'])])
        described = {_subject(item['subject']) for item in ledger['entries'] + ledger['adjustments'] + ledger.get('case_notes', [])}
        for decision in ledger['decisions']:
            group(decision['subject'], decision['evidence'], reason=decision['reason'])
            if _subject(decision['subject']) not in described:
                rows.append(['decision', decision['subject'], '—', '—', '—',
                             decision['reason'], ', '.join(decision['evidence'])])
        _table(report, ['ID', 'Employee/payment', 'Before', 'Allocated', 'Net', 'Reason', 'Sources'], rows)
        report.extend(['Case-specific evidence (note IDs are stable by input order):', ''])
        note_rows = []
        internal_notes = []
        for number, note in enumerate(ledger.get('case_notes', []), 1):
            ref = note.get('id', slug + '-evidence-' + str(number))
            if _internal_note(note):
                internal_notes.append((ref, note))
            else:
                note_rows.append([ref, note['subject'], note['detail'], ', '.join(note['evidence'])])
                group(note['subject'], note['evidence'], 'notes', ref, fact=note['detail'])
        _table(report, ['Note', 'Subject', 'Evidence and limits', 'Sources'], note_rows)
        report.extend(['Issues and confirmation status:', ''])
        issue_rows = []
        for issue in ledger['issues']:
            issue_rows.append([issue['id'], issue['subject'], issue['treatment'],
                               'unknown (not zero)' if issue['amount'] is None else issue['amount'],
                               'unknown' if issue['alternative_amount'] is None else issue['alternative_amount'],
                               issue['status'], ', '.join(issue['evidence'])])
            group(issue['subject'], issue['evidence'], 'issues', issue['id'])
            for confirmation in issue.get('confirmations', []):
                report.extend(['Confirmation for ' + issue['id'] + ': ' + json.dumps(confirmation, ensure_ascii=False) +
                               '. Scope is limited to this issue; no automatic audit approval.', ''])
        _table(report, ['Issue', 'Subject', 'Proposed treatment / missing evidence', 'Amount', 'Alternative', 'Status', 'Sources'], issue_rows)
        report.extend(['Sources (fingerprints and full local paths are in the ledger):', ''])
        _table(report, ['ID / record', 'Audience', 'Retrieved'], [
            ['[' + source['id'] + '](' + source['url'] + ')', _source_audience(source), source['retrieved_at']]
            for source in ledger['sources']])

        questions.extend(['## ' + ledger['employer'], ''])
        question_rows = []
        for number, (subject, item) in enumerate(groups.items(), 1):
            # Internal-only groups have no employer records to confirm.
            if not item['sources'] and not any(item[key] for key in ('notes', 'adjustments', 'issues')):
                continue
            trace = []
            for label in ('notes', 'adjustments', 'issues'):
                if item[label]:
                    trace.append(label + ': ' + ', '.join(item[label]))
            trace.append('sources: ' + ', '.join(sorted(item['sources'])))
            allocations = [a for a in ledger['adjustments'] if a['id'] in item['adjustments']]
            proposed = '; '.join(a['id'] + ': ' + _amounts(a['after']) + ' (net ' + a['net'] + ')' for a in allocations) or 'See mapped evidence/issues.'
            question_rows.append([slug + '-question-' + str(number), subject,
                                  _request(subject, item['sources'], item['labels'], item['reasons'], item['facts'], ledger['audit_start'], ledger['audit_end']), proposed, '<br>'.join(trace)])
        _table(questions, ['ID', 'Subject', 'Factual request', 'Proposed allocation', 'Traceability'], question_rows)
        _table(questions, ['Record confirmation', 'Source IDs'], [[
            'Confirm the authenticity, completeness and audit-period applicability of every listed employer record; '
            'identify corrections, missing records, omitted people/payments, and whether later observations describe the audit period.',
            ', '.join(sorted(employer_sources))]])

        internal.extend(['## ' + ledger['employer'], '',
                         '[Issues, amounts and statuses](audit-report.md#' + slug + ') and [full ledger](ledgers/' + slug + '.json). '
                         'Review each proposed treatment below against factual confirmations; keep unquantified gaps open.', ''])
        _table(internal, ['Rule', 'Provenance / limits', 'Sources'], [
            [key, rule['citation'], ', '.join(rule['sources'])] for key, rule in ledger['rule_refs'].items()])
        _table(internal, ['Issue / subject', 'Auditor decision required', 'Status'], [
            [issue['id'] + ' / ' + issue['subject'], issue['treatment'], issue['status']]
            for issue in ledger['issues']])
        _table(internal, ['Note / subject', 'Decision or priority evidence', 'Review request / sources'], [
            [ref + ' / ' + note['subject'], note['detail'], note['question'] + ' Sources: ' + ', '.join(note['evidence'])]
            for ref, note in internal_notes])
        internal.extend(['Review classification/proposal wording embedded in the remaining case notes internally; '
                         'employer questions request the underlying facts only. Any governing-code ordering, day-count convention, '
                         'owner-election precedence, proxy-period choice, zero-day treatment or professional-duty exception remains '
                         'a proposal wherever its issue is open.', ''])
        _table(internal, ['Internal source confirmation', 'Sources'], [[
            'Verify authenticity, completeness, applicable version and stated rule provenance; resolve guide/interview discrepancies without asking the employer to select policy.',
            ', '.join(sid for sid, source in sources.items() if _source_audience(source) != 'employer') or 'None']])
    files['audit-report.md'] = '\n'.join(report) + '\n'
    files['audit-questions.md'] = '\n'.join(questions) + '\n'
    files['internal-decisions.md'] = '\n'.join(internal) + '\n'
    return files
