import json


CRITERIA = (
    "1. The repository contains a Python contract file. "
    "2. The README explains how to run the tests. "
    "3. The test suite passes."
)


def _deploy(direct_deploy):
    return direct_deploy("contracts/work_proof_verifier.py")


def _create(contract):
    return contract.create_task(
        "Ship the demo contract",
        CRITERIA,
        "https://example.com/work/demo",
        70,
    )


def test_create_and_read(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    task_id = _create(contract)
    assert task_id == 0
    assert contract.total_tasks() == 1

    record = json.loads(contract.get_task(0))
    assert record["title"] == "Ship the demo contract"
    assert record["criteria"] == CRITERIA
    assert record["evidence_url"] == "https://example.com/work/demo"
    assert record["pass_score"] == 70
    assert record["status"] == "open"
    assert record["verdict"] is None


def test_resolve_accepted(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice
    _create(contract)

    direct_vm.mock_web(
        r".*example\.com/work/demo.*",
        {
            "status": 200,
            "body": "<html><body>Contract file, README, and 8 passing tests.</body></html>",
        },
    )
    direct_vm.mock_llm(
        r".*work acceptance reviewer.*",
        json.dumps(
            {
                "verdict": "accepted",
                "score": 92,
                "criteria_met": 3,
                "criteria_total": 3,
                "summary": "The evidence shows all three criteria satisfied.",
            }
        ),
    )

    contract.resolve_task(0)

    record = json.loads(contract.get_task(0))
    assert record["status"] == "resolved"
    assert record["verdict"] == "accepted"
    assert record["score"] == 92
    assert record["criteria_met"] == 3
    assert record["criteria_total"] == 3


def test_resolve_rejected(direct_vm, direct_deploy, direct_bob):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_bob
    _create(contract)

    direct_vm.mock_web(
        r".*example\.com/work/demo.*",
        {
            "status": 200,
            "body": "<html><body>Empty placeholder page.</body></html>",
        },
    )
    direct_vm.mock_llm(
        r".*work acceptance reviewer.*",
        json.dumps(
            {
                "verdict": "rejected",
                "score": 10,
                "criteria_met": 0,
                "criteria_total": 3,
                "summary": "The evidence page shows none of the required work.",
            }
        ),
    )

    contract.resolve_task(0)

    record = json.loads(contract.get_task(0))
    assert record["verdict"] == "rejected"
    assert record["score"] == 10
    assert record["criteria_met"] == 0


def test_create_rejects_short_criteria(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("too short"):
        contract.create_task(
            "Ship the demo contract",
            "do it well",
            "https://example.com/work/demo",
            70,
        )


def test_create_rejects_bad_url(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("must be an http"):
        contract.create_task(
            "Ship the demo contract",
            CRITERIA,
            "ftp://example.com/work/demo",
            70,
        )


def test_create_rejects_bad_pass_score(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("between 1 and 100"):
        contract.create_task(
            "Ship the demo contract",
            CRITERIA,
            "https://example.com/work/demo",
            0,
        )


def test_resolve_unknown_task_reverts(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("Unknown task id"):
        contract.resolve_task(999)


def test_get_unknown_task_reverts(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("Unknown task id"):
        contract.get_task(999)


def test_resolve_twice_reverts(direct_vm, direct_deploy, direct_alice):
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice
    _create(contract)

    direct_vm.mock_web(
        r".*example\.com/work/demo.*",
        {
            "status": 200,
            "body": "<html><body>Contract file, README, and 8 passing tests.</body></html>",
        },
    )
    direct_vm.mock_llm(
        r".*work acceptance reviewer.*",
        json.dumps(
            {
                "verdict": "accepted",
                "score": 92,
                "criteria_met": 3,
                "criteria_total": 3,
                "summary": "The evidence shows all three criteria satisfied.",
            }
        ),
    )

    contract.resolve_task(0)

    with direct_vm.expect_revert("already resolved"):
        contract.resolve_task(0)


# --- Validator checks (steward request, GenLayer action needed b80d7319) ---
#
# In direct-test mode gl.vm.run_nondet_unsafe runs only the leader and
# captures the validator; consensus itself is exercised explicitly with
# direct_vm.run_validator(). Each test below resolves a task with a
# mocked "validator's own" grading, then feeds a crafted leader result
# to the captured validator and asserts its True/False answer.
# pass_score is 70 in every test (see _create).


def _grading(verdict, score, met, total):
    return {
        "verdict": verdict,
        "score": score,
        "criteria_met": met,
        "criteria_total": total,
        "summary": "Mocked grading.",
    }


def _capture_validator(direct_vm, direct_deploy, direct_alice, own_grading):
    """Create a task and resolve it with the mocked grading, so the
    contract's validator is captured for direct_vm.run_validator()."""
    contract = _deploy(direct_deploy)
    direct_vm.sender = direct_alice
    _create(contract)
    direct_vm.mock_web(
        r".*example\.com/work/demo.*",
        {
            "status": 200,
            "body": "<html><body>Contract file, README, and 8 passing tests.</body></html>",
        },
    )
    direct_vm.mock_llm(
        r".*work acceptance reviewer.*",
        json.dumps(own_grading),
    )
    contract.resolve_task(0)
    return contract


def test_validator_rejects_accepted_below_pass(
    direct_vm, direct_deploy, direct_alice
):
    # Steward's exact example: pass_score 70, leader stores accepted
    # with score 55 while the validator independently obtains 70. The
    # old 15-point tolerance alone accepted this (|55 - 70| == 15).
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 70, 3, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 55, 3, 3))
        is False
    )


def test_validator_rejects_rejected_above_pass(
    direct_vm, direct_deploy, direct_alice
):
    # Mirror image: a rejected leader result carrying a score above
    # pass_score must not be stored either.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("rejected", 75, 1, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("rejected", 85, 1, 3))
        is False
    )


def test_validator_rejects_scores_straddling_pass_score(
    direct_vm, direct_deploy, direct_alice
):
    # Leader 72 and validator 68 are within the 15-point tolerance and
    # agree on "accepted", but the scores land on opposite sides of
    # pass_score 70, so there is no consensus about passing.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 68, 3, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 72, 3, 3))
        is False
    )


def test_validator_accepts_matching_accepted_result(
    direct_vm, direct_deploy, direct_alice
):
    # Happy path must keep working: both sides accepted above pass.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 90, 3, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 92, 3, 3))
        is True
    )


def test_validator_accepts_matching_rejected_result(
    direct_vm, direct_deploy, direct_alice
):
    # Happy path for rejection: both sides rejected below pass.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("rejected", 60, 0, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("rejected", 55, 0, 3))
        is True
    )


