"""Gate 3 CLI reuse checks. All records here are invented software fixtures."""
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_audit import COLLECTION_COLUMNS, capture_fixture

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'skills/class-code-assistant/scripts/audit.py'
SLUG = 'juniper-spark-services'


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_fixture(base):
    """Create a new employer with explicit agent-normalized mappings and provenance."""
    base.mkdir(parents=True, exist_ok=True)
    (base / 'guide.md').write_text(
        '**CG-04. C-110 Clerical office employees.**\n'
        '**CG-21. E-510 Electrical installation employees.**\n')
    (base / 'policy.md').write_text(
        'Synthetic test policy: five distinct site days moves all contractor office pay '
        'to the uniquely largest direct field payroll code; missing owner election stays open.\n')
    (base / 'register.csv').write_text(
        'employee_id,name,duties,pay,reported_code\n'
        'JS-E17,Mira Calder,Electrical installation,72819.43,E-510\n'
        'JS-E29,Owen Vale,Office administration,18234.56,C-110\n'
        'JS-O03,Elena Sato,Owner duties unknown,,\n')
    (base / 'signin.csv').write_text(
        'employee_id,date\n' + ''.join('JS-E29,2025-08-0' + str(i) + '\n' for i in range(4, 8)))
    sources = [dict(id=sid, path=name, sha256=fingerprint(base / name),
                    url='https://example.invalid/gate3/' + name,
                    retrieved_at='2026-11-03T16:00:00Z')
               for sid, name in [('guide', 'guide.md'), ('policy', 'policy.md'),
                                 ('register', 'register.csv'), ('signin', 'signin.csv')]]
    case = dict(slug=SLUG, employer='Juniper Spark Services', audit_start='2025-07-07', audit_end='2026-07-05',
                sources=sources, guide_source='guide',
                governing_eligibility={'E-510': dict(reason='Synthetic electrical contractor field work',
                                                    evidence=['guide', 'policy'])},
                rule_refs={key: dict(sources=['policy'], citation='Synthetic test policy, first paragraph')
                           for key in ('office', 'governing', 'owner')},
                reported={'C-110': '18234.56', 'E-510': '72819.43'},
                people=[dict(id='JS-E17', name='Mira Calder', role='direct', code='E-510',
                             pay='72819.43', reported_code='E-510',
                             reported_code_evidence=['register'], evidence=['register']),
                        dict(id='JS-E29', name='Owen Vale', role='office', code='C-110',
                             pay='18234.56', reported_code='C-110', contractor=True,
                             reported_code_evidence=['register'], evidence=['register']),
                        dict(id='JS-O03', name='Elena Sato', role='owner', code=None, pay=None,
                             off_register=True, election_status='unverified', evidence=['register'])],
                signin=[dict(person='JS-E29', date='2025-08-0' + str(i), evidence=['signin']) for i in range(4, 8)],
                **{name: [] for name in COLLECTION_COLUMNS if name not in ('people', 'signin')})
    write_case(base, case)
    return case


def write_case(base, case, name='case.json'):
    path = base / name
    path.write_text(json.dumps(capture_fixture(case, base), indent=2) + '\n')
    return path


def cli(base, output, *args):
    return subprocess.run([sys.executable, str(RUNNER), *args, '--output-dir', str(output)],
                          cwd=base, text=True, capture_output=True, check=False)


