"""Compact draft outputs from an allocation ledger; rendering never approves a case."""
import csv
from decimal import Decimal
import io
import json
import re


def _currency_text(text):
    """Format cent amounts in human prose only; preserve links and nonmoney units."""
    protected = re.compile(r'(`[^`]*`|\[[^\]]*\]\([^)]*\)|<[^>]*>|https?://\S+)')
    amounts = re.compile(r'(?<![\w./:$,+-])([+-]?)(\$?)((?:\d{1,3}(?:,\d{3})+|\d+)\.\d{2})'
                         r'(?![\w%]|\.\d)')

    def prose(part):
        def replace(match):
            before, after = part[:match.start()], part[match.end():]
            if not match[2] and (
                re.match(r'\s*(?:%|percent\b|hours?\b|days?\b|weeks?\b|minutes?\b)', after, re.I)
                or re.search(r'\b(?:hours?|days?|weeks?|minutes?|ratio|rate)\s*[:=]?\s*$', before, re.I)
            ):
                return match[0]
            return match[1] + '$' + format(Decimal(match[3].replace(',', '')), ',.2f')
        return amounts.sub(replace, part)

    return ''.join(part if index % 2 else prose(part)
                   for index, part in enumerate(protected.split(text)))


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


def _record_name(source):
    return re.sub(r'\.(?:csv|md|txt|json)$', '', source['id']).replace('-', ' ').replace('_', ' ').replace('signin', 'sign-in').capitalize()


def _plain(text, sources):
    """Display prose; exact record identifiers remain available in the appendix/ledger."""
    for sid, source in sorted(sources.items(), key=lambda pair: -len(pair[0])):
        if '.' in sid:
            text = text.replace(sid, _record_name(source).lower())
    text = re.sub(r'\s*\([A-Z]{2,}-[A-Z0-9-]+\)', '', text)
    text = re.sub(r'\b[A-Z]{2,}-[A-Z0-9]+(?:-[A-Z0-9]+)*\b\s*', '', text)
    return text


def _reviewed_calls(ledgers):
    """Surface explicit reviewed recommendations, without inventing a priority score."""
    calls = []
    for ledger in ledgers:
        for note in ledger.get('case_notes', []):
            match = re.search(r'Recommend (first|second) employer call\b([^.]*(?:\.[0-9][^.]*)*)\.', note['detail'])
            if match:
                reason = match[2].lstrip(': ').removeprefix('because ')
                reason = re.sub(r'\b\d+\.\d{2}\b', lambda m: '$' + format(Decimal(m[0]), ',.2f'), reason)
                calls.append((1 if match[1] == 'first' else 2, ledger, reason))
    return sorted(calls, key=lambda item: item[0])


def _call_recommendations(ledgers):
    lines = []
    for rank, ledger, reason in _reviewed_calls(ledgers):
        lines.extend([str(rank) + '. **[' + ledger['employer'] + '](#' + ledger['slug'] + ')** — ' +
                      reason[0].upper() + reason[1:] + '.', ''])
    return lines or ['No call order has been recommended in the reviewed case notes.', '']


def _question_priority(pair, ledger):
    subject, item = pair
    if subject == 'Other payroll and duties':
        return (5, 0, 0)
    if subject == 'Records and audit period':
        return (4, 0, 0)
    context = ' '.join(item['labels'] + item['reasons']).lower()
    # Unresolved coverage/period evidence leads, then owners and other open
    # exceptions, then remaining named checks. Stable ties retain reviewed order.
    topic = (0 if any(word in context for word in ('invoice', 'certificate', 'receipts')) else
             1 if item['issues'] or 'owner' in context or 'election' in context else 2)
    impact = sum((abs(Decimal(a['net'])) for a in ledger['adjustments']
                  if a['id'] in item['adjustments']), Decimal(0))
    return (topic, 0 if item['issues'] else 1, -impact)


