import csv
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]/'plugins/find-work/scripts'
sys.path.insert(0,str(SCRIPTS))
from retrieve_evidence import retrieve as evidence
from retrieve_writing import retrieve as writing
from check_retrieval_sources import check
from context_sources import read_source

class RetrievalContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = 'experience/employers/example.md'
        self.put(self.source,'# Example\n\n## Role overview and scope\nTeam contribution only\n\n## Disclosure boundaries\nConfidential metric must not be used\n\n## Relevant work\nSupported action\n### Specific outcome\nQualitative result\n\n## Other work\n'+('Unrelated detail\n'*2000))
        self.put('profile/confidentiality_preferences.md','# Disclosure policy\nNo private metrics')
        self.put('experience/evidence_ledger.csv','claim_id,organization,claim,evidence_status,source,disclosure_status,notes\nEXAMPLE-1,Example,Supported action,user_attested,experience/employers/example.md,approval_required,Team contribution only\n')
        self.library = 'sources/authoritative/approved_resume_openings.md'
        self.put(self.library,'# Policy\nOnly explicitly approved wording.\n\n## First\n- Company: Example\n- Role: Role\n- Status: superseded\n- Context: platform\n### Exact approved wording\nPrior wording\n### Why it worked\nPrior lesson\n\n## Revised\n- Company: Example\n- Role: Role\n- Status: explicitly approved\n- Context: platform\n### Exact approved wording\nCurrent wording\n### Why it worked\nCurrent lesson\n\n## Other\n- Company: Different\n- Role: Role\n- Context: operations\n### Exact approved wording\nUnrelated text')

    def put(self,relative,text):
        path = self.root/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding='utf-8')

    def test_topics_keep_parent_scope_and_confidentiality(self):
        report = evidence(self.root,self.source,['Specific outcome'],claim_ids=['EXAMPLE-1'])
        self.assertTrue(report['complete'])
        text = '\n'.join(e['text'] for e in report['excerpts'])
        for term in ('Supported action','Qualitative result','Team contribution only','Confidential metric'):
            self.assertIn(term,text)
        self.assertNotIn('Unrelated detail',text)
        self.assertEqual('approval_required',report['claims'][0]['fields']['disclosure_status'])
        self.assertIn('No private metrics',report['disclosure_policy'][0]['text'])
        self.assertTrue(all(e['start_line']<=e['end_line'] for e in report['excerpts']))

    def test_small_and_unstructured_evidence_stays_whole(self):
        self.put(self.source,'# Example\n## Work\nAction\n## Limits\nPrivate scope')
        report = evidence(self.root,self.source,['Work'])
        self.assertTrue(report['complete'])
        self.assertIn('Private scope',report['excerpts'][0]['text'])

    def test_missing_heading_claim_or_disclosure_is_incomplete(self):
        self.assertFalse(evidence(self.root,self.source,['Absent'])['complete'])
        self.assertFalse(evidence(self.root,self.source,claim_ids=['MISSING'])['complete'])
        (self.root/'profile/confidentiality_preferences.md').unlink()
        self.assertFalse(evidence(self.root,self.source)['complete'])

    def test_duplicate_heading_is_not_silently_selected(self):
        self.put(self.source,'# Example\n## Work\nFirst\n## Work\nSecond')
        report = evidence(self.root,self.source,['Work'])
        self.assertFalse(report['complete'])
        self.assertIn('ambiguous', ' '.join(report['warnings']))

    def test_catalog_is_not_evidence_and_has_no_claim_body(self):
        report = evidence(self.root,self.source,catalog=True)
        self.assertTrue(report['complete'])
        self.assertEqual([],report['claims'])
        self.assertEqual([],report['excerpts'])

    def test_path_escape_is_rejected(self):
        report = evidence(self.root,'../outside.md')
        self.assertFalse(report['complete'])
        self.assertEqual([],report['sources'])
        with self.assertRaises(ValueError):
            read_source(self.root,'applications/Example/approved_application_wording.md',('experience/employers/',))

    def test_related_writing_versions_keep_full_wording_and_status(self):
        report = writing(self.root,'resume',entries=['Revised'])
        self.assertTrue(report['complete'])
        self.assertEqual(['First','Revised'],[e['entry_id'] for e in report['entries']])
        self.assertEqual('superseded',report['entries'][0]['metadata']['status'])
        self.assertIn('Current lesson',report['entries'][1]['excerpts'][0]['text'])
        self.assertNotIn('Unrelated text',str(report['entries']))

    def test_queries_route_on_metadata_not_wording(self):
        report = writing(self.root,'resume',queries=['platform'])
        self.assertEqual(['First','Revised'],[e['entry_id'] for e in report['catalog']])
        self.assertEqual([],report['entries'])
        self.assertEqual([],writing(self.root,'resume',queries=['Current wording'])['catalog'])

    def test_missing_or_duplicate_writing_entries_remain_explicit(self):
        self.assertFalse(writing(self.root,'resume',entries=['Missing'])['complete'])
        self.put(self.library,'# Policy\n## Duplicate\nOne\n## Duplicate\nTwo')
        report = writing(self.root,'resume',entries=['Duplicate'])
        self.assertFalse(report['complete'])
        self.assertEqual([],report['entries'])

    def test_blank_and_legacy_libraries_do_not_require_conversion(self):
        self.put(self.library,'# Blank approved library\nOnly final approved entries')
        self.assertTrue(writing(self.root,'resume')['complete'])
        self.put(self.library,'# Legacy\nApproved example recorded without headings')
        report = writing(self.root,'resume',queries=['example'])
        self.assertFalse(report['complete'])
        self.assertIn('Approved example',report['policy'][0]['text'])

    def test_freshness_changed_and_incomplete_sources_are_not_reusable(self):
        report = evidence(self.root,self.source,['Relevant work'])
        self.assertEqual('unchanged',check(self.root,[report])['source_state'])
        self.put(self.source,'Changed source')
        self.assertEqual('changed',check(self.root,[report])['source_state'])
        report['complete'] = False
        self.assertEqual('incomplete',check(self.root,[report])['source_state'])

    def test_shared_sources_are_checked_once_and_conflicts_survive(self):
        report = evidence(self.root,self.source)
        checked = check(self.root,[report,report])
        self.assertEqual(len(report['sources']),len(checked['observations']))
        other = dict(report,sources=[dict(s,path=s['path'],sha256='0'*64) for s in report['sources']])
        self.assertEqual('incomplete',check(self.root,[report,other])['source_state'])
