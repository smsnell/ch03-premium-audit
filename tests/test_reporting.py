"""Rendering checks cover traceability and audience boundaries, not prose snapshots."""
from copy import deepcopy
import csv
import importlib.util
import io
import json
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


class ReportingTests(unittest.TestCase):
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
                self.assertIn(amount, files['audit-report.md'])
        self.assertIn('sample-evidence-1', files['audit-questions.md'])
        self.assertIn(original['case_notes'][0]['detail'], files['audit-report.md'])
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
        self.assertEqual(1, employer.count('| Mira |'))
        self.assertIn('travel', employer)

    def test_same_name_unadjusted_pay_is_not_hidden_by_an_adjustment(self):
        sample = ledger()
        sample['entries'].append(dict(subject='Mira', code='C-110', amount='27.31',
                                      reason='Separate same-name employee', evidence=['payroll']))
        files = reporting.render([sample])
        self.assertIn('C-110 27.31', files['audit-report.md'])
        self.assertIn('Separate same-name employee', files['audit-report.md'])

    def test_audience_metadata_overrides_source_name_and_note_default(self):
        sample = ledger()
        sample['sources'][0]['audience'] = 'internal'
        sample['sources'][1]['audience'] = 'employer'
        sample['case_notes'][0]['audience'] = 'internal'
        files = reporting.render([sample])
        self.assertNotIn('payroll', files['audit-questions.md'])
        self.assertIn('guide', files['audit-questions.md'])
        self.assertNotIn('sample-evidence-1', files['audit-questions.md'])
        self.assertIn('sample-evidence-1', files['internal-decisions.md'])
        self.assertIn('adjustment-1', files['audit-questions.md'])

    def test_final_employer_questions_match_the_subject_and_audit_period(self):
        ledgers = [json.loads(p.read_text()) for p in sorted((ROOT / 'deliverables/ledgers').glob('*.json'))]
        files = reporting.render(ledgers)
        questions = files['audit-questions.md']
        dana = next(row for row in questions.splitlines() if '| Dana Whitcomb |' in row)
        request = dana.split('|')[3].lower()
        self.assertIn('site', request)
        self.assertTrue('days' in request or 'dates' in request)
        self.assertNotIn('certificate', request)
        self.assertNotIn('legal identity', request)
        for ref in ('severn-homebuilders-evidence-8', 'severn-homebuilders-evidence-12', 'adjustment-12'):
            self.assertIn(ref, dana)
        raymond = next(row for row in questions.splitlines() if '| Raymond Dunmore |' in row)
        request = raymond.split('|')[3].lower()
        self.assertTrue('no election' in request or 'absence' in request)
        self.assertIn('if', request)
        self.assertNotIn('if exclusion fails', request)
        for ref in ('patuxent-electric-evidence-2', 'patuxent-electric-evidence-9', 'adjustment-1'):
            self.assertIn(ref, raymond)
        for ledger in ledgers:
            section = questions.split('## ' + ledger['employer'], 1)[1].split('\n## ', 1)[0]
            timing = next(row for row in section.splitlines() if 'Source timing and confirmation status' in row)
            self.assertIn(ledger['audit_start'], timing)
            self.assertIn(ledger['audit_end'], timing)
            self.assertNotIn('duties, dates and amounts for Source timing', timing)
            self.assertIn(ledger['slug'] + '-evidence-1', timing)
            self.assertTrue('later' in timing or 'post-period' in timing)
        report = files['audit-report.md']
        for fact in ('11 distinct dates', '59840.70', '214 distinct', '118000.00', '63700.00', '54300.00'):
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
                self.assertIn(reporting._cell(note['detail']), destination)
                self.assertIn(ref, files['internal-decisions.md'] if reporting._internal_note(note) else files['audit-questions.md'])
            for adjustment in item['adjustments']:
                self.assertIn(adjustment['id'], files['audit-questions.md'])
            section = files['audit-questions.md'].split('## ' + item['employer'], 1)[1].split('\n## ', 1)[0]
            for source in item['sources']:
                if reporting._source_audience(source) == 'employer':
                    self.assertIn(source['id'], section)
                else:
                    self.assertNotIn(source['id'], section)


if __name__ == '__main__':
    unittest.main()
