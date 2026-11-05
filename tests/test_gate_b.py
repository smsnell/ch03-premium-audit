"""Gate B: new synthetic employers, reviewed eligibility and actual time/pay splits."""
import contextlib
import csv
from copy import deepcopy
from decimal import Decimal
import hashlib
import io
import json
import unittest

import test_audit as fixtures


audit = fixtures.audit
TIME_COLUMNS = dict(id='Entry number', person='Worker key', date='Work date',
                    code='Trade class', hours='Actual hours', pay='Earned wages')


class GateBTests(unittest.TestCase):
    setUp = fixtures.AuditTests.setUp
    case = fixtures.AuditTests.case
    person = fixtures.AuditTests.person
    site = fixtures.AuditTests.site

    def run_raw(self, case):
        return audit.Audit(case, self.base).run()

    def captured(self, case):
        return fixtures.capture_fixture(case, self.base)

    def time_capture(self, case, rows, sid='actual-time'):
        """A newly captured source, independent of normalized allocations."""
        path = self.base / (sid + '.csv')
        with path.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(TIME_COLUMNS.values()))
            writer.writeheader()
            writer.writerows({TIME_COLUMNS[k]: v for k, v in row.items()} for row in rows)
        case['sources'] = [s for s in case['sources'] if s['id'] != sid]
        case['sources'].append(dict(id=sid, path=path.name,
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            url='https://example.invalid/' + path.name, retrieved_at='2026-11-03T12:00:00Z'))
        return dict(source=sid, columns=dict(TIME_COLUMNS))

    def split_case(self):
        case = self.case()
        case.update(slug='new-split-employer', employer='New Synthetic Split Employer')
        case['people'] = [self.person('worker', '123.45', 'split', None,
            allocations={'E-510': '100.01', 'H-420': '23.44'})]
        case['reported'] = {'E-510': '123.45'}
        case['rule_refs']['division'] = dict(sources=['guide', 'records'], citation='CG-07 division of payroll')
        rows = [dict(id='time-1', person='worker', date='2025-07-07', code='E-510', hours='1', pay='60.00'),
                dict(id='time-2', person='worker', date='2025-07-08', code='E-510', hours='2', pay='40.01'),
                dict(id='time-3', person='worker', date='2025-07-09', code='H-420', hours='9', pay='23.44')]
        case['time_records'] = dict(checks=[self.time_capture(case, rows)])
        return self.captured(case), rows

    def governing_case(self):
        case = self.case()
        case['people'] = [self.person('office', '100.00', 'office', 'C-110', contractor=True),
                          self.person('field', '200.00', 'direct', 'E-510'),
                          self.person('shop', '1000.00', 'direct', 'M-830')]
        case['reported'] = {'C-110': '100.00', 'E-510': '200.00', 'M-830': '1000.00'}
        case['signin'] = self.site('office', 5)
        case['governing_eligibility'] = {'E-510': dict(reason='Reviewed field electrical duties', evidence=['guide', 'records'])}
        return self.captured(case)

    def test_governing_uses_reviewed_field_eligibility_before_office_transfer(self):
        result = self.run_raw(self.governing_case())
        self.assertEqual({'E-510': '300.00', 'M-830': '1000.00'}, result['totals'])
        self.assertEqual({'E-510': '200.00'}, result['governing_before_office'])

    def test_governing_missing_review_shop_candidate_and_missing_evidence_fail(self):
        baseline = self.governing_case()
        self.run_raw(baseline)
        variants = []
        bad = deepcopy(baseline); del bad['governing_eligibility']; variants.append(bad)
        for field, value in [('reason', ''), ('evidence', ['guide']), ('evidence', ['records']), ('evidence', [])]:
            bad = deepcopy(baseline); bad['governing_eligibility']['E-510'][field] = value; variants.append(bad)
        bad = deepcopy(baseline)
        bad['governing_eligibility']['M-830'] = dict(reason='Shop is larger', evidence=['guide', 'records'])
        variants.append(bad)
        bad = deepcopy(baseline)
        bad['governing_eligibility'] = {}
        variants.append(bad)
        for bad in variants:
            with self.subTest(eligibility=bad.get('governing_eligibility')), self.assertRaises(audit.InputError):
                self.run_raw(bad)

    def test_actual_pay_controls_split_despite_unequal_rates_and_conserves_cents(self):
        case, _ = self.split_case()
        result = self.run_raw(case)
        self.assertEqual({'E-510': '100.01', 'H-420': '23.44'}, result['totals'])
        self.assertEqual(Decimal('123.45'), sum(map(Decimal, result['totals'].values())))
        self.assertEqual('0.00', result['net_adjustment'])
        self.assertTrue(any('actual-time' in e['evidence'] for e in result['entries']))

    def test_new_employer_governing_cli_uses_reviewed_eligibility(self):
        case = self.governing_case()
        case.update(slug='fresh-field-business', employer='Fresh Synthetic Field Business')
        path = self.base / 'fresh-field.json'
        path.write_text(json.dumps(case))
        output = self.base / 'fresh-field-output'
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(0, audit.main(['--case', str(path), '--output-dir', str(output)]))
        with (output / 'codes/fresh-field-business.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual({'E-510': '300.00', 'M-830': '1000.00'},
                         {row['class_code']: row['payroll_allocated'] for row in rows})

    def test_split_requires_source_and_complete_column_mapping(self):
        case, _ = self.split_case()
        self.run_raw(case)
        variants = []
        bad = deepcopy(case); del bad['time_records']; variants.append(bad)
        bad = deepcopy(case); bad['time_records']['checks'][0]['source'] = 'missing'; variants.append(bad)
        bad = deepcopy(case); del bad['time_records']['checks'][0]['columns']['pay']; variants.append(bad)
        bad = deepcopy(case); bad['time_records']['checks'][0]['columns']['pay'] = 'pay'; variants.append(bad)
        for bad in variants:
            with self.subTest(records=bad.get('time_records')), self.assertRaises(audit.InputError):
                self.run_raw(bad)

    def test_split_omission_and_changed_allocations_fail_against_untouched_capture(self):
        case, _ = self.split_case()
        self.run_raw(case)
        original = (self.base / 'actual-time.csv').read_bytes()
        for allocations in ({'E-510': '100.01'}, {'E-510': '100.00', 'H-420': '23.45'},
                            {'E-510': '100.01', 'H-420': '23.44', 'M-830': '1.00'}):
            bad = deepcopy(case); bad['people'][0]['allocations'] = allocations
            with self.subTest(allocations=allocations), self.assertRaises(audit.InputError):
                self.run_raw(bad)
        self.assertEqual(original, (self.base / 'actual-time.csv').read_bytes())

    def test_fresh_capture_missing_row_cannot_reconcile_full_pay(self):
        case, rows = self.split_case()
        self.run_raw(case)
        # Refresh hash only because this deliberately models a distinct newly captured source.
        case['time_records']['checks'] = [self.time_capture(case, rows[:-1])]
        case['people'][0]['allocations'] = {'E-510': '100.01', 'H-420': '23.44'}
        with self.assertRaises(audit.InputError):
            self.run_raw(case)

    def test_invalid_actual_rows_fail_closed(self):
        baseline, rows = self.split_case()
        self.run_raw(baseline)
        for field, values in [('hours', ['0', '-1', 'NaN', 'Infinity', 'text']),
                              ('date', ['2025-07-06', '2026-07-06', 'invalid']),
                              ('person', ['unknown']), ('pay', ['1.001', 'NaN', '-1.00']),
                              ('id', ['', 'time-2']), ('code', ['UNKNOWN'])]:
            for value in values:
                with self.subTest(field=field, value=value):
                    bad = deepcopy(baseline); new_rows = deepcopy(rows); new_rows[0][field] = value
                    bad['time_records']['checks'] = [self.time_capture(bad, new_rows)]
                    with self.assertRaises(audit.InputError):
                        self.run_raw(bad)

    def test_ids_unique_across_sources_and_rows_must_name_split_person(self):
        case, rows = self.split_case()
        self.run_raw(case)
        duplicate = dict(rows[0])
        case['time_records']['checks'].append(self.time_capture(case, [duplicate], 'second-time'))
        with self.assertRaises(audit.InputError):
            self.run_raw(case)
        case, rows = self.split_case()
        case['people'].append(self.person('direct', '1.00', 'direct', 'E-510'))
        rows[0]['person'] = 'direct'
        case['time_records']['checks'] = [self.time_capture(case, rows)]
        self.captured(case)
        with self.assertRaises(audit.InputError):
            self.run_raw(case)

    def test_split_requires_guide_division_provenance_and_exact_full_wages(self):
        case, _ = self.split_case()
        self.run_raw(case)
        for rule in [dict(sources=['records'], citation='CG-07'), dict(sources=['guide', 'records'], citation='Other rule')]:
            bad = deepcopy(case); bad['rule_refs']['division'] = rule
            with self.subTest(rule=rule), self.assertRaises(audit.InputError):
                self.run_raw(bad)
        bad = deepcopy(case); bad['people'][0]['pay'] = '123.46'; self.captured(bad)
        with self.assertRaises(audit.InputError):
            self.run_raw(bad)

    def test_division_citation_must_exist_in_captured_guide(self):
        case, _ = self.split_case()
        self.run_raw(case)
        guide = self.base / 'guide.md'
        guide.write_text('\n'.join(line for line in guide.read_text().splitlines() if 'CG-07' not in line))
        # A different captured guide lacks the claimed paragraph, despite an accurate hash.
        next(source for source in case['sources'] if source['id'] == 'guide')['sha256'] = hashlib.sha256(guide.read_bytes()).hexdigest()
        with self.assertRaises(audit.InputError):
            self.run_raw(case)

    def test_specific_house_rule_roles_cannot_bypass_with_allocations(self):
        for role in ('direct', 'office', 'roofing', 'dispatcher', 'owner', 'catering'):
            case, _ = self.split_case()
            case['people'][0].update(role=role, code='E-510')
            with self.subTest(role=role), self.assertRaises(audit.InputError):
                self.run_raw(case)

    def test_special_code_families_cannot_bypass_house_rules_via_split(self):
        for code in ('C-110', 'R-310', 'R-320', 'T-610', 'F-710', 'F-720'):
            case, rows = self.split_case()
            case['people'][0]['allocations'] = {code: '100.01', 'H-420': '23.44'}
            rows[0]['code'] = rows[1]['code'] = code
            case['time_records']['checks'] = [self.time_capture(case, rows)]
            with self.subTest(code=code), self.assertRaises(audit.InputError):
                self.run_raw(case)

    def test_multicode_allowance_needs_explicit_allocation_evidence(self):
        case, _ = self.split_case()
        case['allowances'] = [dict(id='travel', person='worker', amount='50.00', days=1,
            documented_reimbursement=False, basis='uniform_daily', daily_rate='50.00',
            basis_evidence=['records'], evidence=['records'])]
        self.captured(case)
        with self.assertRaises(audit.InputError):
            self.run_raw(case)
        case['allowances'][0]['code'] = 'E-510'
        with self.assertRaises(audit.InputError):
            self.run_raw(case)
        case['allowances'][0]['allocation_evidence'] = ['records']
        self.assertEqual({'E-510': '103.01', 'H-420': '23.44'}, self.run_raw(case)['totals'])

    def test_new_employer_cli_and_atomic_failure_preserve_existing_outputs(self):
        case, _ = self.split_case()
        case['case_notes'] = [dict(subject='New worker duties', detail='Synthetic reviewed trade allocation.',
            question='Confirm trade duties.', factual_question='Which dated jobs involved electrical work?',
            evidence=['records'])]
        path = self.base / 'new-employer.json'; path.write_text(json.dumps(case))
        output = self.base / 'new-output'
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(0, audit.main(['--case', str(path), '--output-dir', str(output)]))
            self.assertEqual([case['slug'] + '.csv'], sorted(p.name for p in (output / 'codes').iterdir()))
            self.assertIn('Which dated jobs involved electrical work?', (output / 'audit-questions.md').read_text())
            before = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            case['people'][0]['allocations']['E-510'] = '100.00'
            path.write_text(json.dumps(case))
            self.assertEqual(2, audit.main(['--case', str(path), '--output-dir', str(output)]))
            self.assertEqual(before, {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()})
            fresh = self.base / 'invalid-new-output'
            self.assertEqual(2, audit.main(['--case', str(path), '--output-dir', str(fresh)]))
            self.assertFalse(fresh.exists())


if __name__ == '__main__':
    unittest.main()
