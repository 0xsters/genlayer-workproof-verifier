# GenLayer Portal submission, ready to paste

Form: Submit Contribution (portal.genlayer.foundation)

- Contribution Type: Builder
- Category: Intelligent Contracts
- Contribution Date: 11/10/2026
- Title: WorkProof Verifier: a GenLayer Intelligent Contract for consensus-graded work acceptance
- Evidence URL: https://github.com/0xsters/genlayer-workproof-verifier

## Notes / Description (paste exactly, under the 1,000 character limit)

WorkProof Verifier is a reusable GenLayer Intelligent Contract primitive for checking submitted work against written acceptance criteria. A submitter registers a task, its criteria, an evidence URL, and a pass score. Validators independently fetch the evidence and grade it; the verdict is stored only when validators agree under a custom equivalence rule: the verdict must match exactly, the score must be within 15 points, and the criteria met count within 1. It uses real GenLayer consensus logic: web rendering, structured LLM grading, and run_nondet_unsafe with a custom validator. It includes a double-resolution guard, input validation, readable source, 9 passing direct tests, and full documentation, so other builders can reuse it for bounties, contributions, and agent marketplaces.

## Verification evidence (already run locally)

- `genvm-lint check contracts/work_proof_verifier.py`: lint passed (3 checks), validation passed, contract WorkProofVerifier, 4 methods (2 view, 2 write).
- `pytest tests/direct -v`: 9 passed.
