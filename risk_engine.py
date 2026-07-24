"""Risk scoring engine for the Singapore MNC Risk & Strategy Analyzer."""

from __future__ import annotations

from dataclasses import dataclass


RISK_WEIGHTS = {
    "cost_pressure": 0.25,
    "talent_labour": 0.20,
    "competition_growth": 0.18,
    "regulation_compliance": 0.17,
    "global_strategy": 0.20,
}


@dataclass(frozen=True)
class RiskProfile:
    industry: str
    cost_pressure: float
    talent_labour: float
    competition_growth: float
    regulation_compliance: float
    global_strategy: float
    growth_potential: float
    automation_readiness: float
    regional_expansion_fit: float


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def weighted_risk_score(profile: RiskProfile) -> float:
    score = 0.0
    for field_name, weight in RISK_WEIGHTS.items():
        score += clamp_score(getattr(profile, field_name)) * weight
    return round(score, 1)


def risk_band(score: float) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def strategic_position(profile: RiskProfile) -> str:
    risk = weighted_risk_score(profile)
    if profile.growth_potential >= 78 and risk < 70:
        return "Invest and scale selectively"
    if profile.growth_potential >= 78:
        return "Keep Singapore as control hub, scale regionally"
    if risk >= 70:
        return "Stabilise costs before expansion"
    return "Optimise and expand through partnerships"


def recommendations(profile: RiskProfile) -> list[str]:
    actions: list[str] = []

    if profile.cost_pressure >= 70:
        actions.append(
            "Move routine back-office work to lower-cost regional shared-service locations while keeping leadership, treasury, compliance, and innovation in Singapore."
        )
    else:
        actions.append(
            "Keep Singapore operations lean through hybrid work, vendor consolidation, and productivity tracking."
        )

    if profile.talent_labour >= 68:
        actions.append(
            "Reduce hiring pressure through upskilling, university partnerships, internal mobility, and automation of repetitive roles."
        )

    if profile.competition_growth >= 60:
        actions.append(
            "Use Singapore as an ASEAN launchpad instead of relying on the small domestic market; enter new markets through distributors, joint ventures, or phased pilots."
        )

    if profile.regulation_compliance >= 70:
        actions.append(
            "Create a compliance operating model covering data privacy, employment pass planning, tax, sector rules, audit cadence, and board reporting."
        )

    if profile.global_strategy >= 65:
        actions.append(
            "Run quarterly scenario planning for tariffs, external demand shocks, energy costs, geopolitics, and supply-chain disruption."
        )

    if profile.automation_readiness >= 75:
        actions.append(
            "Prioritise AI-enabled workflows such as finance reporting, customer support triage, demand forecasting, and compliance monitoring."
        )

    return actions


def ai_prompt(profile: RiskProfile) -> str:
    """Prompt template for optional LLM-based recommendation generation."""
    return (
        "Act as a Singapore regional strategy consultant. "
        f"Industry: {profile.industry}. "
        f"Risk score: {weighted_risk_score(profile)} ({risk_band(weighted_risk_score(profile))}). "
        "Create a concise action plan using this strategy: keep Singapore as a high-value hub, "
        "move routine work to cost-effective locations, invest in talent and technology, "
        "strengthen compliance, and expand regionally through partnerships."
    )
