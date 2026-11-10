# GenLayer Portal submission, ready to paste

Form: Submit Contribution (portal.genlayer.foundation)

- Contribution Type: Builder
- Category: Intelligent Contracts
- Contribution Date: 11/10/2026
- Title: WorkProof Verifier: a GenLayer Intelligent Contract for consensus-graded work acceptance
- Evidence URL: https://github.com/0xsters/genlayer-workproof-verifier

## Notes / Description (paste exactly, under the 1,000 character limit)

WorkProof Verifier is a reusable GenLayer Intelligent Contract primitive for checking submitted work against written acceptance criteria. A submitter registers a task, its criteria, an evidence URL, and a pass score. Validators independently fetch the evidence and grade it; the verdict is stored only when validators agree under a custom equivalence rule: the verdict must match exactly, the score must be within 15 points, and the criteria met count within 1. It uses real GenLayer consensus logic: web rendering, structured LLM grading, and run_nondet_unsafe with a custom validator. It includes a double-resolution guard, input validation, readable source, 9 passing direct tests, and full documentation, so other builders can reuse it for bounties, contributions, and agent marketplaces.

## Deployed contract (added 2026-11-10)

- Network: GenLayer Studionet (chain 61999), deployed from 0x11B9dd6d3129Eb740011b1A948aDCbCB67758a10
- Contract address: 0xD974a24a033714a64987539EF13986f63E51d426
- Deploy transaction: 0x16685e0cbe54741822b9adfa66e57294d1c1b5387c4ebf00ea6e3b2a9fafe2ee
- Explorer (contract): https://explorer-studio.genlayer.com/address/0xD974a24a033714a64987539EF13986f63E51d426
- Verified on-chain by reading the code and schema back from the Studio node: the stored code is this contract and the schema lists create_task, resolve_task, get_task, and total_tasks.
- Note: deployment used Studionet because Studio's Bradbury network node currently rejects every contract schema (verified with the official minimal example as well); Bradbury Phase 2 publishes no public GenLayer node RPC in the docs.

Portal evidence to attach:
1. Type "GitHub Repository": https://github.com/0xsters/genlayer-workproof-verifier
2. Type "GenLayer Explorer Contract": https://explorer-studio.genlayer.com/address/0xD974a24a033714a64987539EF13986f63E51d426

## Verification evidence (already run locally)

- `genvm-lint check contracts/work_proof_verifier.py`: lint passed (3 checks), validation passed, contract WorkProofVerifier, 4 methods (2 view, 2 write).
- `pytest tests/direct -v`: 9 passed.