def _question_sections(ledger, groups, sources):
    slug = ledger['slug']
    employer_sources = {sid for sid, source in sources.items() if _source_audience(source) == 'employer'}
    # Attach the facts underlying a shared governing-code issue to the workers
    # whose recorded days/duties decide it. The policy treatment stays internal.
    payroll_subjects = {_subject(e['subject']) for e in ledger['entries'] + ledger['adjustments']}
    for subject, item in list(groups.items()):
        policies = [i for i in ledger['issues'] if i['id'] in item['issues']]
        if (subject in payroll_subjects or item['adjustments'] or item['factual_questions'] or not policies
                or not all(re.search(r'governing|corrected field|office transfers', i['treatment'], re.I) for i in policies)):
            continue
        targets = []
        for decision in ledger['decisions']:
            count = re.match(r'(\d+) unique in-period (positive roof|site) days', decision['reason'])
            if count and decision['subject'] in groups:
                targets.append((decision['subject'], count))
        if not targets:
            continue
        for name, count in targets:
            target = groups[name]
            target['_policy_only'] = target.get('_policy_only', not target['issues'])
            for key in ('issues', 'notes'):
                target[key].extend(value for value in item[key] if value not in target[key])
            target['sources'].update(item['sources'])
            # Roof workers already have named positive-day checks, individually
            # or in the routine crew question. Give office staff their own facts.
            if count[2] == 'site' and not target['factual_questions']:
                wages = sum((Decimal(e['amount']) for e in ledger['entries'] if e['subject'] == name), Decimal(0))
                target['factual_questions'].append(
                    'Confirm ' + name + '’s ' + count[1] + ' distinct site dates in the audit period and wages of ' + _money(wages) +
                    '; describe office duties and any visit purposes. Confirm whether duties were office-only and identify omitted visits or other field work.')
        del groups[subject]
    # One shared-record check replaces both timing and repeated document requests.
    combined = {'Records and audit period': dict(notes=[], adjustments=[], issues=[], sources=set(employer_sources),
                labels=[], reasons=[], facts=[], factual_questions=[])}
    for subject, item in groups.items():
        if not item['sources'] and not any(item[key] for key in ('notes', 'adjustments', 'issues')):
            continue
        context = ' '.join(item['labels'] + item['reasons']).lower()
        key = subject
        if 'source timing' in subject.lower() or subject == 'Nonemployee visitor':
            key = 'Records and audit period'
        elif subject.startswith('Gross receipts ') and 'Monthly receipts' in groups:
            key = 'Monthly receipts'
        elif (not item['factual_questions'] and 'invoice' not in context and 'certificate' not in context
              and (not item['issues'] or item.get('_policy_only') or ('governing' in context and 'owner' not in context))):
            key = 'Other payroll and duties'
        target = combined.setdefault(key, dict(notes=[], adjustments=[], issues=[], sources=set(), labels=[],
                                               reasons=[], facts=[], factual_questions=[]))
        for field in target:
            if field == 'sources':
                target[field].update(item[field])
            else:
                target[field].extend(value for value in item[field] if value not in target[field])
    record_numbers = {sid: n for n, sid in enumerate(sorted(employer_sources), 1)}
    packet = ', '.join('[' + _record_name(sources[sid]) + '](#' + slug + '-record-' + str(n) + ')'
                       for sid, n in record_numbers.items()) or 'No employer records supplied.'
    body = ['<a id="' + slug + '"></a>', '## ' + ledger['employer'], '',
            'Records: ' + packet + '.', '']
    appendix = ['### ' + ledger['employer'], '', '[Full ledger](ledgers/' + slug + '.json). '
                'Policy decisions remain in [internal decisions](internal-decisions.md#' + slug + ').', '']
    trace_rows = []
    seen_purposes, seen_evidence = {}, {}
    for number, (subject, item) in enumerate(sorted(combined.items(), key=lambda pair: _question_priority(pair, ledger)), 1):
        context = ' '.join(item['labels'] + item['reasons']).lower()
        adjustments = [a for a in ledger['adjustments'] if a['id'] in item['adjustments']]
        amount = sum((sum((Decimal(v) for v in a['after'].values()), Decimal(0)) for a in adjustments), Decimal(0))
        request = ' '.join(item['factual_questions'])
        needed = []
        outcome = ''
        owner = 'owner' in context or 'election' in context
        if subject == 'Records and audit period':
            request = ('For ' + ledger['employer'] + ', confirm the [common record checks](#common-confirmations) for ' +
                       ledger['audit_start'] + ' through ' + ledger['audit_end'] + '; list exceptions in this employer’s response.')
            if any('Nonemployee visitor' in label for label in item['labels']):
                request += ' Confirm that blank employee IDs in the site log are nonemployee visitors.'
            why = ledger['employer'] + ' needs its own completeness and period confirmation.'
            needed = ['A dated response from ' + ledger['employer'] + ', with any missing or corrected records.']
        else:
            if not request:
                subjects = list(dict.fromkeys(_subject(label) for label in item['labels']))
                named_payroll = {_subject(e['subject']) for e in ledger['entries'] + ledger['adjustments']}
                if subject == 'Other payroll and duties':
                    subjects = [name for name in subjects if name in named_payroll] or subjects
                request = 'Confirm wages and actual duties for ' + ', '.join(subjects) + '.'
                roof_counts = []
                for name in subjects:
                    for decision in ledger['decisions']:
                        count = re.match(r'(\d+) unique in-period positive roof days', decision['reason'])
                        if decision['subject'] == name and count:
                            roof_counts.append(name + ': ' + count[1])
                if roof_counts:
                    request += ' Confirm distinct dates with positive roofing time (' + '; '.join(roof_counts) + ').'
                if 'invoice' in context or 'certificate' in context:
                    request = 'Confirm ' + subject + '’s legal identity, trade, every payment and certificate authenticity, including any coverage gaps.'
                elif item['issues'] and ('owner' in context or 'election' in context):
                    request = 'Confirm ' + subject + '’s duties, remuneration and whether an exclusion election was filed.'
                elif 'site days' in context:
                    request += ' Confirm every site date and any omitted visits.'
            why = 'Checks the payroll and duty evidence supporting the current allocation.'
            if subject == 'Other payroll and duties':
                routine_pay = sum((Decimal(e['amount']) for e in ledger['entries']
                                   if _subject(e['subject']) in subjects), Decimal(0))
                why = 'Reconcile $' + format(routine_pay, ',.2f') + ' of allocated payroll for the named employees.'
                needed.append('Their payroll entries and duty records, with corrections marked.')
            elif owner:
                uncertain = any(i['id'] in item['issues'] and i['amount'] is None for i in ledger['issues'])
                why = (subject + '’s omitted remuneration remains unknown; missing election evidence establishes neither inclusion nor exclusion.'
                       if uncertain else 'Verify the reported election status and field duties supporting ' + subject + '’s owner basis.')
                facts = ' '.join(item['facts'] + item['factual_questions'])
                no_filing = bool(re.search(r'absence of (?:a )?filed election|\bno[ -]election(?! (?:form|evidence|document|record))', facts, re.I))
                needed.append(
                    ('Confirm the reported statement that no election was filed. If incorrect, provide the filed election and effective dates. '
                     if no_filing else 'State whether an election was filed; if filed, provide the election and effective dates. ') +
                    'If filing evidence is unavailable, state that separately; unavailable evidence does not mean no election was filed. '
                    'Provide duties and remuneration records.')
            elif 'invoice' in context or 'certificate' in context:
                why = 'Full-period coverage for the same legal entity determines whether subcontractor payments add payroll.'
                outcome = 'Proposed added payroll: ' + _money(amount) + '.'
                needed.append('Payment records, legal-entity evidence and coverage for the entire audit period, including renewals.')
            elif 'roof days' in context:
                why = 'The 15-roof-day boundary determines the classification of the worker’s whole pay.'
                needed.append('Dated roofing time entries and payroll reconciliation.')
            elif 'site days' in context or 'office day count' in context:
                why = 'At five or more site days, the contractor office rule moves the whole wage to the governing field code.'
                needed.append('Site dates, visit purposes and payroll records.')
            elif 'six visits' in context:
                why = 'The legal-duty exception remains open despite six real visits; construction duties would require further review.'
                needed.append('Site log and matter records identifying who attended and what work they performed.')
            elif 'zero-day' in context or 'zero days' in context:
                why = 'The payment remains provisionally included until its expense purpose or travel days are supported.'
                needed.append('Payment purpose, receipts and corrected travel-day records.')
            elif 'allowance' in context or 'travel' in context:
                why = 'Actual payments and days determine the daily allowance exclusion and any payroll excess.'
                needed.append('Dated payments, expense support and actual out-of-town days.')
            elif 'whole-week' in context or 'whole week' in context or 'route-day rule' in context:
                why = 'Two or more ride days changes the classification of the whole week’s pay; zero/one-day weeks stay clerical.'
                needed.append('Weekly gross pay matched to dated ride entries, including weeks without rides.')
            elif 'receipts' in context:
                why = 'Exact-period catering receipts determine whether the 40% threshold is met; the supplied-period proxy remains open.'
                needed.append('Daily sales at both period boundaries or an exact audit-period dining/catering summary.')
            net = sum((Decimal(a['net']) for a in adjustments), Decimal(0))
            if net and 'invoice' not in context and 'certificate' not in context:
                outcome = 'Proposed payroll ' + ('addition: $' if net > 0 else 'reduction: $') + format(abs(net), ',.2f') + '.'
                if owner:
                    outcome += ' Proposed owner basis: $' + format(amount, ',.2f') + '.'
            elif subject != 'Other payroll and duties' and not outcome and adjustments:
                after = {}
                for adjustment in adjustments:
                    for code, value in adjustment['after'].items():
                        after[code] = after.get(code, Decimal(0)) + Decimal(value)
                if 'site days' in context or 'office day count' in context:
                    outcome = ('Whole wage ' + _money(amount) + ' remains in clerical payroll (C-110).' if set(after) == {'C-110'} else
                               'Whole wage ' + _money(amount) + ' moves to the governing field allocation: ' +
                               _amounts({code: _money(value) for code, value in after.items()}) + '.')
                elif 'allowance' in context or 'travel' in context:
                    outcome = 'No allowance excess is currently added to payroll.'
                else:
                    outcome = 'Current allocation: ' + _amounts({code: _money(value) for code, value in after.items()}) + '.'
            # Preserve all reviewed facts, but separate stand-alone document requests.
            sentences = re.split(r'(?<=[.?])\s+(?=[A-Z])', request)
            evidence_sentences = [s for s in sentences if s.startswith(('Provide ', 'Supply ', 'Authenticate '))]
            questions = [s for s in sentences if s not in evidence_sentences]
            if questions:
                request = ' '.join(questions)
                if evidence_sentences and not owner:
                    needed = evidence_sentences  # More precise reviewed requests replace generic ones.
                elif evidence_sentences:
                    # Retain the reviewed request, conditional on a filing having
                    # occurred; never equate unavailable paperwork with no filing.
                    needed.append('Only if an election was filed: ' + ' '.join(evidence_sentences))
            if not needed:
                needed = ['Shared duty and payroll records; supporting dates and corrections for the stated facts.']
        anchor = slug + '-q-' + str(number)
        trace = slug + '-trace-' + str(number)
        indent = ' ' * (len(str(number)) + 2)
        evidence = _plain(' '.join(needed), sources)
        purpose_display = why
        if why in seen_purposes:
            previous, previous_subject = seen_purposes[why]
            purpose_display = 'Same test as [' + previous_subject + '](#' + previous + ').'
        else:
            seen_purposes[why] = (anchor, subject)
        if outcome:
            purpose_display += ' ' + outcome
        if evidence in seen_evidence:
            previous = seen_evidence[evidence]
            evidence = 'This subject’s entries in the [same evidence checklist](#' + previous + ').'
        else:
            seen_evidence[evidence] = anchor
        body.extend(['<a id="' + anchor + '"></a>', '', str(number) + '. **' + subject + '**', '',
                     indent + '**Question:** ' + _plain(request, sources), '',
                     indent + '**Why it matters:** ' + purpose_display, '',
                     indent + '**Evidence needed:** ' + evidence + ' [Traceability](#' + trace + ').', ''])
        trace_rows.append(['<a id="' + trace + '"></a>[' + str(number) + '. ' + subject + '](#' + anchor + ')',
                           '; '.join(dict.fromkeys(_subject(label) for label in item['labels'])), ', '.join(item['adjustments']) or '—',
                           ', '.join(item['notes']) or '—', ', '.join(item['issues']) or '—',
                           ', '.join(sorted(item['sources'])) or '—'])
    _table(appendix, ['Question', 'Subjects / records', 'Adjustments', 'Evidence notes', 'Open issues', 'Sources'], trace_rows)
    _table(appendix, ['Shared record', 'Source ID / original'], [
        ['<a id="' + slug + '-record-' + str(n) + '"></a>' + _record_name(sources[sid]),
         '[' + sid + '](' + sources[sid]['url'] + ')'] for sid, n in record_numbers.items()])
    return body, appendix


