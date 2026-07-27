"""Agent-style orchestration for the Singapore MNC capstone project.

The project can be presented as an AI agent because it decomposes the task into
tools, calls those tools in order, and produces a decision-ready strategy brief.
"""

from __future__ import annotations

import json
from pathlib import Path

from advanced_ml_engine import analyze_portfolio, load_profiles
from risk_engine import RiskProfile, ai_prompt, recommendations, weighted_risk_score


DATA_PATH = Path(__file__).parent / "data" / "risk_profiles.csv"


def tool_load_industry_profile(industry: str) -> RiskProfile:
    profiles = load_profiles(DATA_PATH)
    for profile in profiles:
        if profile.industry.lower() == industry.lower():
            return profile
    choices = ", ".join(profile.industry for profile in profiles)
    raise ValueError(f"Industry not found. Choose one of: {choices}")


def tool_calculate_risk(profile: RiskProfile) -> dict[str, object]:
    return {
        "industry": profile.industry,
        "risk_score": weighted_risk_score(profile),
        "actions": recommendations(profile),
    }


def tool_get_policy_context() -> list[str]:
    return [
        "EDB positions Singapore as a leading regional headquarters base for global growth.",
        "MOM Employment Pass eligibility requires qualifying salary and, unless exempted, COMPASS.",
        "IRAS Refundable Investment Credit supports approved high-value activities including headquarters, centres of excellence, R&D, digital services, and supply-chain management.",
        "MTI 2Q 2026 advance estimates show strong growth, but external shocks still require scenario planning.",
    ]


def tool_generate_llm_prompt(profile: RiskProfile) -> str:
    return ai_prompt(profile)


def run_agent(industry: str) -> dict[str, object]:
    profile = tool_load_industry_profile(industry)
    portfolio = analyze_portfolio(DATA_PATH)
    selected = next(item for item in portfolio if item["industry"] == profile.industry)

    return {
        "agent_goal": "Recommend a Singapore MNC risk mitigation and growth strategy.",
        "tool_trace": [
            "tool_load_industry_profile",
            "tool_calculate_risk",
            "advanced_ml_engine.analyze_portfolio",
            "tool_get_policy_context",
            "tool_generate_llm_prompt",
        ],
        "policy_context": tool_get_policy_context(),
        "risk_result": tool_calculate_risk(profile),
        "advanced_analysis": selected,
        "llm_ready_prompt": tool_generate_llm_prompt(profile),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Singapore MNC strategy agent.")
    parser.add_argument("--industry", default="Technology and AI services")
    args = parser.parse_args()
    print(json.dumps(run_agent(args.industry), indent=2))