def test_validator_rejects_criteria_total_mismatch(
    direct_vm, direct_deploy, direct_alice
):
    # The old validator never checked criteria_total at all. A leader
    # total 2 points away from the validator's own total must be
    # rejected, mirroring the +-1 tolerance on criteria_met.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 92, 3, 5)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 92, 3, 3))
        is False
    )


def test_validator_rejects_criteria_met_above_total(
    direct_vm, direct_deploy, direct_alice
):
    # Persisted counts must be internally consistent: criteria_met can
    # never exceed criteria_total.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 92, 3, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 92, 3, 2))
        is False
    )


def test_validator_rejects_negative_criteria_met(
    direct_vm, direct_deploy, direct_alice
):
    # Counts are bounded below at zero; -1 is within 1 of the
    # validator's own 0, so only the explicit bound catches it.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 92, 0, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 92, -1, 3))
        is False
    )


def test_validator_accepts_criteria_counts_within_tolerance(
    direct_vm, direct_deploy, direct_alice
):
    # Counts at the +-1 tolerance edge on both met and total must
    # still pass, so the fix does not make consensus unreachable.
    _capture_validator(
        direct_vm, direct_deploy, direct_alice, _grading("accepted", 92, 2, 3)
    )
    assert (
        direct_vm.run_validator(leader_result=_grading("accepted", 92, 3, 4))
        is True
    )
