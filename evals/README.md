# Behavioral contracts

Run `python evals/run_evals.py` from the starter root. The suite combines actual synthetic helper behavior with checks of maintained workflow instructions. It guards identity, warning fallback, truthful evidence, disclosure, approval, and application state. It does not run a simulated job-search conversation or establish live model performance, writing quality, or Free-account usage.

When observable workflow behavior changes, revise or add a case and its tests. Do not weaken cases to hide a regression. Tests live in `tests/test_workflow_contracts.py`, `tests/test_lookup.py` and `tests/test_letter_clarity.py`.