def render(ledgers):
    """Return relative filename -> text, preserving all ledger facts and CSV values."""
    files = {}
    report = ['# Draft audit report', '',
              'Provisional allocations. CSVs must accompany this report and audit-questions.md. '
              'Final audit sign-off is not established. Retrieval timestamps are provenance, not proof of a fresh live run.', '',
              'Case evidence appears once below; full notes, decisions, source paths and SHA-256 fingerprints remain in each linked ledger. '
              'Rule provenance and proposal approvals are in [internal-decisions.md](internal-decisions.md).', '']
    questions = ['# Audit questions', '', 'Recommended calls, in order:', ''] + _call_recommendations(ledgers)
    questions.extend(['Use the questions below to confirm facts before sign-off. Requests are not confirmations; '
                      'open business issues remain open. [Traceability appendix](#traceability-appendix).', ''])
    questions.extend(['<a id="common-confirmations"></a>', '', '**Common checks — apply separately to every employer**', '',
                      'Confirm that the listed records are authentic and complete for that employer’s audit period. '
                      'Identify omitted people, payments or records and supply corrections. Verify whether later field observations '
                      'describe audit-period duties; do not count post-period visits or rides as in-period events. '
                      'Collect each shared record once and reuse it for the named questions. Record a separate dated response '
                      'for each employer; one employer’s confirmation does not cover another.', ''])
    question_packages = {}
    question_appendix = ['<a id="traceability-appendix"></a>', '## Traceability appendix', '',
                        'Question links return to the call sheet. IDs map to the unchanged report and full ledgers.', '']
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

        def group(subject, evidence=(), label=None, ref=None, reason=None, fact=None, factual_question=None):
            key = _subject(subject)
            item = groups.setdefault(key, dict(notes=[], adjustments=[], issues=[], sources=set(), labels=[], reasons=[], facts=[], factual_questions=[]))
            item['sources'].update(set(evidence) & employer_sources)
            item['labels'].append(subject)
            if reason:
                item['reasons'].append(reason)
            if fact:
                item['facts'].append(fact)
            if factual_question and factual_question not in item['factual_questions']:
                item['factual_questions'].append(factual_question)
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
                # Only an explicitly reviewed factual prompt crosses this boundary.
                # Original questions may mix employer facts with auditor policy choices.
                group(note['subject'], note['evidence'], 'notes', ref, fact=note['detail'],
                      factual_question=note.get('factual_question'))
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

        body, appendix = _question_sections(ledger, groups, sources)
        question_packages[slug] = (body, appendix)

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
    call_ranks = {ledger['slug']: rank for rank, ledger, _ in _reviewed_calls(ledgers)}
    for slug in sorted(question_packages, key=lambda slug: call_ranks.get(slug, 3)):
        body, appendix = question_packages[slug]
        questions.extend(body)
        question_appendix.extend(appendix)
    files['audit-report.md'] = _currency_text('\n'.join(report) + '\n')
    files['audit-questions.md'] = _currency_text('\n'.join(questions + question_appendix) + '\n')
    files['internal-decisions.md'] = _currency_text('\n'.join(internal) + '\n')
    return files
