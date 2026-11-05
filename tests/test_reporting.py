"""Rendering checks cover traceability and audience boundaries, not prose snapshots."""
from copy import deepcopy
import csv
import importlib.util
import io
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reporting', ROOT / 'skills/class-code-assistant/scripts/reporting.py')
reporting = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reporting)


def ledger():
    return dict(slug='sample', employer='Sample Employer', status='draft; final sign-off not established',
                split_decision='provisionally reject', audit_start='2025-07-07', audit_end='2026-07-05',
                reported={'C-110': '100.00'}, totals={'E-510': '110.00'}, rationale_refs={'E-510': 'CG-21'},
                baseline='100.00', net_adjustment='10.00',
                sources=[dict(id=sid, path=sid, url='https://example.invalid/' + sid,
                              sha256='synthetic-' + sid, retrieved_at='2026-11-03T16:00:00Z', **extra)
                         for sid, extra in [('payroll', {}), ('guide', {}), ('interview-2', {}),
                                            ('house-policy', {'audience': 'internal'})]],
                rule_refs={'allowance': dict(citation='Synthetic policy', sources=['guide', 'house-policy'])},
                entries=[dict(subject='Mira', code='E-510', amount='110.00', reason='Electrical duties', evidence=['payroll'])],
                adjustments=[dict(id='adjustment-1', subject='Mira', before={'C-110': '100.00'},
                                  after={'E-510': '110.00'}, net='10.00', kind='adjustment',
                                  reason='Electrical duties and payment', evidence=['payroll', 'guide'])],
                decisions=[dict(subject='Mira', reason='Electrical duties', evidence=['payroll', 'guide'])],
                issues=[dict(id='travel', subject='Mira', treatment='Proposed zero-day payment inclusion',
                             evidence=['payroll', 'house-policy'], amount='10.00', alternative_amount='0.00',
                             status='open', confirmations=[])],
                case_notes=[dict(subject='Mira / payment', detail='Gross 100.00, allowance 10.00; travel days unknown.',
                                 question='Confirm 10.00 and select the governing house policy.', evidence=['payroll', 'house-policy']),
                            dict(subject='Application decision and call priority', detail='Review proposed priority.',
                                 question='Approve the suggested call order.', evidence=['guide', 'interview-2'])])


def sections(questions, employer):
    body, appendix = questions.split('## Traceability appendix', 1)
    body = body.split('## ' + employer + '\n', 1)[1].split('\n## ', 1)[0]
    appendix = appendix.split('### ' + employer + '\n', 1)[1].split('\n### ', 1)[0]
    return body, appendix


def blocks(questions):
    body = questions.split('## Traceability appendix', 1)[0]
    return re.findall(r'^\d+\. \*\*.*?(?=^\d+\. \*\*|^## |\Z)', body, re.M | re.S)


def question_for(questions, subject):
    return next(block for block in blocks(questions) if subject in block.split('\n', 1)[0])


def question_field(block, field):
    return re.search(r'\*\*' + re.escape(field) + r':\*\* (.*)', block)[1]


def trace_for(questions, item, block):
    number = re.match(r'(\d+)\.', block)[1]
    return next(row for row in sections(questions, item['employer'])[1].splitlines()
                if '](#' + item['slug'] + '-q-' + number + ')' in row)


