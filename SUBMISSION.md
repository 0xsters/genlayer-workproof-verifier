# GenLayer Portal submission, ready to paste

Form: Submit Contribution (portal.genlayer.foundation)

- Contribution Type: Builder
- Category: Intelligent Contracts
- Contribution Date: 11/10/2026
- Title: WorkProof Verifier: a GenLayer Intelligent Contract for consensus-graded work acceptance
- Evidence URL: https://github.com/0xsters/genlayer-workproof-verifier

## Notes / Description (paste exactly, under the 1,000 character limit)

WorkProof Verifier is a reusable GenLayer Intelligent Contract primitive for checking submitted work against written acceptance criteria. A submitter registers a task, its criteria, an evidence URL, and a pass score. Validators independently fetch the evidence and grade it; the verdict is stored only when validators agree under a custom equivalence rule: the verdict must match exactly, the score must be within 15 points, and the criteria counts within 1. The rule was strengthened after steward feedback: an accepted result must score at or above pass_score and a rejected result below it, on both the leader's and the validator's side, and the persisted criteria counts must be non-negative with criteria_met never above criteria_total. It includes a double-resolution guard, input validation, readable source, 18 passing direct tests, and full documentation, so other builders can reuse it for bounties, contributions, and agent marketplaces.

## Deployed contract (redeployed 2026-11-16, corrected version)

- Network: GenLayer Studionet (chain 61999)
- Contract address: 0x8f80766C3297476543fCFf42a1562AbCa7dd4961
- Deploy transaction: 0x64ffddbed8314efda83866f18a272108fd50f3bff40beaa7ed5d8373c66546ba (verified live on the Studio explorer 2026-11-16 13:39 WIB: status FINALIZED, GenVM result SUCCESS, consensus Accepted; created 2026-11-16 09:48:39)
- Explorer (contract): https://explorer-studio.genlayer.com/address/0x8f80766C3297476543fCFf42a1562AbCa7dd4961
- Deployed by the owner in GenLayer Studio on 2026-11-16 from the corrected contract (GitHub commit 0eff9f9). The previous deployment (0xD974a24a033714a64987539EF13986f63E51d426, tx 0x16685e0cbe54741822b9adfa66e57294d1c1b5387c4ebf00ea6e3b2a9fafe2ee) was the old version and is superseded.
- Note: deployment used Studionet because Studio's Bradbury network node currently rejects every contract schema (verified with the official minimal example as well); Bradbury Phase 2 publishes no public GenLayer node RPC in the docs.

Portal evidence to attach:
1. Type "GitHub Repository": https://github.com/0xsters/genlayer-workproof-verifier
2. Type "GenLayer Explorer Contract": https://explorer-studio.genlayer.com/address/0x8f80766C3297476543fCFf42a1562AbCa7dd4961

## Verification evidence (already run locally)

- `genvm-lint check contracts/work_proof_verifier.py`: lint passed (3 checks), validation passed, contract WorkProofVerifier, 4 methods (2 view, 2 write).
- `pytest tests/direct -v`: 18 passed (9 original tests + 9 validator tests added for the steward request: accepted-below-pass, rejected-above-pass, scores straddling pass_score, criteria total mismatch, criteria_met above total, negative criteria_met, and two tolerance happy paths).
- The 6 new rejection tests were run against the ORIGINAL contract first and failed there, proving they exercise the fix; they pass on the corrected contract.

## Redeploy done (2026-11-16)

- The corrected contract was redeployed by the owner in GenLayer Studio on 2026-11-16 at 0x8f80766C3297476543fCFf42a1562AbCa7dd4961. The deployed source matches this corrected repository (GitHub commit 0eff9f9). Deploy transaction hash filled in above (verified live on the explorer). The portal reply can be sent now.