class Gate3ReuseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.case = write_fixture(self.base)

    def package(self, output, expected):
        self.assertEqual({'audit-report.md', 'audit-questions.md', 'codes/' + SLUG + '.csv',
                          'ledgers/' + SLUG + '.json', 'internal-decisions.md'},
                         {str(p.relative_to(output)) for p in output.rglob('*') if p.is_file()})
        with (output / 'codes' / (SLUG + '.csv')).open(newline='') as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(['class_code', 'payroll_allocated', 'rationale_ref'], reader.fieldnames)
            rows = list(reader)
        self.assertEqual(expected, {r['class_code']: r['payroll_allocated'] for r in rows})
        for row in rows:
            self.assertRegex(row['payroll_allocated'], r'^[0-9]+\.[0-9]{2}$')
            self.assertNotEqual('0.00', row['payroll_allocated'])
            self.assertEqual({'C-110': 'CG-04', 'E-510': 'CG-21'}[row['class_code']], row['rationale_ref'])
        return json.loads((output / 'ledgers' / (SLUG + '.json')).read_text())

    def test_new_employer_cli_and_explicit_unknown_owner(self):
        output = self.base / 'new-employer'
        result = cli(self.base, output, '--case', 'case.json')
        self.assertEqual(0, result.returncode, result.stderr)
        ledger = self.package(output, {'C-110': '18234.56', 'E-510': '72819.43'})
        self.assertEqual('91053.99', ledger['baseline'])
        self.assertEqual('0.00', ledger['net_adjustment'])
        self.assertEqual('provisionally accept', ledger['split_decision'])
        owner = next(i for i in ledger['issues'] if i['id'] == 'JS-O03-owner-election')
        self.assertIsNone(owner['amount'])
        self.assertIsNone(owner['alternative_amount'])
        self.assertEqual('open', owner['status'])
        report = (output / 'audit-report.md').read_text()
        questions = (output / 'audit-questions.md').read_text()
        self.assertIn('unknown (not zero)', report)
        self.assertIn('Elena Sato', report)
        self.assertIn('JS-O03-owner-election', questions)
        internal = (output / 'internal-decisions.md').read_text()
        for source in self.case['sources']:
            self.assertIn(source['id'], internal if source['id'] == 'guide' else questions)
            self.assertEqual(source['sha256'], next(s['sha256'] for s in ledger['sources'] if s['id'] == source['id']))

    def test_changed_source_stale_hash_fails_then_fresh_normalization_changes_allocation(self):
        original = self.base / 'original'
        self.assertEqual(0, cli(self.base, original, '--case', 'case.json').returncode)
        original_bytes = {str(p.relative_to(original)): p.read_bytes() for p in original.rglob('*') if p.is_file()}
        register = self.base / 'register.csv'
        register.write_text(register.read_text().replace('18234.56', '19456.78'))
        with (self.base / 'signin.csv').open('a') as stream:
            stream.write('JS-E29,2025-08-08\n')
        stale_output = self.base / 'stale'
        result = cli(self.base, stale_output, '--case', 'case.json')
        self.assertEqual(2, result.returncode)
        self.assertIn('Source fingerprint mismatch: register', result.stderr)
        self.assertFalse(stale_output.exists())
        self.assertFalse(list(self.base.glob('.audit-stage-*')))
        self.assertEqual(original_bytes, {str(p.relative_to(original)): p.read_bytes() for p in original.rglob('*') if p.is_file()})
        # Agent interpretation is explicit: updating a fingerprint alone does not parse prose/CSV.
        for source in self.case['sources']:
            source['sha256'] = fingerprint(self.base / source['path'])
        self.case['people'][1]['pay'] = '19456.78'
        self.case['reported']['C-110'] = '19456.78'
        self.case['signin'].append(dict(person='JS-E29', date='2025-08-08', evidence=['signin']))
        write_case(self.base, self.case, 'updated.json')
        updated = self.base / 'updated'
        result = cli(self.base, updated, '--case', 'updated.json')
        self.assertEqual(0, result.returncode, result.stderr)
        ledger = self.package(updated, {'E-510': '92276.21'})
        self.assertEqual('92276.21', ledger['baseline'])
        self.assertEqual('0.00', ledger['net_adjustment'])
        self.assertEqual('provisionally reject', ledger['split_decision'])
        adjustment = next(a for a in ledger['adjustments'] if a['subject'] == 'Owen Vale')
        self.assertEqual({'C-110': '19456.78'}, adjustment['before'])
        self.assertEqual({'E-510': '19456.78'}, adjustment['after'])
        self.assertEqual('open', ledger['issues'][0]['status'])
        self.assertIsNone(ledger['issues'][0]['amount'])

    def test_missing_inputs_publish_no_partial_bundle_and_preserve_existing_output(self):
        for kind in ('case-file', 'source-file', 'people-field', 'employee-pay'):
            with self.subTest(kind=kind):
                bad = deepcopy(self.case)
                if kind == 'case-file':
                    args = ['--case', 'case.json', '--case', 'absent.json']
                    expected = 'absent.json'
                else:
                    bad['slug'] = 'juniper-incomplete'
                    if kind == 'source-file':
                        next(s for s in bad['sources'] if s['id'] == 'signin')['path'] = 'absent-signin.csv'
                        expected = 'Missing source'
                    elif kind == 'people-field':
                        del bad['people']
                        expected = 'people'
                    else:
                        bad['people'][0]['pay'] = None
                        expected = 'Missing employee amount'
                    write_case(self.base, bad, 'incomplete.json')
                    args = ['--case', 'case.json', '--case', 'incomplete.json']
                output = self.base / ('missing-' + kind)
                result = cli(self.base, output, *args)
                self.assertEqual(2, result.returncode)
                self.assertIn('INCOMPLETE:', result.stderr)
                self.assertIn(expected, result.stderr)
                self.assertFalse(output.exists())
                self.assertFalse(list(self.base.glob('.audit-stage-*')))
        existing = self.base / 'existing'
        existing.mkdir()
        (existing / 'sentinel.txt').write_text('retain existing output\n')
        result = cli(self.base, existing, '--case', 'case.json')
        self.assertEqual(2, result.returncode)
        self.assertIn('Output directory already exists', result.stderr)
        self.assertEqual(['sentinel.txt'], [p.name for p in existing.iterdir()])
        self.assertEqual('retain existing output\n', (existing / 'sentinel.txt').read_text())

    def test_case_evidence_notes_keep_linked_question_and_validate_required_fields(self):
        note = dict(subject='Owen Vale site log', detail='Four distinct in-period site dates support C-110.',
                    question='Confirm the four dates and completeness of the site log.', evidence=['signin'])
        self.case['case_notes'] = [note]
        write_case(self.base, self.case)
        output = self.base / 'notes'
        result = cli(self.base, output, '--case', 'case.json')
        self.assertEqual(0, result.returncode, result.stderr)
        ledger = self.package(output, {'C-110': '18234.56', 'E-510': '72819.43'})
        self.assertEqual([note], ledger['case_notes'])
        report = (output / 'audit-report.md').read_text()
        questions = (output / 'audit-questions.md').read_text()
        self.assertIn(SLUG + '-evidence-1', report)
        self.assertIn(note['detail'], report)
        self.assertIn(SLUG + '-evidence-1', questions)
        self.assertIn(note['subject'], questions)
        self.assertIn('signin', report)
        self.assertIn('signin', questions)
        for field in ('subject', 'detail', 'question', 'evidence'):
            with self.subTest(field=field):
                bad = deepcopy(self.case)
                bad['case_notes'][0][field] = ['absent-record'] if field == 'evidence' else ' '
                write_case(self.base, bad, 'bad-note.json')
                failed_output = self.base / ('bad-note-' + field)
                result = cli(self.base, failed_output, '--case', 'bad-note.json')
                self.assertEqual(2, result.returncode)
                self.assertIn('Unknown evidence source' if field == 'evidence' else
                              'Case evidence requires subject, detail and question', result.stderr)
                self.assertFalse(failed_output.exists())


if __name__ == '__main__':
    unittest.main()
