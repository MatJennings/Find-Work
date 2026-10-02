import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/find-work/skills'

class WorkflowContracts(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding='utf-8')

    def test_intermediary_requires_tracing_detail_and_application_evidence(self):
        policy = (SKILLS/'find-jobs/references/verification.md').read_text()
        for term in ('two or three distinctive quoted phrases', 'complete live intermediary', 'functional application path', 'Never guess the employer', 'uncertain'):
            self.assertIn(term, policy)

    def test_lookup_never_establishes_current_verification_or_approval(self):
        policy = (SKILLS/'find-jobs/references/retrieval.md').read_text()
        for term in ('Different requisitions remain separate', 'incomplete', 'Historical checks never replace required live verification', 'Never reconstruct approval'):
            self.assertIn(term, policy)

    def test_gaps_and_disclosure_do_not_expand_approval(self):
        policy = (SKILLS/'review-job/references/experience-gaps.md').read_text()
        for term in ('one focused neutral question', 'keep the unknown', 'does not approve disclosure', 'Stretch applications'):
            self.assertIn(term, policy)

    def test_production_and_submission_boundaries(self):
        policy = (SKILLS/'produce-files/SKILL.md').read_text()
        for term in ('Make no substantive wording changes', 'Ready to apply', 'Do not record `Applied` until the user confirms submission', 'Do not rasterize pages', 'Do not load historical writing libraries'):
            self.assertIn(term, policy)

    def test_live_trial_is_deferred_and_missing_capabilities_are_explicit(self):
        checklist = self.read('docs/LIVE_SETUP_CHECKLIST.md')
        self.assertIn('not observed, never passed', checklist)
        self.assertIn('remain untested until observed live', checklist)
        setup = (SKILLS/'setup-job-search/SKILL.md').read_text()
        self.assertIn('If no Python runtime exists', setup)
        self.assertIn('Do not infer capabilities from plan alone', setup)
        self.assertIn('report the incomplete migration', setup)

    def test_optional_depth_does_not_add_default_overhead(self):
        decisions = self.read('docs/OPTIONAL_FEATURE_DECISIONS.md')
        for term in ('Independent drafting reviewer', 'Full first-to-final learning records', 'Workspace schema remains 3', 'never replaces existing profiles'):
            self.assertIn(term, decisions)
        drafting = (SKILLS/'draft-application/SKILL.md').read_text()
        self.assertIn('Do not repeat an unchanged full evaluation', drafting)
        self.assertIn('without a separate reviewer', drafting)
        optional = (SKILLS/'draft-application/references/optional-depth.md').read_text()
        self.assertIn('same context is not independent', optional)
        self.assertIn('never career facts or production wording', optional)

    def test_generic_voice_and_scope_are_not_candidate_specific(self):
        policy = (SKILLS/'draft-application/references/evidence-led-bullets.md').read_text()
        self.assertIn('No separate reviewer or decision-card file is required', policy)
        self.assertIn('candidate-specific', policy)
        self.assertIn('Never invent metrics', policy)
