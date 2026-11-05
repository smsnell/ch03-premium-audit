"""Gate A fail-closed boundaries against untouched synthetic source captures."""
from copy import deepcopy
import csv
import hashlib
import unittest
import json

import test_audit as fixtures
from test_gate3 import cli


class GateATests(unittest.TestCase):
    setUp = fixtures.AuditTests.setUp
    case = fixtures.AuditTests.case
    person = fixtures.AuditTests.person

    def prepared(self, case):
        fixtures.capture_fixture(case, self.base)
        fixtures.audit.Audit(case, self.base).run()  # Establish valid baseline before mutations.
        return case

    def run_raw(self, case):
        return fixtures.audit.Audit(case, self.base).run()

    def test_every_collection_and_completeness_record_is_required(self):
        baseline = self.prepared(self.case())
        for name in fixtures.COLLECTION_COLUMNS:
            with self.subTest(collection=name), self.assertRaises(fixtures.audit.InputError):
                bad = deepcopy(baseline)
                del bad[name]
                self.run_raw(bad)
            with self.subTest(completeness=name), self.assertRaises(fixtures.audit.InputError):
                bad = deepcopy(baseline)
                del bad['completeness'][name]
                self.run_raw(bad)
        bad = deepcopy(baseline)
        del bad['completeness']
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(bad)

    def test_delete_one_invoice_rejected_against_untouched_capture(self):
        case = self.case()
        case['sub_invoices'] = [dict(id='invoice-' + str(i), name='Synthetic Trade', date='2025-09-01',
                                    amount='100.00', code='E-510', evidence=['records']) for i in range(2)]
        self.prepared(case)
        capture = self.base / 'synthetic-sub_invoices.csv'
        original = capture.read_bytes()
        source = deepcopy(next(s for s in case['sources'] if s['id'] == 'fixture-sub_invoices'))
        case['sub_invoices'].pop()
        # Do not recapture or edit fingerprints: this is the dangerous omission.
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(case)
        self.assertEqual(original, capture.read_bytes())
        self.assertEqual(source, next(s for s in case['sources'] if s['id'] == source['id']))
        path = self.base / 'deleted-invoice.json'
        path.write_text(json.dumps(case))
        output = self.base / 'deleted-invoice-output'
        result = cli(self.base, output, '--case', str(path))
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertFalse(output.exists())
        self.assertFalse(list(self.base.glob('.audit-stage-*')))

    def test_same_count_changed_invoice_is_not_complete(self):
        case = self.case()
        case['sub_invoices'] = [dict(id='invoice', name='Synthetic Trade', date='2025-09-01',
                                    amount='100.00', code='E-510', evidence=['records'])]
        self.prepared(case)
        for field, replacement in [('id', 'different-invoice'), ('amount', '99.99')]:
            bad = deepcopy(case)
            bad['sub_invoices'][0][field] = replacement
            with self.subTest(field=field), self.assertRaises(fixtures.audit.InputError):
                self.run_raw(bad)

    def test_route_rides_reconcile_independently_to_captured_log(self):
        case = self.case()
        case['people'][0]['role'] = 'dispatcher'
        case['route_weeks'] = [dict(person='a', start='2025-07-07', pay='100.00',
            ride_dates=['2025-07-07', '2025-07-08'], evidence=['records'])]
        self.prepared(case)
        original = (self.base / 'synthetic-route-log.csv').read_bytes()
        case['route_weeks'][0]['ride_dates'].pop()
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(case)
        self.assertEqual(original, (self.base / 'synthetic-route-log.csv').read_bytes())

    def test_unavailable_certificate_search_is_explicit_and_does_not_exempt_invoice(self):
        case = self.case()
        case['sub_invoices'] = [dict(id='invoice', name='Synthetic Trade', date='2025-09-01',
                                    amount='100.00', code='E-510', evidence=['records'])]
        fixtures.capture_fixture(case, self.base)
        case['completeness']['certificates'] = dict(status='unavailable', evidence=['records'])
        result = self.run_raw(case)
        self.assertEqual('60.00', result['totals']['E-510'])
        for name in ('signin', 'sub_invoices'):
            bad = deepcopy(case)
            bad[name] = []
            bad['completeness'][name] = dict(status='unavailable', evidence=['records'])
            with self.subTest(collection=name), self.assertRaises(fixtures.audit.InputError):
                self.run_raw(bad)

    def dated_allowances(self, same_day):
        case = self.case()
        case['allowances'] = [dict(id=str(i), person='a', amount=amount, days=1,
                                  date=date, documented_reimbursement=False, evidence=['records']) for i, (amount, date) in enumerate([
            ('70.00', '2025-08-01'), ('24.00', '2025-08-01' if same_day else '2025-08-02')])]
        return fixtures.capture_fixture(case, self.base)

    def test_daily_allowance_cap_groups_worker_day(self):
        for same_day, excess in [(False, '23.00'), (True, '47.00')]:
            with self.subTest(same_day=same_day):
                result = self.run_raw(self.dated_allowances(same_day))
                self.assertEqual(excess, result['net_adjustment'])
                self.assertEqual(fixtures.audit.fmt(fixtures.Decimal('100.00') + fixtures.Decimal(excess)),
                                 result['totals']['C-110'])

    def test_aggregate_allowance_requires_exact_supported_uniform_rate(self):
        case = self.case()
        row = dict(id='aggregate', person='a', amount='94.00', days=2, documented_reimbursement=False, evidence=['records'],
                   basis='uniform_daily', daily_rate='47.00', basis_evidence=['records'])
        case['allowances'] = [row]
        self.prepared(case)
        for field in ('basis', 'daily_rate', 'basis_evidence'):
            bad = deepcopy(case)
            del bad['allowances'][0][field]
            with self.subTest(field=field), self.assertRaises(fixtures.audit.InputError):
                self.run_raw(bad)
        bad = deepcopy(case)
        bad['allowances'][0]['daily_rate'] = '46.99'
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(bad)
        bad = deepcopy(case)
        bad['allowances'][0].update(amount='1754.00', days=22, daily_rate='79.73')
        fixtures.capture_fixture(bad, self.base)
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(bad)

    def test_multiple_or_mixed_aggregate_allowances_rejected(self):
        for second in [dict(id='second', person='a', amount='47.00', days=1, documented_reimbursement=False,
                            basis='uniform_daily', daily_rate='47.00', basis_evidence=['records'], evidence=['records']),
                       dict(id='second', person='a', amount='47.00', days=1, documented_reimbursement=False,
                            date='2025-08-01', evidence=['records'])]:
            case = self.case()
            case['allowances'] = [dict(id='first', person='a', amount='94.00', days=2, documented_reimbursement=False,
                basis='uniform_daily', daily_rate='47.00', basis_evidence=['records'], evidence=['records']), second]
            fixtures.capture_fixture(case, self.base)
            with self.subTest(second=second), self.assertRaises(fixtures.audit.InputError):
                self.run_raw(case)

    def test_owner_missing_evidence_never_sets_automatic_treatment(self):
        for status in ('included', 'excluded'):
            case = self.case()
            owner = self.person('owner', '100.00', 'owner', 'E-510', election_status=status,
                                field_work=True)
            case['people'] = [owner]
            fixtures.capture_fixture(case, self.base)
            with self.subTest(status=status), self.assertRaises(fixtures.audit.InputError):
                self.run_raw(case)
        case = self.case()
        case['people'] = [self.person('owner', '100.00', 'owner', 'E-510',
                                     election_status='unverified', field_work=True)]
        fixtures.capture_fixture(case, self.base)
        with self.assertRaises(fixtures.audit.InputError):
            self.run_raw(case)
        case = self.case()
        case['people'].append(self.person('owner', None, 'owner', None,
            election_status='unverified', off_register=True))
        fixtures.capture_fixture(case, self.base)
        result = self.run_raw(case)
        self.assertEqual('100.00', result['baseline'])
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        issue = next(i for i in result['issues'] if i['id'] == 'owner-owner-election')
        self.assertEqual('open', issue['status'])
        self.assertIsNone(issue['alternative_amount'])


    def test_included_off_register_owner_fixed_basis_preserves_unknown_input_pay(self):
        case = self.case()
        case['people'].append(self.person('owner', None, 'owner', 'E-510',
            election_status='included', inclusion_evidence=['records'], off_register=True, field_work=True))
        fixtures.capture_fixture(case, self.base)
        result = self.run_raw(case)
        self.assertEqual({'C-110': '100.00', 'E-510': '63700.00'}, result['totals'])
        self.assertEqual('63700.00', result['net_adjustment'])
        owner_control = next(p for p in result['input_controls']['owners'] if p['id'] == 'owner')
        self.assertIn('pay', owner_control)
        self.assertIsNone(owner_control['pay'])
        self.assertIsNone(case['people'][1]['pay'])
        case['people'][1]['field_work'] = False
        with self.assertRaisesRegex(fixtures.audit.InputError, 'Included non-field owner remuneration is unknown'):
            self.run_raw(case)

    def test_daily_allowance_duplicate_ids_dates_and_class_conflicts_fail(self):
        baseline = self.dated_allowances(same_day=True)
        self.run_raw(baseline)
        duplicate = deepcopy(baseline)
        duplicate['allowances'][1]['id'] = duplicate['allowances'][0]['id']
        with self.assertRaisesRegex(fixtures.audit.InputError, 'Duplicate allowance id'):
            self.run_raw(duplicate)
        conflict = deepcopy(baseline)
        for row, code in zip(conflict['allowances'], ('E-510', 'H-420')):
            row.update(code=code, allocation_evidence=['records'])
        with self.assertRaisesRegex(fixtures.audit.InputError, 'Same-day allowance allocation needs one reviewed class'):
            self.run_raw(conflict)
        for when in ('2025-07-06', '2026-07-06'):
            outside = deepcopy(baseline)
            outside['allowances'][0]['date'] = when
            fixtures.capture_fixture(outside, self.base)
            with self.subTest(date=when), self.assertRaisesRegex(fixtures.audit.InputError, 'Allowance date outside audit period'):
                self.run_raw(outside)

    def test_grouped_daily_allowance_retains_original_payment_ids_and_amounts(self):
        case = self.dated_allowances(same_day=True)
        result = self.run_raw(case)
        self.assertEqual(case['allowances'], result['input_controls']['allowance_inputs'])
        files = fixtures.audit.render([result])
        saved = json.loads(files['ledgers/synthetic.json'])
        self.assertEqual(case['allowances'], saved['input_controls']['allowance_inputs'])
        for row in case['allowances']:
            with self.subTest(payment=row['id']):
                self.assertIn(row['id'] + ' $' + format(fixtures.audit.money(row['amount']), ',.2f'), files['audit-report.md'])
        combined = next(a for a in result['adjustments'] if 'payment 0 + 1' in a['subject'])
        self.assertEqual({'C-110': '47.00'}, combined['after'])
        self.assertIn('0 70.00; 1 24.00', combined['reason'])

    def test_dropped_normalized_records_fail_against_each_frozen_capture(self):
        case = self.case()
        case['people'].append(self.person('b', '200.00', 'direct', 'E-510'))
        case['reported']['E-510'] = '200.00'
        case['signin'] = [dict(person='a', date='2025-08-01', evidence=['records'])]
        case['roofing'] = [dict(person='b', date='2025-08-01', hours='1', evidence=['records'])]
        case['allowances'] = [dict(id='travel', person='a', amount='70.00', days=1,
            date='2025-08-01', documented_reimbursement=False, evidence=['records'])]
        case['certificates'] = [dict(name='Synthetic Trade', start='2025-07-01',
                                    end='2026-07-06', evidence=['records'])]
        self.prepared(case)
        for name in ('people', 'signin', 'roofing', 'allowances', 'certificates'):
            bad = deepcopy(case)
            bad[name].pop()
            capture = self.base / ('synthetic-' + name + '.csv')
            original = capture.read_bytes()
            with self.subTest(collection=name), self.assertRaisesRegex(fixtures.audit.InputError,
                    'Source reconciliation failed for ' + name + ': missing'):
                self.run_raw(bad)
            self.assertEqual(original, capture.read_bytes())


    def test_receipts_require_completeness_and_full_raw_aggregate(self):
        for first_catering, second_catering in [('10.00', '50.00'), ('40.00', '30.00')]:
            with self.subTest(first_catering=first_catering):
                case = self.case()
                case['people'][0].update(role='catering', code='F-720')
                case['reported'] = {'F-720': '100.00'}
                full_catering = fixtures.audit.fmt(fixtures.Decimal(first_catering) + fixtures.Decimal(second_catering))
                case['receipts'] = dict(start=case['audit_start'], end=case['audit_end'],
                    gross='150.00', catering=full_catering, evidence=['records'])
                fixtures.capture_fixture(case, self.base)
                capture = self.base / 'synthetic-receipts.csv'
                with capture.open('w', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=('rawgross', 'rawcatering'))
                    writer.writeheader()
                    writer.writerows([dict(rawgross='100.00', rawcatering=first_catering),
                                      dict(rawgross='50.00', rawcatering=second_catering)])
                source = next(s for s in case['sources'] if s['id'] == 'fixture-receipts')
                source['sha256'] = hashlib.sha256(capture.read_bytes()).hexdigest()
                case['completeness']['receipts']['checks'][0]['columns'] = dict(gross='rawgross', catering='rawcatering')
                baseline = self.run_raw(case)
                self.assertEqual({'F-720': '100.00'}, baseline['totals'])
                original = capture.read_bytes()
                missing = deepcopy(case)
                del missing['completeness']['receipts']
                with self.assertRaises(fixtures.audit.InputError):
                    self.run_raw(missing)
                reduced = deepcopy(case)
                reduced['receipts'].update(gross='100.00', catering=first_catering)
                with self.assertRaisesRegex(fixtures.audit.InputError, '[Rr]eceipts|receipts'):
                    self.run_raw(reduced)
                self.assertEqual(original, capture.read_bytes())
                self.assertEqual(source['sha256'], hashlib.sha256(capture.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
