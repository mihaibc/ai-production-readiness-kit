from pathlib import Path

from aipr.gates import evaluate_gate
from aipr.scoring import assess
from aipr.validation import load_usecase


def test_gate_passes_without_threshold_or_critical_requirement() -> None:
    assessment = assess(load_usecase(Path("examples/document-ingestion-quality-monitor/usecase.yaml")))

    gate = evaluate_gate(assessment)

    assert gate["passed"] is True
    assert gate["failures"] == []


def test_gate_fails_score_threshold() -> None:
    assessment = assess(load_usecase(Path("examples/document-ingestion-quality-monitor/usecase.yaml")))

    gate = evaluate_gate(assessment, min_score=95)

    assert gate["passed"] is False
    assert gate["failures"] == ["Score 73 is below required minimum 95."]


def test_gate_fails_on_unresolved_critical_findings() -> None:
    assessment = assess(load_usecase(Path("examples/supplier-risk-intake-screener/usecase.yaml")))

    gate = evaluate_gate(assessment, fail_on_critical=True)

    assert gate["passed"] is False
    assert "critical finding" in str(gate["failures"][0])
