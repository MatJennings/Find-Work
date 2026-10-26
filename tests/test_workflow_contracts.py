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

class WritingQualityContracts(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding='utf-8')

    def test_default_letter_craft_is_single_context(self):
        craft = (SKILLS/'draft-application/references/cover-letter-craft.md').read_text(encoding='utf-8')
        for term in ('Argument before proof', 'three genuinely different opening theses', 'Provability',
                     'One proof point', 'Read-aloud check', 'no extra agents', 'not an independent review',
                     'check_letter_clarity.py'):
            self.assertIn(term, craft)
        drafting = (SKILLS/'draft-application/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references/cover-letter-craft.md', drafting)
        self.assertIn('references/opening-quality.md', drafting)

    def test_opening_quality_tests(self):
        opening = (SKILLS/'draft-application/references/opening-quality.md').read_text(encoding='utf-8')
        for term in ('Concrete payoff', 'One thread', 'Not the posting', 'Banned openings', 'Cold read', 'no separate reviewer'):
            self.assertIn(term, opening)

    def test_deep_letter_review_is_opt_in_and_bounded(self):
        deep = (SKILLS/'draft-application/references/deep-letter-review.md').read_text(encoding='utf-8')
        for term in ('Off by default', 'not expected to fit a free plan', 'same-context review is never independent',
                     'END OF PACKET FILE', 'at most two revisions', 'Never rotate agents', 'never approved wording'):
            self.assertIn(term, deep)
        prefs = self.read('plugins/find-work/assets/workspace/profile/cover_letter_preferences.md')
        self.assertIn('Deep letter review: off unless turned on', prefs)
        decisions = self.read('docs/OPTIONAL_FEATURE_DECISIONS.md')
        self.assertIn('Deep letter review', decisions)

    def test_skills_do_not_reread_loaded_instructions(self):
        for name in ('find-jobs', 'review-job', 'draft-application', 'produce-files', 'build-career-foundation'):
            text = (SKILLS/name/'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('already-loaded `AGENTS.md` without re-reading it', text, name)
        workspace = self.read('plugins/find-work/assets/workspace/AGENTS.md')
        self.assertIn('Do not re-read it', workspace)

    def test_search_and_production_rules(self):
        find = (SKILLS/'find-jobs/SKILL.md').read_text(encoding='utf-8')
        for term in ('not title alone', 'hard rules as screens', 'make the title a link'):
            self.assertIn(term, find)
        produce = (SKILLS/'produce-files/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('never let a bullet split across pages', produce)
        self.assertIn('propose the smallest fix for approval', produce)

    def test_form_defaults_require_confirmation(self):
        answers = self.read('plugins/find-work/assets/workspace/sources/authoritative/approved_application_answers.md')
        for term in ('explicitly confirms', 'Leave a question blank until confirmed', 'never establishes citizenship'):
            self.assertIn(term, answers)
