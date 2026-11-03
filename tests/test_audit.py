"""Synthetic Gate 2 boundaries; fixtures are not employer evidence."""
import contextlib
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit', ROOT / 'skills/class-code-assistant/scripts/audit.py')
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        guide = '\n'.join('**' + ref + '. ' + code + ' Synthetic description.**' for code, ref in {
            'C-110': 'CG-04', 'R-310': 'CG-11', 'R-320': 'CG-12', 'H-420': 'CG-15',
            'E-510': 'CG-21', 'T-610': 'CG-31', 'F-710': 'CG-41', 'F-720': 'CG-42'}.items())
        (self.base / 'guide.md').write_text(guide)
        (self.base / 'records.txt').write_text('Synthetic records for focused software tests only.')
        sources = []
        for sid, filename in [('guide', 'guide.md'), ('records', 'records.txt')]:
            sources.append(dict(id=sid, path=filename, sha256=hashlib.sha256((self.base / filename).read_bytes()).hexdigest(),
                                url='https://example.invalid/' + filename, retrieved_at='2026-11-03T12:00:00Z'))
        self.template = dict(slug='synthetic', employer='Synthetic Employer', audit_start='2025-07-07', audit_end='2026-07-05',
            sources=sources, guide_source='guide', rule_refs={key: dict(sources=['records'], citation='Synthetic test policy') for key in (
                'roofing', 'office', 'governing', 'owner', 'allowance', 'subcontractors', 'dispatcher', 'catering')},
            reported={'C-110': '100.00'}, people=[self.person('a', '100.00', 'office', 'C-110')])

    def person(self, pid, pay, role, code, **extra):
        return dict(id=pid, name='Synthetic person ' + pid, pay=pay, role=role, code=code, evidence=['records'], **extra)

    def case(self):
        return deepcopy(self.template)

    def run_case(self, case):
        return audit.Audit(case, self.base).run()

    def site(self, pid, count):
        return [dict(person=pid, date=str(date(2025, 7, 7) + timedelta(days=i)), evidence=['records']) for i in range(count)]

    def test_office_four_five_and_unique_in_period(self):
        for count, expected in [(4, {'C-110': '100.00', 'E-510': '200.00'}),
                                (5, {'E-510': '300.00'})]:
            with self.subTest(count=count):
                c = self.case()
                c['people'][0]['contractor'] = True
                c['people'].append(self.person('b', '200.00', 'direct', 'E-510'))
                c['reported']['E-510'] = '200.00'
                c['signin'] = self.site('a', count)
                c['signin'] += [deepcopy(c['signin'][0]), dict(person='a', date='2026-07-06', evidence=['records'])]
                result = self.run_case(c)
                self.assertEqual(expected, result['totals'])

    def test_roof_fourteen_fifteen_positive_unique_dates_no_hours_split(self):
        for count, expected in [(14, 'R-320'), (15, 'R-310')]:
            with self.subTest(count=count):
                c = self.case()
                c['people'] = [self.person('a', '100.00', 'roofing', 'R-310')]
                c['reported'] = {'R-310': '100.00'}
                c['roofing'] = [dict(r, hours='0.25') for r in self.site('a', count)]
                c['roofing'] += [deepcopy(c['roofing'][0]), dict(person='a', date='2026-07-06', hours='8', evidence=['records']),
                                 dict(person='a', date='2025-08-20', hours='0', evidence=['records'])]
                self.assertEqual({expected: '100.00'}, self.run_case(c)['totals'])

    def test_governing_before_office_transfers_and_supported_additions(self):
        c = self.case()
        c['people'] = [self.person('a', '1000.00', 'office', 'C-110', contractor=True),
                       self.person('b', '200.00', 'direct', 'E-510'), self.person('c', '100.00', 'direct', 'H-420')]
        c['reported'] = {'C-110': '1000.00', 'E-510': '200.00', 'H-420': '100.00'}
        c['signin'] = self.site('a', 5)
        c['sub_invoices'] = [dict(id='inv', date='2025-09-01', name='Synthetic Trade', amount='200.00', code='H-420', evidence=['records'])]
        c['certificates'] = []
        result = self.run_case(c)
        self.assertEqual({'E-510': '200.00', 'H-420': '1220.00'}, result['totals'])
        self.assertEqual({'E-510': '200.00', 'H-420': '220.00'}, result['governing_before_office'])

    def test_tied_and_absent_field_code_stays_open(self):
        for tied in (False, True):
            c = self.case()
            c['people'][0]['contractor'] = True
            c['signin'] = self.site('a', 5)
            if tied:
                c['people'] += [self.person('b', '200.00', 'direct', 'E-510'), self.person('c', '200.00', 'direct', 'H-420')]
                c['reported'].update({'E-510': '200.00', 'H-420': '200.00'})
            with self.assertRaises(audit.InputError):
                self.run_case(c)
            c['people'][0]['exception_issue'] = 'governing-proposal'
            c['open_issues'] = [dict(id='governing-proposal', subject='Synthetic person a',
                                    treatment='Explicit proposed C-110 retention pending field destination', amount='100.00', evidence=['records'])]
            result = self.run_case(c)
            self.assertEqual('100.00', result['totals']['C-110'])
            self.assertEqual('open', result['issues'][0]['status'])
            self.assertIn('governing', result['issues'][0]['id'])

    def sub_case(self):
        c = self.case()
        c['sub_invoices'] = [dict(id='inv', date='2025-09-01', name='Synthetic Trade', amount='100.01', code='R-310', evidence=['records'])]
        c['certificates'] = []
        return c

    def cert(self, **extra):
        return dict(name='Synthetic Trade', start='2025-07-01', end='2026-07-06', evidence=['records'], **extra)

    def test_sub_full_period_certificate_excludes(self):
        c = self.sub_case()
        c['certificates'] = [self.cert()]
        result = self.run_case(c)
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        self.assertIn('no addition', result['decisions'][-1]['reason'])

    def test_partial_certificate_does_not_exempt_pre_expiry_payment(self):
        c = self.sub_case()
        c['sub_invoices'][0]['date'] = '2025-09-01'
        cert = self.cert()
        cert['end'] = '2026-01-31'
        c['certificates'] = [cert]
        self.assertEqual('60.01', self.run_case(c)['totals']['R-310'])

    def test_alias_requires_explicit_approval_evidence_and_full_coverage(self):
        c = self.sub_case()
        cert = self.cert(alias_for='Synthetic Trade', alias_approved=False)
        cert['name'] = 'Synthetic Trade LLC'
        c['certificates'] = [cert]
        self.assertEqual('60.01', self.run_case(c)['totals']['R-310'])
        cert['alias_approved'] = True
        with self.assertRaises(audit.InputError):
            self.run_case(c)
        cert['alias_evidence'] = ['records']
        self.assertEqual({'C-110': '100.00'}, self.run_case(c)['totals'])
        cert['end'] = '2026-01-31'
        self.assertEqual('60.01', self.run_case(c)['totals']['R-310'])

    def test_per_invoice_half_up_before_aggregation(self):
        c = self.sub_case()
        c['sub_invoices'] = [dict(id=str(i), date='2025-09-01', name='Synthetic Trade', amount='0.01', code='R-310', evidence=['records']) for i in range(2)]
        self.assertEqual('0.02', self.run_case(c)['totals']['R-310'])

    def test_included_field_owner_fixed_basis(self):
        c = self.case()
        c['people'] = [self.person('a', '100.00', 'owner', 'E-510', reported_code='C-110',
                                   reported_code_evidence=['records'], election_valid=False, field_work=True)]
        result = self.run_case(c)
        self.assertEqual({'E-510': '63700.00'}, result['totals'])
        self.assertEqual('63600.00', result['net_adjustment'])

    def test_valid_owner_election_with_provisional_precedence(self):
        c = self.case()
        c['people'].append(self.person('owner', None, 'owner', 'E-510', election_valid=True, off_register=True,
                          election_start='2025-07-01', election_end='2026-07-06', election_evidence=['records']))
        result = self.run_case(c)
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        self.assertEqual('open', result['issues'][0]['status'])
        self.assertIn('precedence', result['issues'][0]['id'])

    def test_partial_owner_election_fails(self):
        c = self.case()
        c['people'].append(self.person('owner', None, 'owner', 'E-510', election_valid=True, off_register=True,
                          election_start='2025-07-01', election_end='2026-01-31', election_evidence=['records']))
        with self.assertRaises(audit.InputError):
            self.run_case(c)

    def test_unknown_off_register_owner_not_zero_or_63700(self):
        c = self.case()
        c['people'].append(self.person('owner', None, 'owner', None, election_valid=False, off_register=True))
        result = self.run_case(c)
        self.assertIsNone(result['issues'][0]['amount'])
        self.assertEqual('100.00', result['baseline'])
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        c['people'][1]['pay'] = '0.00'
        with self.assertRaises(audit.InputError):
            self.run_case(c)

    def test_allowance_cap_excess_zero_day_and_documented_expense(self):
        for amount, days, documented, extra in [('1034.00', 22, False, '0.00'), ('1754.00', 22, False, '720.00'),
                                                 ('390.00', 0, False, '390.00'), ('390.00', 0, True, '0.00')]:
            with self.subTest(amount=amount, days=days, documented=documented):
                c = self.case()
                row = dict(id='travel', person='a', code='C-110', amount=amount, days=days,
                           documented_reimbursement=documented, evidence=['records'])
                if documented:
                    row['reimbursement_evidence'] = ['records']
                c['allowances'] = [row]
                result = self.run_case(c)
                self.assertEqual(audit.fmt(Decimal('100') + Decimal(extra)), result['totals']['C-110'])
                self.assertEqual(days == 0 and not documented, bool(result['issues']))

    def test_route_one_two_days_week_and_site_independence(self):
        for count, code in [(0, 'C-110'), (1, 'C-110'), (2, 'T-610')]:
            c = self.case()
            c['people'][0]['role'] = 'dispatcher'
            c['route_weeks'] = [dict(person='a', start='2025-07-07', pay='100.00',
                                    ride_dates=['2025-07-07', '2025-07-08'][:count], evidence=['records'])]
            if count:
                c['route_weeks'][0]['ride_dates'].append('2025-07-07')
            c['signin'] = self.site('a', 9)
            self.assertEqual({code: '100.00'}, self.run_case(c)['totals'])

    def test_route_must_reconcile_and_pay_week_monday(self):
        c = self.case()
        c['people'][0]['role'] = 'dispatcher'
        c['route_weeks'] = [dict(person='a', start='2025-07-07', pay='99.99', ride_dates=[], evidence=['records'])]
        with self.assertRaises(audit.InputError):
            self.run_case(c)
        c['route_weeks'][0].update(start='2025-07-08', pay='100.00')
        with self.assertRaises(audit.InputError):
            self.run_case(c)

    def test_catering_below_exact_threshold_no_wage_proportion(self):
        for receipts, code in [('39.99', 'F-710'), ('40.00', 'F-720')]:
            c = self.case()
            c['people'] = [self.person('a', '100.00', 'catering', 'F-720')]
            c['reported'] = {'F-720': '100.00'}
            c['receipts'] = dict(start=c['audit_start'], end=c['audit_end'], gross='100.00', catering=receipts, evidence=['records'])
            result = self.run_case(c)
            self.assertEqual({code: '100.00'}, result['totals'])
            self.assertFalse(result['issues'])

    def test_receipts_period_mismatch_is_open_proxy(self):
        c = self.case()
        c['people'][0].update(role='catering', code='F-720')
        c['receipts'] = dict(start='2025-07-01', end='2026-06-30', gross='100.00', catering='22.00', evidence=['records'])
        result = self.run_case(c)
        self.assertEqual({'F-710': '100.00'}, result['totals'])
        self.assertEqual('receipts-period', result['issues'][0]['id'])
        self.assertIsNone(result['issues'][0]['amount'])

    def test_confirmation_isolated_never_approves_case_or_rewrites_payroll(self):
        c = self.case()
        c['open_issues'] = [dict(id=key, subject='Synthetic person a', treatment='Proposed exception', amount=None, evidence=['records']) for key in ('P1', 'P2')]
        c['confirmations'] = [dict(issue_id='P1', by='Synthetic reviewer', at='2026-11-03', scope='Duties only', evidence=['records'])]
        result = self.run_case(c)
        self.assertEqual(['confirmation_recorded', 'open'], [i['status'] for i in result['issues']])
        self.assertIn('draft', result['status'])
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        c['confirmations'][0]['issue_id'] = 'nonexistent'
        with self.assertRaises(audit.InputError):
            self.run_case(c)

    def test_harbor_style_exception_preserves_six_visits_and_open_issue(self):
        c = self.case()
        c['people'][0]['exception_issue'] = 'P1'
        c['open_issues'] = [dict(id='P1', subject='Synthetic person a', treatment='Legal professional visits; proposed clerical retention',
                                amount='100.00', evidence=['records'])]
        c['signin'] = self.site('a', 6)
        result = self.run_case(c)
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        self.assertEqual('open', result['issues'][0]['status'])
        self.assertEqual(6, len(c['signin']))

    def test_noncontractor_office_visits_require_explicit_exception(self):
        c = self.case()
        c['signin'] = self.site('a', 5)
        with self.assertRaises(audit.InputError):
            self.run_case(c)

    def test_zero_roof_days_requires_complete_source_evidence(self):
        c = self.case()
        c['people'][0].update(role='roofing', code='R-310')
        c['roofing'] = []
        with self.assertRaises(audit.InputError):
            self.run_case(c)
        c['people'][0]['roofing_evidence'] = ['records']
        self.assertEqual({'R-320': '100.00'}, self.run_case(c)['totals'])

    def test_employee_reported_code_requires_its_own_source_and_default_is_unspecified(self):
        c = self.case()
        result = self.run_case(c)
        self.assertEqual({'code not specified in application': '100.00'}, result['adjustments'][0]['before'])
        self.assertEqual('baseline_allocation', result['adjustments'][0]['kind'])
        c['people'][0]['reported_code'] = 'C-110'
        with self.assertRaises(audit.InputError):
            self.run_case(c)
        c['people'][0]['reported_code_evidence'] = ['records']
        self.assertEqual([], self.run_case(c)['adjustments'])

    def test_application_total_mismatch_is_open_register_baseline_not_fabricated(self):
        c = self.case()
        c['reported']['C-110'] = '99.00'
        result = self.run_case(c)
        self.assertEqual({'C-110': '100.00'}, result['totals'])
        self.assertEqual('100.00', result['baseline'])
        self.assertEqual('application-register-total', result['issues'][0]['id'])
        self.assertEqual('open', result['issues'][0]['status'])
        self.assertEqual('99.00', result['issues'][0]['alternative_amount'])

    def test_invoice_date_required_and_in_period(self):
        c = self.sub_case()
        for value in ('2025-07-06', '2026-07-06'):
            c['sub_invoices'][0]['date'] = value
            with self.assertRaises(audit.InputError):
                self.run_case(c)
        del c['sub_invoices'][0]['date']
        with self.assertRaises(KeyError):
            self.run_case(c)

    def test_invalid_money_unknown_employee_code_and_missing_records_fail(self):
        for value in ('NaN', 'Infinity', '-1.00', '1.001', '1,000.00', None, 1.0):
            with self.subTest(value=value), self.assertRaises(audit.InputError):
                audit.money(value)
        variants = []
        c = self.case(); c['people'][0]['code'] = 'Z-000'; variants.append(c)
        c = self.case(); c['people'][0]['role'] = 'unmapped'; variants.append(c)
        c = self.case(); c['people'][0]['pay'] = None; variants.append(c)
        c = self.case(); c['people'][0]['contractor'] = True; variants.append(c)
        c = self.case(); c['signin'] = [dict(person='unknown', date='2025-07-07', evidence=['records'])]; variants.append(c)
        c = self.case(); c['people'][0]['evidence'] = []; variants.append(c)
        c = self.case(); c['sources'][0]['sha256'] = 'changed'; variants.append(c)
        c = self.case(); c['people'][0]['pay'] = '0.00'; c['reported'] = {'C-110': '0.00'}; variants.append(c)
        for c in variants:
            with self.subTest(c=c), self.assertRaises(audit.InputError):
                self.run_case(c)

    def test_decimal_conservation_and_report_question_coverage(self):
        c = self.sub_case()
        result = self.run_case(c)
        self.assertEqual(Decimal(result['baseline']) + Decimal(result['net_adjustment']),
                         sum(Decimal(v) for v in result['totals'].values()))
        files = audit.render([result])
        self.assertEqual('class_code,payroll_allocated,rationale_ref', files['codes/synthetic.csv'].splitlines()[0])
        self.assertIn('R-310,60.01,CG-11', files['codes/synthetic.csv'])
        self.assertIn('Synthetic Trade invoice inv', files['audit-report.md'])
        for item in result['adjustments']:
            self.assertIn(item['id'], files['audit-questions.md'])
        for source in result['sources']:
            self.assertIn('Confirm record ' + source['id'], files['audit-questions.md'])

    def test_cli_one_bundle_missing_input_preserves_previous_and_new_directory(self):
        path = self.base / 'case.json'
        path.write_text(json.dumps(self.case()))
        output = self.base / 'output'
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(0, audit.main(['--case', str(path), '--output-dir', str(output)]))
            before = (output / 'audit-report.md').read_bytes()
            self.assertEqual(2, audit.main(['--case', str(path), '--output-dir', str(output)]))
            self.assertEqual(before, (output / 'audit-report.md').read_bytes())
            bad = self.case(); bad['people'][0]['pay'] = None
            path.write_text(json.dumps(bad))
            self.assertEqual(2, audit.main(['--case', str(path), '--output-dir', str(self.base / 'bad-output')]))
            self.assertFalse((self.base / 'bad-output').exists())
            first, second = self.case(), self.case()
            second.update(slug='second', employer='Second Synthetic Employer')
            bundle = self.base / 'bundle.json'
            bundle.write_text(json.dumps({'cases': [first, second]}))
            self.assertEqual(0, audit.main(['--bundle', str(bundle), '--output-dir', str(self.base / 'bundle-output')]))
            self.assertTrue((self.base / 'bundle-output/codes/second.csv').exists())
            second['people'][0]['role'] = 'unmapped'
            bundle.write_text(json.dumps([first, second]))
            self.assertEqual(2, audit.main(['--bundle', str(bundle), '--output-dir', str(self.base / 'invalid-bundle')]))
            self.assertFalse((self.base / 'invalid-bundle').exists())

    def test_cli_changed_source_and_traversal_fail_closed(self):
        path = self.base / 'case.json'
        c = self.case()
        path.write_text(json.dumps(c))
        (self.base / 'records.txt').write_text('Changed source')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(2, audit.main(['--case', str(path), '--output-dir', str(self.base / 'changed')]))
        self.assertFalse((self.base / 'changed').exists())
        c['slug'] = '../escape'
        with self.assertRaises(audit.InputError):
            self.run_case(c)


if __name__ == '__main__':
    unittest.main()
