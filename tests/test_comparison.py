from pathlib import Path

from aipr.comparison import compare_payload
from aipr.scoring import assess
from aipr.validation import load_usecase


def test_compare_payload_includes_scores_deltas_and_finding_changes() -> None:
    before = assess(load_usecase(Path("examples/supplier-risk-intake-screener/usecase.yaml")))
    after = assess(load_usecase(Path("examples/research-knowledge-base-curator/usecase.yaml")))

    payload = compare_payload(before, after)

    assert payload["before"]["name"] == "Supplier Risk Intake Screener"
    assert payload["after"]["name"] == "Research Knowledge Base Curator"
    assert payload["score_delta"] > 0
    assert len(payload["categories"]) == 10
    assert {"key", "category", "before", "after", "delta"} <= set(payload["categories"][0])
    assert payload["resolved_findings"]
