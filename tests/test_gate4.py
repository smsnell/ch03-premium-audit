"""Gate 4 isolation and allocation regressions; all inputs are synthetic fixtures."""
from copy import deepcopy
import json
import unittest

import test_audit as fixtures
from test_gate3 import cli


class Gate4Tests(unittest.TestCase):
    setUp = fixtures.AuditTests.setUp
    case = fixtures.AuditTests.case
    person = fixtures.AuditTests.person
    run_case = fixtures.AuditTests.run_case
    site = fixtures.AuditTests.site

    def confirmation(self, slug='synthetic', kind='employer_fact'):
        return dict(case_slug=slug, issue_id='shared-issue', kind=kind,
                    by='Synthetic reviewer', at='2026-11-03',
                    scope='Synthetic record completeness only', evidence=['records'])

    def issue_case(self):
        case = self.case()
        case['open_issues'] = [dict(id=issue_id, subject='Synthetic person a',
                                   treatment='Synthetic proposed treatment', amount='100.00',
                                   alternative_amount='0.00', evidence=['records'])
                               for issue_id in ('shared-issue', 'other-issue')]
        return case

    def bundle_run(self, cases, name):
        path = self.base / (name + '.json')
        path.write_text(json.dumps({'cases': [fixtures.capture_fixture(case, self.base) for case in cases]}))
        output = self.base / name
        result = cli(self.base, output, '--bundle', str(path))
        return result, output

    def ledger(self, output, slug):
        return json.loads((output / 'ledgers' / (slug + '.json')).read_text())

    def test_cli_preserves_explicit_internal_audience(self):
        case = self.issue_case()
        case['case_notes'] = [dict(subject='Special convention', detail='Auditor must review the proposed convention.',
                                   question='Approve this convention?', evidence=['records'], audience='internal')]
        result, output = self.bundle_run([case], 'audience')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual('internal', self.ledger(output, 'synthetic')['case_notes'][0]['audience'])
        self.assertIn('Special convention', (output / 'internal-decisions.md').read_text())
        self.assertNotIn('Special convention', (output / 'audit-questions.md').read_text())

    def test_cli_confirmation_is_issue_and_employer_scoped_and_preserves_amounts(self):
        first = self.issue_case()
        second = deepcopy(first)
        second.update(slug='second', employer='Second Synthetic Employer')
        result, original = self.bundle_run([first, second], 'original')
        self.assertEqual(0, result.returncode, result.stderr)
        before_first = self.ledger(original, first['slug'])
        before_second = self.ledger(original, second['slug'])
        first['confirmations'] = [self.confirmation()]
        result, confirmed = self.bundle_run([first, second], 'confirmed')
        self.assertEqual(0, result.returncode, result.stderr)
        after = self.ledger(confirmed, first['slug'])
        self.assertEqual(before_second, self.ledger(confirmed, second['slug']))
        self.assertEqual(['confirmation_recorded', 'open'], [i['status'] for i in after['issues']])
        self.assertEqual([self.confirmation()], after['issues'][0]['confirmations'])
        self.assertEqual([], after['issues'][1]['confirmations'])
        for key in ('totals', 'baseline', 'net_adjustment', 'entries', 'adjustments', 'status'):
            self.assertEqual(before_first[key], after[key], key)
        self.assertIn('draft', after['status'])
        for old_issue, new_issue in zip(before_first['issues'], after['issues']):
            for key in ('amount', 'alternative_amount', 'treatment', 'evidence'):
                self.assertEqual(old_issue[key], new_issue[key])
        for slug in (first['slug'], second['slug']):
            self.assertEqual((original / 'codes' / (slug + '.csv')).read_bytes(),
                             (confirmed / 'codes' / (slug + '.csv')).read_bytes())
        first['confirmations'].append(self.confirmation(kind='internal_decision'))
        result, both = self.bundle_run([first, second], 'both-kinds')
        self.assertEqual(0, result.returncode, result.stderr)
        both_ledger = self.ledger(both, first['slug'])
        self.assertEqual(['employer_fact', 'internal_decision'],
                         [c['kind'] for c in both_ledger['issues'][0]['confirmations']])
        self.assertEqual(first['confirmations'], both_ledger['issues'][0]['confirmations'])
        self.assertEqual('open', both_ledger['issues'][1]['status'])
        self.assertEqual(before_second, self.ledger(both, second['slug']))
        self.assertEqual(before_first['totals'], both_ledger['totals'])

    def test_cli_rejects_wrong_employer_even_when_issue_id_matches_and_invalid_kind(self):
        first = self.issue_case()
        second = deepcopy(first)
        second.update(slug='second', employer='Second Synthetic Employer')
        for field, value in [('case_slug', 'second'), ('case_slug', None),
                             ('kind', None), ('kind', 'approval')]:
            with self.subTest(field=field, value=value):
                bad = deepcopy(first)
                record = self.confirmation()
                if value is None:
                    del record[field]
                else:
                    record[field] = value
                bad['confirmations'] = [record]
                result, output = self.bundle_run([bad, second], 'invalid-' + field + '-' + str(value))
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn('Confirmation', result.stderr)
                self.assertFalse(output.exists())
                self.assertFalse(list(self.base.glob('.audit-stage-*')))

    def test_roof_allowance_follows_calculated_siding_code(self):
        case = self.case()
        case['people'][0].update(role='roofing', code='R-310')
        case['reported'] = {'R-310': '100.00'}
        case['roofing'] = [dict(row, hours='1') for row in self.site('a', 14)]
        case['allowances'] = [dict(id='travel', person='a', amount='60.00', days=1, date='2025-08-01',
                                  documented_reimbursement=False, evidence=['records'])]
        ledger = self.run_case(case)
        self.assertEqual({'R-320': '113.00'}, ledger['totals'])
        allowance = next(a for a in ledger['adjustments'] if a['subject'].endswith('payment travel'))
        self.assertEqual({'R-320': '13.00'}, allowance['after'])

    def test_multicode_dispatcher_allowance_requires_code_and_allocation_evidence(self):
        case = self.case()
        case['people'][0]['role'] = 'dispatcher'
        case['route_weeks'] = [dict(person='a', start=start, pay='50.00', ride_dates=rides,
                                    evidence=['records']) for start, rides in
                               [('2025-07-07', []), ('2025-07-14', ['2025-07-14', '2025-07-15'])]]
        row = dict(id='travel', person='a', amount='60.00', days=1, date='2025-08-01',
                   documented_reimbursement=False, evidence=['records'])
        case['allowances'] = [row]
        for fields in ({}, {'code': 'T-610'}, {'allocation_evidence': ['records']},
                       {'code': 'T-610', 'allocation_evidence': ['missing-record']}):
            with self.subTest(fields=fields), self.assertRaises(fixtures.audit.InputError):
                bad = deepcopy(case)
                bad['allowances'][0].update(fields)
                self.run_case(bad)
        row.update(code='T-610', allocation_evidence=['records'])
        self.assertEqual({'C-110': '50.00', 'T-610': '63.00'}, self.run_case(case)['totals'])

    def test_allowance_uses_person_id_when_two_people_share_a_name(self):
        case = self.case()
        case['people'] = [self.person('a', '100.00', 'roofing', 'R-310'),
                          self.person('b', '200.00', 'direct', 'E-510')]
        case['people'][1]['name'] = case['people'][0]['name']
        case['reported'] = {'R-310': '100.00', 'E-510': '200.00'}
        case['roofing'] = [dict(row, hours='1') for row in self.site('a', 14)]
        case['allowances'] = [dict(id='travel', person='b', amount='60.00', days=1, date='2025-08-01',
                                  documented_reimbursement=False, evidence=['records'])]
        self.assertEqual({'R-320': '100.00', 'E-510': '213.00'}, self.run_case(case)['totals'])

    def test_included_field_owner_rejects_clerical_destination(self):
        case = self.case()
        case['people'] = [self.person('a', '100.00', 'owner', 'C-110',
                                     election_status='included', inclusion_evidence=['records'], field_work=True)]
        with self.assertRaises(fixtures.audit.InputError):
            self.run_case(case)
        case['people'][0]['code'] = 'E-510'
        self.assertEqual({'E-510': '63700.00'}, self.run_case(case)['totals'])


if __name__ == '__main__':
    unittest.main()
