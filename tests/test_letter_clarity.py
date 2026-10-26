import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('check_letter_clarity', ROOT / 'plugins/find-work/scripts/check_letter_clarity.py')
clarity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(clarity)

BODY = ' '.join(['Teams ship faster when the problem is clear before the work starts.'] * 20)
LETTER = f"Re Product Lead\n\nDear Hiring Team,\n\n{BODY}\n\nSincerely,\nSample Candidate\n"


class LetterClarity(unittest.TestCase):
    def test_clean_letter_passes(self):
        errors, warnings, stats = clarity.check(LETTER)
        self.assertEqual(errors, [])
        self.assertEqual(stats['body_paragraphs'], 1)

    def test_stock_phrase_and_ceiling_are_errors(self):
        errors, _, _ = clarity.check(LETTER.replace('Teams ship', 'I am excited to apply. Teams ship', 1))
        self.assertTrue(any('excited to apply' in e for e in errors))
        errors, _, _ = clarity.check(LETTER, ceiling=100)
        self.assertTrue(any('ceiling' in e for e in errors))

    def test_punctuation_only_checked_when_chosen(self):
        letter = LETTER.replace('clear before', 'clear; before', 1).replace('Re Product', 'Re: Product')
        errors, _, _ = clarity.check(letter)
        self.assertEqual(errors, [])
        errors, _, _ = clarity.check(letter, avoid=frozenset({'semicolon', 'colon'}))
        self.assertTrue(any('Semicolon' in e for e in errors))
        self.assertTrue(any('Colon' in e for e in errors))

    def test_resume_overlap_warns(self):
        text = ("# Resume\n\nLed a team that rebuilt the onboarding workflow for enterprise customers in one quarter.\n\n"
                "# Cover letter\n\nDear Hiring Team,\n\nI led a team that rebuilt the onboarding workflow for enterprise customers in one quarter.\n\nSincerely,\n")
        _, warnings, _ = clarity.check(text)
        self.assertTrue(any('repeat the resume' in w for w in warnings))

    def test_cli_exit_code(self):
        path = ROOT / 'tests' / '_tmp_letter.txt'
        path.write_text(LETTER.replace('Teams ship', 'A proven track record. Teams ship', 1), encoding='utf-8')
        try:
            self.assertEqual(clarity.main([str(path)]), 1)
        finally:
            path.unlink()


if __name__ == '__main__':
    unittest.main()
