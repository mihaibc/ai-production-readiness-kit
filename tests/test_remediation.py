from pathlib import Path

from aipr.remediation import effort_for, remediation_items, why_it_matters
from aipr.scoring import assess
from aipr.validation import load_usecase


def test_remediation_items_include_stable_metadata() -> None:
    assessment = assess(load_usecase(Path("examples/supplier-risk-intake-screener/usecase.yaml")))

    items = remediation_items(assessment)

    assert items
    assert set(items[0]) == {
        "priority",
        "severity",
        "category",
        "effort",
        "action",
        "why_it_matters",
    }
    assert items[0]["priority"] == 1
    assert items[0]["severity"] == "critical"
    assert items[0]["effort"] in {"medium", "high"}
    assert items[0]["why_it_matters"]


def test_remediation_effort_is_category_based() -> None:
    assert effort_for("Governance and security", "critical") == "high"
    assert effort_for("Human-in-the-loop", "critical") == "high"
    assert effort_for("Adoption and enablement", "warning") == "low"
    assert effort_for("Operations and ownership", "critical") == "medium"


def test_remediation_rationale_falls_back_to_general() -> None:
    assert why_it_matters("Unexpected category") == "Improves readiness before expanding production use."
