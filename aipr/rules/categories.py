from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryDefinition:
    key: str
    name: str
    points: int


CATEGORIES = [
    CategoryDefinition("business", "Business value and workflow fit", 10),
    CategoryDefinition("data", "Data readiness", 10),
    CategoryDefinition("rag", "RAG / retrieval quality", 10),
    CategoryDefinition("model_architecture", "Model architecture", 10),
    CategoryDefinition("governance", "Governance and security", 15),
    CategoryDefinition("human_in_the_loop", "Human-in-the-loop design", 10),
    CategoryDefinition("evals", "Evals and quality assurance", 15),
    CategoryDefinition("observability", "Observability and cost control", 10),
    CategoryDefinition("operations", "Operations and ownership", 5),
    CategoryDefinition("adoption", "Adoption and enablement", 5),
]
