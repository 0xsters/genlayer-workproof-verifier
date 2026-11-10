# WorkProof Verifier

A reusable **GenLayer Intelligent Contract** primitive that grades submitted
work against written acceptance criteria, with the verdict decided by
validator consensus rather than a single reviewer.

Someone registers a task with a title, plain-language acceptance criteria, a
public evidence URL (a repository, a document, a deployed page), and a pass
score. Anyone can then resolve the task: the contract fetches the evidence
page, asks an LLM to grade it criterion by criterion, and stores the outcome
only after independent validators reproduce and accept the result through the
Equivalence Principle.

That makes the contract a shared acceptance layer for bounties, contribution
programs, and agent marketplaces: the party offering work and the party doing
it both point at the same on-chain verdict instead of arguing over
screenshots.

- Contract: `contracts/work_proof_verifier.py`
- Tests: `tests/direct/test_work_proof_verifier.py`

## Why GenLayer

A traditional smart contract cannot do this job. It cannot read a web page,
it cannot interpret prose criteria like "the README explains how to run the
tests", and it cannot judge whether evidence satisfies them. GenLayer
Intelligent Contracts run Python with two extra capabilities:

| Capability | API used here |
| --- | --- |
| Fetch and render a live web page | `gl.nondet.web.render(url, mode="html")` |
| Ask an LLM for structured output | `gl.nondet.exec_prompt(prompt, response_format="json")` |
| Reach consensus on non-deterministic output | `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)` |

## How it works

```
create_task(title, criteria, evidence_url, pass_score)   # deterministic
        |
        v
resolve_task(task_id)                                    # non-deterministic block
        |
        |-- evaluate() -> render evidence, prompt LLM, normalize result
        |
        |-- validate() -> re-run evaluate(), compare:
        |                   verdict must match exactly
        |                   score must be within 15 points
        |                   criteria_met must be within 1
        |
        v
store {status: "resolved", verdict, score, criteria_met, criteria_total, summary}
```

Two design details matter:

1. **All `gl.nondet.*` calls live inside the non-deterministic block.**
   Storage writes happen after consensus, in deterministic code, so no node
   can write its own version of the verdict before the network agrees.
2. **The verdict is a fixed enum** (`accepted` / `rejected` /
   `inconclusive`) with a bounded integer score and explicit criteria
   counts. Free-form reasoning is allowed to differ between validators; the
   decision is not.

A task can be resolved exactly once. The double-resolution guard is covered
by a dedicated test.

## The record

`get_task(task_id)` returns the stored record as JSON:

```json
{
  "title": "Ship the demo contract",
  "criteria": "1. ... 2. ... 3. ...",
  "evidence_url": "https://example.com/work/demo",
  "pass_score": 70,
  "submitter": "0x...",
  "status": "resolved",
  "verdict": "accepted",
  "score": 92,
  "criteria_met": 3,
  "criteria_total": 3,
  "summary": "The evidence shows all three criteria satisfied."
}
```

## Prerequisites

- Python 3.12+
- Dependencies from `requirements.txt` (`genlayer-test`, `genvm-linter`)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 1. Lint the contract

```bash
genvm-lint check contracts/work_proof_verifier.py
```

### 2. Run the tests

Direct-mode tests run the contract in memory with the web and LLM calls
mocked, so they need no server and no network:

```bash
pytest tests/direct -v
```

The suite covers task creation and reading, an accepted resolution, a
rejected resolution, input validation (short criteria, non-HTTP evidence
URL, pass score out of range), unknown task ids, and the double-resolution
guard.

Verified locally on 2026-11-10: `genvm-lint check` passed (3 checks,
validation passed, 4 methods: 2 view, 2 write) and the full direct suite
passed, 9 of 9 tests.

> Troubleshooting: if direct tests fail with `HTTP 404 ... genvm-universal.tar.xz`,
> the test SDK is looking for a release asset name that recent genvm
> releases no longer publish. Copy the tarball the linter already cached
> into the direct-test cache and run the tests again:
> `mkdir -p ~/.cache/gltest-direct && cp ~/.cache/genvm-linter/genvm-universal-*.tar.xz ~/.cache/gltest-direct/genvm-universal.tar.xz`

### 3. Deploy

The zero-setup path is [GenLayer Studio](https://studio.genlayer.com):
paste `contracts/work_proof_verifier.py` and deploy. The constructor takes
no arguments. The CLI path works too, with the GenLayer CLI and a local
Studio running (`genlayer init && genlayer up`).

### 4. Try it

1. Call `create_task("Ship the demo contract", "1. ... 2. ... 3. ...", "https://example.com/work/demo", 70)`. It returns a task id starting at `0`.
2. Call `resolve_task(0)`.
3. Call `get_task(0)` and read the verdict.

## Prompt injection note

The evidence page is untrusted input: a worker could hide text in it that
tries to instruct the grading model. The grading prompt wraps the task, the
criteria, and the evidence in explicit tags and instructs the model to treat
everything inside them as data only, never as instructions. A production
deployment would harden this further (evidence allowlists, multiple evidence
sources, a minimum evidence length), and the contract is written so those
checks can be added inside `evaluate()` without changing the storage schema.

## Ideas to extend

- Add an appeal flow: a second evidence URL triggers one re-grade.
- Support several evidence URLs per task and require agreement across them.
- Add `@gl.public.write.payable` so resolving a task can carry a bounty that
  is released on an `accepted` verdict.

## License

MIT
