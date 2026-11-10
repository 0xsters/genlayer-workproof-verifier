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