class ReportingTests(unittest.TestCase):
    def test_currency_display_formats_cents_and_preserves_nonmonetary_tokens(self):
        original = (
            'Amounts: 47918.65, -54300.00; (0.00), -0.00 and $1,234.56 / -$2,345.67. '
            'Rates: 22.00395373%, 40.00%; counts: 214, 11 distinct dates; '
            'dates: 2026-07-05; time: 2026-11-03T16:00:00.00Z; '
            'duration: 1.25 hours, 2.50 days; code: `rate = 12.34`; '
            'source: https://example.invalid/12.34?q=56.78.'
        )
        expected = (
            'Amounts: $47,918.65, -$54,300.00; ($0.00), -$0.00 and $1,234.56 / -$2,345.67. '
            'Rates: 22.00395373%, 40.00%; counts: 214, 11 distinct dates; '
            'dates: 2026-07-05; time: 2026-11-03T16:00:00.00Z; '
            'duration: 1.25 hours, 2.50 days; code: `rate = 12.34`; '
            'source: https://example.invalid/12.34?q=56.78.'
        )
        self.assertEqual(expected, reporting._currency_text(original))
        self.assertEqual(expected, reporting._currency_text(expected))

    def test_routine_payroll_confirmation_includes_unchanged_wages_without_adjustments(self):
        sample = ledger()
        sample.update(adjustments=[], issues=[], case_notes=[], baseline='110.00',
                      net_adjustment='0.00', reported={'E-510': '110.00'})
        questions = reporting.render([sample])['audit-questions.md']
        routine = question_for(questions, 'Other payroll and duties')
        self.assertIn('Mira', routine)
        self.assertIn('$110.00', routine)
        self.assertNotIn('$0.00', routine)

    def test_render_preserves_ledger_csv_and_all_adjustment_trace(self):
        original = ledger()
        before = deepcopy(original)
        files = reporting.render([original])
        self.assertEqual(before, original)
        self.assertEqual(original, json.loads(files['ledgers/sample.json']))
        rows = list(csv.DictReader(io.StringIO(files['codes/sample.csv'])))
        self.assertEqual([dict(class_code='E-510', payroll_allocated='110.00', rationale_ref='CG-21')], rows)
        for adjustment in original['adjustments']:
            self.assertIn(adjustment['id'], files['audit-report.md'])
            self.assertIn(adjustment['id'], files['audit-questions.md'])
            for amount in list(adjustment['before'].values()) + list(adjustment['after'].values()) + [adjustment['net']]:
                self.assertIn(reporting._currency_text(amount), files['audit-report.md'])
        self.assertIn('sample-evidence-1', sections(files['audit-questions.md'], 'Sample Employer')[1])
        self.assertIn(reporting._currency_text(original['case_notes'][0]['detail']), files['audit-report.md'])
        self.assertIn('payroll', files['audit-questions.md'])

    def test_employer_questions_request_facts_and_internal_requests_stay_internal(self):
        files = reporting.render([ledger()])
        employer = files['audit-questions.md']
        for sid in ('guide', 'interview-2', 'house-policy'):
            self.assertNotIn(sid, employer)
            self.assertIn(sid, files['internal-decisions.md'])
        self.assertNotIn('select the governing house policy', employer)
        self.assertNotIn('Approve the suggested call order', employer)
        self.assertIn('Approve the suggested call order', files['internal-decisions.md'])
        self.assertIn('sample-evidence-2', files['internal-decisions.md'])
        # One factual question groups Mira's wage, payment, adjustment and open issue.
        self.assertEqual(1, sum('Mira' in block.split('\n', 1)[0] for block in blocks(employer)))
        self.assertIn('travel', employer)

    def test_reviewed_factual_questions_group_without_copying_mixed_policy_requests(self):
        sample = ledger()
        sample['case_notes'][0]['factual_question'] = 'Confirm Mira received 10.00 and provide the dated travel receipts.'
        sample['case_notes'].append(dict(
            subject='Mira / travel dates', detail='Two dates need checking.',
            question='Confirm dates and approve a zero-day exception.',
            factual_question='Identify Mira’s travel dates and correct any omitted trips.', evidence=['payroll']))
        sample['case_notes'][1]['factual_question'] = 'Internal-only prompt must stay internal.'
        before = deepcopy(sample)
        files = reporting.render([sample])
        questions = files['audit-questions.md']
        self.assertEqual(1, sum('Mira' in block.split('\n', 1)[0] for block in blocks(questions)))
        self.assertIn(reporting._currency_text(sample['case_notes'][0]['factual_question']), questions)
        self.assertIn(sample['case_notes'][2]['factual_question'], questions)
        self.assertNotIn('select the governing house policy', questions)
        self.assertNotIn('approve a zero-day exception', questions)
        self.assertNotIn('Internal-only prompt', questions)
        self.assertNotIn('Confirm audit-period duties, dates and amounts for Mira', question_for(questions, 'Mira'))
        self.assertEqual(before, sample)
        self.assertEqual(before, json.loads(files['ledgers/sample.json']))

    def test_same_name_unadjusted_pay_is_not_hidden_by_an_adjustment(self):
        sample = ledger()
        sample['entries'].append(dict(subject='Mira', code='C-110', amount='27.31',
                                      reason='Separate same-name employee', evidence=['payroll']))
        files = reporting.render([sample])
        self.assertIn('C-110 $27.31', files['audit-report.md'])
        self.assertIn('Separate same-name employee', files['audit-report.md'])

    def test_audience_metadata_overrides_source_name_and_note_default(self):
        sample = ledger()
        sample['sources'][0]['audience'] = 'internal'
        sample['sources'][1]['audience'] = 'employer'
        sample['case_notes'][0]['audience'] = 'internal'
        files = reporting.render([sample])
        self.assertNotIn('sources: payroll', files['audit-questions.md'])
        self.assertIn('guide', files['audit-questions.md'])
        self.assertNotIn('sample-evidence-1', files['audit-questions.md'])
        self.assertIn('sample-evidence-1', files['internal-decisions.md'])
        self.assertIn('adjustment-1', files['audit-questions.md'])

    def test_final_employer_questions_match_the_subject_and_audit_period(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        files = reporting.render(ledgers)
        questions = files['audit-questions.md']
        dana = question_for(questions, 'Dana Whitcomb')
        request = dana.lower()
        self.assertIn('site', request)
        self.assertTrue('days' in request or 'dates' in request)
        self.assertNotIn('certificate', request)
        self.assertNotIn('legal identity', request)
        appendix = sections(questions, 'Severn Homebuilders')[1]
        for ref in ('severn-homebuilders-evidence-8', 'severn-homebuilders-evidence-12', 'adjustment-12'):
            self.assertIn(ref, appendix)
            self.assertNotIn(ref, dana)
        raymond = question_for(questions, 'Raymond Dunmore')
        request = raymond.lower()
        self.assertTrue('no election' in request or 'absence' in request)
        self.assertIn('if', request)
        self.assertNotIn('if exclusion fails', request)
        appendix = sections(questions, 'Patuxent Electric')[1]
        for ref in ('patuxent-electric-evidence-2', 'patuxent-electric-evidence-9', 'adjustment-1'):
            self.assertIn(ref, appendix)
            self.assertNotIn(ref, raymond)
        for item in ledgers:
            body, appendix = sections(questions, item['employer'])
            timing = question_for(body, 'Records and audit period')
            self.assertIn(item['audit_start'], timing)
            self.assertIn(item['audit_end'], timing)
            self.assertIn('](#common-confirmations)', timing)
            self.assertIn('employer', timing.lower())
            self.assertIn(item['slug'] + '-evidence-1', appendix)
            records_number = re.match(r'(\d+)\.', timing)[1]
            records_row = next(line for line in appendix.splitlines()
                               if '](#' + item['slug'] + '-q-' + records_number + ')' in line)
            self.assertIn(item['slug'] + '-evidence-1', records_row)
            visitors = [(number, note) for number, note in enumerate(item['case_notes'], 1)
                        if note['subject'] == 'Nonemployee visitor']
            if visitors:
                self.assertIn('blank employee IDs', timing)
                self.assertIn('nonemployee visitors', timing)
                for number, note in visitors:
                    self.assertIn(note.get('id', item['slug'] + '-evidence-' + str(number)), records_row)
            else:
                self.assertNotIn('blank employee IDs', body)
        opening = questions.split('\n## ', 1)[0]
        self.assertIn('authentic and complete', opening.lower())
        self.assertTrue('later' in opening or 'post-period' in opening)
        self.assertEqual(1, questions.lower().count('authentic and complete'))
        report = files['audit-report.md']
        for fact in ('11 distinct dates', '$59,840.70', '214 distinct', '$118,000.00', '$63,700.00', '$54,300.00'):
            self.assertIn(fact, report)

    def test_actual_six_compact_package_keeps_all_note_and_source_coverage(self):
        paths = sorted((ROOT / 'deliverables/ledgers').glob('*.json'))
        self.assertEqual(6, len(paths))
        ledgers = [json.loads(path.read_text()) for path in paths]
        files = reporting.render(ledgers)
        all_markdown = '\n'.join(files[name] for name in ('audit-report.md', 'audit-questions.md', 'internal-decisions.md'))
        # Gate 3 report + questions were 199,351 bytes; include the new internal file in this budget.
        self.assertLessEqual(len(all_markdown.encode()), 199351 * .75)
        for item in ledgers:
            self.assertEqual(item, json.loads(files['ledgers/' + item['slug'] + '.json']))
            for number, note in enumerate(item['case_notes'], 1):
                ref = note.get('id', item['slug'] + '-evidence-' + str(number))
                self.assertIn(ref, all_markdown)
                destination = files['internal-decisions.md'] if reporting._internal_note(note) else files['audit-report.md']
                self.assertIn(reporting._currency_text(reporting._cell(note['detail'])), destination)
                self.assertIn(ref, files['internal-decisions.md'] if reporting._internal_note(note) else files['audit-questions.md'])
            for adjustment in item['adjustments']:
                self.assertIn(adjustment['id'], files['audit-questions.md'])
            body, section = sections(files['audit-questions.md'], item['employer'])
            for source in item['sources']:
                if reporting._source_audience(source) == 'employer':
                    self.assertIn(source['id'], section)
                else:
                    self.assertNotIn(source['id'], body + section)

    def test_questions_have_call_order_readable_blocks_and_linked_traceability(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        existing_report = (ROOT / 'deliverables/audit-report.md').read_text()
        ledgers.sort(key=lambda item: existing_report.index('## ' + item['employer'] + '\n'))
        files = reporting.render(ledgers)
        questions = files['audit-questions.md']
        body = questions.split('## Traceability appendix', 1)[0]
        lead = body.split('\n## ', 1)[0]
        self.assertTrue(questions.startswith('# Audit questions\n'))
        self.assertIn('<a id="common-confirmations"></a>', lead)
        self.assertLess(lead.index('Severn Homebuilders'), lead.index('Larkspur Lane Bistro'))
        for fact in ('$52,260.78', '$114,293.80'):
            self.assertIn(fact, lead)
        self.assertIn('insurance', lead.lower())
        self.assertIn('period evidence', lead.lower())
        self.assertEqual(6, len(re.findall(r'^## ', body, re.M)))
        employers = re.findall(r'^## (.+)$', body, re.M)
        priority = ['Severn Homebuilders', 'Larkspur Lane Bistro']
        self.assertEqual(priority + [item['employer'] for item in ledgers if item['employer'] not in priority], employers)
        expected_files = {'audit-report.md', 'audit-questions.md', 'internal-decisions.md'}
        expected_files.update('codes/' + item['slug'] + '.csv' for item in ledgers)
        expected_files.update('ledgers/' + item['slug'] + '.json' for item in ledgers)
        self.assertEqual(expected_files, set(files))
        for name in sorted(expected_files - {'audit-questions.md'}):
            existing = (ROOT / 'deliverables' / name)
            if name.endswith('.md'):
                self.assertEqual(reporting._currency_text(existing.read_text()), files[name], name)
            else:
                self.assertEqual(existing.read_bytes(), files[name].encode(), name)
        anchors = re.findall(r'<a (?:id|name)="([^"]+)"', questions)
        self.assertEqual(len(anchors), len(set(anchors)))
        local_links = re.findall(r'\]\(#([^)]*)\)', questions)
        self.assertTrue(local_links)
        self.assertTrue(set(local_links) <= set(anchors) | {'traceability-appendix'})
        for item in ledgers:
            section, trace = sections(questions, item['employer'])
            question_blocks = blocks(section)
            self.assertEqual(list(range(1, len(question_blocks) + 1)),
                             [int(re.match(r'(\d+)\.', block)[1]) for block in question_blocks])
            headings = [block.split('\n', 1)[0] for block in question_blocks]
            records_index = next(i for i, heading in enumerate(headings) if 'Records and audit period' in heading)
            routine = [i for i, heading in enumerate(headings) if 'Other payroll and duties' in heading]
            self.assertEqual(len(headings) - (2 if routine else 1), records_index)
            if routine:
                self.assertEqual([len(headings) - 1], routine)
            rows = [line for line in trace.splitlines() if line.startswith('| ') and re.search(r'\]\(#' + re.escape(item['slug']) + r'-q-\d+\)', line)]
            self.assertEqual(len(question_blocks), len(rows), item['employer'])
            mapped_trace = '\n'.join(rows)
            for number, block in enumerate(question_blocks, 1):
                for field in ('**Question:**', '**Why it matters:**', '**Evidence needed:**'):
                    self.assertIn(field, block)
                self.assertIn('](#' + item['slug'] + '-trace-' + str(number) + ')', block)
                matching_row = next(row for row in rows if '](#' + item['slug'] + '-q-' + str(number) + ')' in row)
                self.assertIn('<a id="' + item['slug'] + '-trace-' + str(number) + '"></a>', matching_row)
                self.assertNotIn('| ', block)
            # Repeated reasons/document requests must defer to shared defaults or an earlier block.
            for field in ('Why it matters', 'Evidence needed'):
                seen = set()
                for block in question_blocks:
                    value = re.search(r'\*\*' + field + r':\*\* (.*)', block)[1]
                    value = re.sub(r' \[Traceability\]\(#[^)]+\)\.', '', value)
                    if value in seen:
                        self.assertRegex(value, r'\]\(#[^)]+\)')
                    seen.add(value)
            for adjustment in item['adjustments']:
                self.assertIn(adjustment['id'], mapped_trace)
                self.assertNotIn(adjustment['id'], section)
            for issue in item['issues']:
                self.assertIn(issue['id'], mapped_trace)
            for number, note in enumerate(item['case_notes'], 1):
                ref = note.get('id', item['slug'] + '-evidence-' + str(number))
                self.assertNotIn(ref, section)
                if not reporting._internal_note(note):
                    self.assertIn(ref, mapped_trace)
                    if note.get('factual_question') and not note['subject'].startswith(('Source timing', 'Nonemployee visitor')):
                        sources = {source['id']: source for source in item['sources']}
                        prompt = reporting._plain(note['factual_question'], sources)
                        for sentence in re.split(r'(?<=[.?])\s+(?=[A-Z])', prompt):
                            self.assertIn(reporting._currency_text(sentence), section, note['subject'])
            for source in item['sources']:
                if reporting._source_audience(source) == 'employer':
                    self.assertIn(source['id'], mapped_trace)
                    self.assertNotIn(source['id'], section)
                    self.assertIn(re.sub(r'[^a-z0-9]', '', Path(source['path']).stem.lower()),
                                  re.sub(r'[^a-z0-9]', '', section.lower()))
                else:
                    self.assertNotIn(source['id'], section + trace)
            self.assertNotIn('Confirm audit-period duties, dates and amounts for', section)
            self.assertNotIn('Proposed allocation', section)

        severn = blocks(sections(questions, 'Severn Homebuilders')[0])
        leading_subjects = [block.split('\n', 1)[0] for block in severn[:3]]
        self.assertTrue(any('Kent Island Roofing' in title for title in leading_subjects[:2]))
        self.assertTrue(any('Tidewater' in title for title in leading_subjects[:2]))
        self.assertIn('Tenbury', leading_subjects[2])
        larkspur = blocks(sections(questions, 'Larkspur Lane Bistro')[0])
        self.assertIn('Monthly receipts', larkspur[0].split('\n', 1)[0])

    def test_reviewed_call_rank_uses_notes_and_preserves_unranked_input_order(self):
        ledgers = []
        for slug, recommendation in [('unranked-z', None), ('rank-two', 'second'),
                                     ('unranked-a', None), ('rank-one', 'first')]:
            item = ledger()
            item['slug'] = slug
            item['employer'] = slug.title()
            item['case_notes'] = item['case_notes'][:1]
            if recommendation:
                item['case_notes'].append(dict(
                    subject='Application decision and call priority',
                    detail='Recommend ' + recommendation + ' employer call: reviewed missing records.',
                    question='Review call order.', evidence=['guide']))
            ledgers.append(item)
        for supplied in (ledgers, list(reversed(ledgers))):
            files = reporting.render(supplied)
            body = files['audit-questions.md'].split('## Traceability appendix', 1)[0]
            expected = ['Rank-One', 'Rank-Two'] + [item['employer'] for item in supplied if item['slug'].startswith('unranked')]
            self.assertEqual(expected, re.findall(r'^## (.+)$', body, re.M))
            self.assertEqual([item['employer'] for item in supplied],
                             re.findall(r'^## (.+)$', files['audit-report.md'], re.M))
            self.assertEqual([item['employer'] for item in supplied],
                             re.findall(r'^## (.+)$', files['internal-decisions.md'], re.M))

    def test_new_employer_without_timing_note_still_has_records_confirmation_and_mapping(self):
        item = ledger()
        for field in ('entries', 'adjustments', 'decisions', 'issues', 'case_notes'):
            item[field] = []
        questions = reporting.render([item])['audit-questions.md']
        body, appendix = sections(questions, item['employer'])
        self.assertEqual(1, len(blocks(body)))
        records = question_for(body, 'Records and audit period')
        self.assertIn(item['audit_start'], records)
        self.assertIn(item['audit_end'], records)
        self.assertIn('](#common-confirmations)', records)
        row = next(line for line in appendix.splitlines() if '](#sample-q-1)' in line)
        self.assertIn('payroll', row)

    def test_new_employer_without_reviewed_call_recommendation_gets_no_invented_priority(self):
        questions = reporting.render([ledger()])['audit-questions.md']
        lead = questions.split('\n## ', 1)[0]
        self.assertNotIn('Severn', lead)
        self.assertNotIn('Larkspur', lead)
        self.assertNotIn('first', lead.lower())
        self.assertNotIn('second', lead.lower())
        self.assertNotIn('$52,260.78', questions)
        self.assertNotIn('$114,293.80', questions)
        self.assertNotIn('Approve the suggested call order', questions)
        body, appendix = sections(questions, 'Sample Employer')
        self.assertTrue(blocks(body))
        self.assertIn('adjustment-1', appendix)

    def test_reviewed_six_case_questions_keep_decisive_employer_facts(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        questions = reporting.render(ledgers)['audit-questions.md']
        expected = {
            'Tomas Reyes': ('“Thomas”', 'six visits', 'litigation notes/photos'),
            'Rafael Duarte': ('15 distinct', 'positive roofing time', '$47,918.65'),
            'Jamal Whitfield': ('9 distinct', 'positive roofing time', '$46,205.10'),
            'Teresa Lindqvist': ('9 listed site visits', 'measure houses'),
            'Marissa Gale': ('4 distinct site dates', '$71,250.45'),
            'Dana Whitcomb': ('11 distinct site dates', '$59,840.70'),
            'Raymond Dunmore': ('absence of a filed election', '214 distinct', '$118,000.00'),
            'Kyle Brandt': ('$390.00 with 0 recorded', 'What was the payment for?', 'receipts'),
            'Lena Ortiz': ('21 weeks with 0', '6 with 1', '21 with 2', '4 with 3', '$47,442.20'),
            'Paul Haskins': ('50 weeks with 0', '2 with 1', '$46,675.20'),
            'Kent Island Roofing': ('Kent Island Roofing & Siding LLC', '2026-01-31', '2026-07-05', 'coverage gaps'),
            'Monthly receipts': ('July 1–6, 2025', 'July 1–5, 2026', '$1,647,026.05'),
        }
        for subject, facts in expected.items():
            row = question_for(questions, subject)
            for fact in facts:
                self.assertIn(fact, row, subject)
        for owner in ('Catherine Harbor', 'Philip Crestwood', 'Martin Severn', 'Gloria Rhee', 'Rosa Delacroix'):
            row = question_for(questions, owner)
            for fact in ('filed election', 'effective dates', 'unknown, not zero', 'remuneration'):
                self.assertIn(fact, row, owner)
        for mixed_request in ('confirm the proposed election-first precedence',
                              'whether the proxy is accepted', 'whole-week T-610 classification'):
            self.assertNotIn(mixed_request, questions)

    def test_each_workers_outcome_remains_local_after_rule_deduplication(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        questions = reporting.render(ledgers)['audit-questions.md']
        for name in ('Curtis Bell', 'Hector Ruiz', 'Aaron Weiss'):
            why = question_field(question_for(questions, name), 'Why it matters')
            self.assertIn('$720.00', why, name)
            self.assertRegex(why.lower(), r'addition|add|included|excess')
        for name, amount, code in [('Marissa Gale', '$71,250.45', 'C-110'),
                                   ('Dana Whitcomb', '$59,840.70', 'H-420')]:
            why = question_field(question_for(questions, name), 'Why it matters')
            self.assertIn(amount, why, name)
            self.assertIn(code, why, name)
        self.assertRegex(question_field(question_for(questions, 'Marissa Gale'), 'Why it matters').lower(),
                         r'remain|retain|clerical')

    def test_shared_count_issue_maps_to_factual_workers_including_office_only_worker(self):
        item = json.loads((ROOT / 'deliverables/ledgers/bay-crest-exteriors.json').read_text())
        questions = reporting.render([item])['audit-questions.md']
        body, _ = sections(questions, item['employer'])
        self.assertNotIn('**Bay Crest crew and office transfer**', body)
        issue = next(issue for issue in item['issues'] if issue['id'] == 'P2-count-order')
        for subject in ('Rafael Duarte', 'Jamal Whitfield', 'Teresa Lindqvist', 'Nora Beckett', 'Other payroll and duties'):
            block = question_for(body, subject)
            row = trace_for(questions, item, block)
            self.assertIn(issue['id'], row, subject)
            for sid in issue['evidence']:
                if reporting._source_audience(next(s for s in item['sources'] if s['id'] == sid)) == 'employer':
                    self.assertIn(sid, row, subject)
            request = question_field(block, 'Question').lower()
            self.assertNotRegex(request, r'accepted count|governing.code order|before office|proposed convention|confirm.*policy')
        nora = question_field(question_for(body, 'Nora Beckett'), 'Question').lower()
        self.assertRegex(nora, r'office.only|office duties|stayed in (?:the )?office')
        self.assertRegex(nora, r'0 (?:distinct )?site|zero (?:distinct )?site|no .*site|no .*visits')
        self.assertRegex(nora, r'omitted|missing|other duties')
        routine = question_field(question_for(body, 'Other payroll and duties'), 'Question')
        for name, count in [('Darnell Price', 188), ('Kevin Moraes', 176), ('Sam Okonjo', 201),
                            ('Luis Carrillo', 164), ('Brian Tull', 152), ('Owen Petrakis', 97)]:
            self.assertRegex(routine, re.escape(name) + r'[^;\n]*\b' + str(count) + r'\b')

    def test_owner_evidence_distinguishes_no_filing_from_unavailable_document(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        questions = reporting.render(ledgers)['audit-questions.md']
        raymond = question_for(questions, 'Raymond Dunmore')
        evidence = question_field(raymond, 'Evidence needed').lower()
        self.assertRegex(evidence, r'no.election|no.filing|no election|absence|not filed')
        self.assertRegex(evidence, r'if .*incorrect|if .*wrong|if .*filed')
        self.assertNotIn('or confirmation it is unavailable', evidence)
        for owner in ('Catherine Harbor', 'Philip Crestwood', 'Martin Severn', 'Gloria Rhee', 'Rosa Delacroix'):
            evidence = question_field(question_for(questions, owner), 'Evidence needed').lower()
            self.assertIn('filed election', evidence, owner)
            self.assertIn('effective dates', evidence, owner)
            self.assertRegex(evidence, r'unavailable|cannot .*provid|missing', owner)
            self.assertNotRegex(evidence, r'unavailable[^.]*means[^.]*no (?:election|filing)')

    def test_renamed_cases_route_counts_and_keep_changed_amounts_without_fixed_names(self):
        originals = [json.loads((ROOT / 'deliverables/ledgers' / (slug + '.json')).read_text())
                     for slug in ('bay-crest-exteriors', 'patuxent-electric')]
        substitutions = {'Bay Crest Exteriors': 'North Orchard Trades', 'bay-crest-exteriors': 'north-orchard',
                         'Bay Crest crew and office transfer': 'Shared crew and office review',
                         'P2-count-order': 'new-count-review', 'Patuxent Electric': 'River Bend Wiring',
                         'patuxent-electric': 'river-bend'}
        for item in originals:
            for index, decision in enumerate(item['decisions']):
                subject = reporting._subject(decision['subject'])
                substitutions.setdefault(subject, 'Worker ' + str(len(substitutions)))
        def renamed(value):
            if isinstance(value, str):
                for old, new in sorted(substitutions.items(), key=lambda pair: -len(pair[0])):
                    value = value.replace(old, new)
                return value
            if isinstance(value, list):
                return [renamed(v) for v in value]
            if isinstance(value, dict):
                return {k: renamed(v) for k, v in value.items()}
            return value
        items = renamed(originals)
        roof, electrical = items
        for item, rank in ((roof, 'second'), (electrical, 'first')):
            item['case_notes'] = [note for note in item['case_notes'] if 'call priority' not in note['subject'].lower()]
            item['case_notes'].append(dict(subject='Application decision and call priority',
                detail='Recommend ' + rank + ' employer call: reviewed factual records.',
                question='Approve priority.', evidence=['interview-2']))
        for name, net in [('Curtis Bell', '835.17'), ('Hector Ruiz', '835.17'), ('Aaron Weiss', '942.86')]:
            adjustment = next(a for a in electrical['adjustments']
                              if a['subject'].startswith(substitutions[name] + ' payment'))
            adjustment['net'] = net
            adjustment['after'] = {next(iter(adjustment['after'])): net}
        before = deepcopy(items)
        files = reporting.render(items)
        self.assertEqual(before, items)
        questions = files['audit-questions.md']
        body = questions.split('## Traceability appendix', 1)[0]
        self.assertEqual([electrical['employer'], roof['employer']], re.findall(r'^## (.+)$', body, re.M))
        for name, net in [('Curtis Bell', '$835.17'), ('Hector Ruiz', '$835.17'), ('Aaron Weiss', '$942.86')]:
            why = question_field(question_for(questions, substitutions[name]), 'Why it matters')
            self.assertIn(net, why)
        roof_body, _ = sections(questions, roof['employer'])
        self.assertNotIn('**Shared crew and office review**', roof_body)
        for name in ('Rafael Duarte', 'Jamal Whitfield', 'Teresa Lindqvist', 'Nora Beckett'):
            block = question_for(roof_body, substitutions[name])
            self.assertIn('new-count-review', trace_for(questions, roof, block))
        self.assertIn('0', question_field(question_for(roof_body, substitutions['Nora Beckett']), 'Question'))


if __name__ == '__main__':
    unittest.main()
