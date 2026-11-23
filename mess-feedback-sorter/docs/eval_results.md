# Eval results

> **This file was generated with the offline MOCK LLM, not a real model.**
> Run `python eval_harness.py` with a real key and use that output for submission.


Run mode: **MOCK (offline fake LLM, not a real model)**, 2026-11-22 23:28

Five normal comments that are **not** in feedback_input.csv. The expected category and urgent flag were written before the run. A test passes only if both are correct (final result, after the safety net).

| # | Comment | Expected | LLM urgent (before safety net) | Final | Result |
|---|---|---|---|---|---|
| 1 | There was a plastic piece in the upma | hygiene / urgent | True | hygiene / urgent | PASS |
| 2 | Sambar was too spicy today | taste / not urgent | False | taste / not urgent | PASS |
| 3 | Only one dosa was given at breakfast today | quantity / not urgent | False | quantity / not urgent | PASS |
| 4 | The biscuit packet expiry date was yesterday | hygiene / urgent | False | hygiene / urgent | PASS |
| 5 | Dinner counter opened 15 minutes after the usual time | timing / not urgent | False | timing / not urgent | PASS |

**5 of 5 correct (100%)**

## Safety net contribution

- Test 4 ("The biscuit packet expiry date was yesterday"): the LLM said urgent = False; the safety net raised it to true (matched: expiry).

## What this does not prove

Five cases is a small test. A pass here means the tool handled these five, not that it is always right. Before the committee relies on it, check many more real comments by hand.

## My notes (write after a live run)

- Which test failed before the safety net, and why?
- What did I change?
