import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'plugins/find-work/scripts'
sys.path.insert(0, str(SCRIPTS))
from lookup_application import lookup, normalized_url
from lookup_discovery import lookup_discovery

class LookupContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'job_search').mkdir()
        (self.root / 'applications/Example Company').mkdir(parents=True)
        self.fields = ['company', 'role', 'official_url', 'requisition_id', 'status', 'application_status']
        self.write('job_search/roles.csv', [dict(company='Example Company', role='Example Role', official_url='https://example.invalid/job', requisition_id='R1', status='active', application_status='Drafting')])
        self.write('applications.csv', [dict(company='Example Company', role='Example Role', official_url='https://example.invalid/job', status='Drafting')])

    def write(self, relative, rows):
        with (self.root / relative).open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_matching_rows_keep_separate_authorities(self):
        report = lookup(self.root, {'company':'Example Company', 'role':'Example Role'})
        self.assertTrue(report['lookup_complete'])
        self.assertEqual(2, len(report['records']))
        self.assertEqual({'applications.csv', 'job_search/roles.csv'}, {r['source'] for r in report['records']})

    def test_same_title_different_requisitions_are_ambiguous(self):
        self.write('job_search/roles.csv', [dict(company='Example Company', role='Example Role', requisition_id=req) for req in ['R1','R2']])
        report = lookup(self.root, {'company':'Example Company', 'role':'Example Role', 'requisition_id':'R1'})
        self.assertEqual('ambiguous', report['result'])
        self.assertEqual(['R1','R2'], report['role_groups'][0]['requisition_ids'])

    def test_missing_and_malformed_trackers_keep_no_match_incomplete(self):
        (self.root / 'applications.csv').unlink()
        self.assertFalse(lookup(self.root, {'company':'Other'})['lookup_complete'])
        self.write('applications.csv', [])
        with (self.root / 'job_search/roles.csv').open('a') as handle:
            handle.write('Broken,Short\n')
        report = lookup(self.root, {'company':'Other'})
        self.assertFalse(report['lookup_complete'])
        self.assertTrue(report['sources'][0]['warning_records'])

    def test_context_excludes_unapproved_and_production_wording(self):
        folder = self.root / 'applications/Example Company'
        (folder/'README.md').write_text('Target context')
        (folder/'approved_application_wording.md').write_text('Do not implicitly load')
        report = lookup(self.root, {'company':'Example Company'}, include_context=True)
        files = report['local_records'][0]['files']
        self.assertEqual('Target context', next(f['text'] for f in files if f['path'].endswith('README.md')))
        self.assertNotIn('text', next(f for f in files if f['path'].endswith('approved_application_wording.md')))

    def test_application_record_template_is_retrievable_without_loading_wording(self):
        (self.root/'applications/Example Company/application_record.md').write_text('Outstanding question and approval scope')
        report = lookup(self.root, {'company':'Example Company'}, include_context=True)
        self.assertTrue(any(f.get('text') == 'Outstanding question and approval scope' for record in report['local_records'] for f in record['files']))

    def test_batch_shares_records_and_does_not_confuse_live_and_application_state(self):
        lead = dict(company='Example Company', role='Example Role', requisition_id='R1')
        report = lookup_discovery(self.root, [lead, lead])
        self.assertEqual(2, len(report['sources']))
        self.assertEqual(2, len(report['records']))
        self.assertNotIn('different_recorded_states', report['candidates'][0]['identity_flags'])
        self.assertEqual(report['candidates'][0]['record_refs'], report['candidates'][1]['record_refs'])

    def test_url_tracking_is_ignored_but_role_query_is_preserved(self):
        self.assertEqual(normalized_url('https://example.invalid/job?utm_source=x&id=1'), normalized_url('https://example.invalid/job?id=1'))
        self.assertNotEqual(normalized_url('https://example.invalid/job?id=1'), normalized_url('https://example.invalid/job?id=2'))
        with self.assertRaises(ValueError):
            normalized_url('https://user:password' + '@' + 'example.invalid/job')
