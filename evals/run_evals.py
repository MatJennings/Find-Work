"""Run maintained deterministic behavioral contracts, without model/API calls."""
import sys
import unittest
from pathlib import Path

root = Path(__file__).resolve().parents[1]
suite = unittest.TestSuite()
for pattern in ('test_workflow_contracts.py', 'test_lookup.py', 'test_context_retrieval.py', 'test_privacy_contracts.py'):
    suite.addTests(unittest.defaultTestLoader.discover(str(root / 'tests'), pattern=pattern))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
