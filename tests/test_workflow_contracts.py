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

    def test_generic_voice_and_scope_are_not_candidate_specific(self):
        policy = (SKILLS/'draft-application/references/evidence-led-bullets.md').read_text()
        self.assertIn('No separate reviewer or decision-card file is required', policy)
        self.assertIn('candidate-specific', policy)
        self.assertIn('Never invent metrics', policy)
