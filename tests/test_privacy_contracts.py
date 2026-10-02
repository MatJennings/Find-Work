import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'plugins/find-work/scripts'))
from privacy_scan import scan_history_text, scan_text, forbidden_patterns

class PrivacyContracts(unittest.TestCase):
    def setUp(self):
        self.forbidden = forbidden_patterns(['Example Person'])
        self.identity = 'Example Person <' + 'person' + '@' + 'example.invalid>'

    def test_default_still_flags_git_identities(self):
        issues = []
        scan_history_text('Author: '+self.identity,self.forbidden,issues)
        self.assertTrue(issues)

    def test_explicit_review_exempts_only_git_identity_headers(self):
        issues = []
        scan_history_text('Author: '+self.identity+'\nCommit: '+self.identity+'\n    Generic commit',self.forbidden,issues,True)
        self.assertEqual([],issues)

    def test_commit_message_and_changed_paths_remain_scanned(self):
        issues = []
        scan_history_text('Author: '+self.identity+'\n    Leaked '+self.identity+'\nA\tExample Person.md',self.forbidden,issues,True)
        self.assertTrue(any('forbidden term' in item for item in issues))
        self.assertTrue(any('email address' in item for item in issues))

    def test_file_blob_cannot_be_exempted_by_identity_like_text(self):
        issues = []
        scan_text('historical blob','Author: '+self.identity,self.forbidden,issues)
        self.assertTrue(issues)
