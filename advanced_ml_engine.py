"""Advanced ML-style analytics for the Singapore MNC Risk & Strategy Analyzer.

This module is intentionally dependency-light. It uses numpy instead of
scikit-learn so the project can run on machines where ML packages are not
installed, while still demonstrating real modelling ideas:

- weighted risk scoring
- k-means segmentation
- Monte Carlo stress testing
- contribution-based explainability
- scenario-based strategy selection
"""

from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

import numpy as np

from risk_engine import RISK_WEIGHTS, RiskProfile, recommendations, risk_band, weighted_risk_score


FEATURES = [
    "cost_pressure",
    "talent_labour",
    "competition_growth",
    "regulation_compliance",
    "global_strategy",
    "growth_potential",
    "automation_readiness",
    "regional_expansion_fit",
]

RISK_FEATURES = list(RISK_WEIGHTS)


def load_profiles(path: str | Path) -> list[RiskProfile]:
    rows: list[RiskProfile] = []
    with Path(path).open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            rows.append(
                RiskProfile(
                    industry=row["industry"],
                    cost_pressure=float(row["cost_pressure"]),
                    talent_labour=float(row["talent_labour"]),
                    competition_growth=float(row["competition_growth"]),
                    regulation_compliance=float(row["regulation_compliance"]),
                    global_strategy=float(row["global_strategy"]),
                    growth_potential=float(row["growth_potential"]),
                    automation_readiness=float(row["automation_readiness"]),
                    regional_expansion_fit=float(row["regional_expansion_fit"]),
                )
            )
    return rows


def feature_matrix(profiles: Iterable[RiskProfile], features: list[str] = FEATURES) -> np.ndarray:
    return np.array([[getattr(profile, feature) for feature in features] for profile in profiles], dtype=float)


def standardize(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    means = matrix.mean(axis=0)
    stds = matrix.std(axis=0)
    stds[stds == 0] = 1.0
    return (matrix - means) / stds, means, stds


def kmeans_segments(matrix: np.ndarray, k: int = 3, iterations: int = 50) -> tuple[np.ndarray, np.ndarray]:
    """Small deterministic k-means implementation for strategic segmentation."""
    scaled, _, _ = standardize(matrix)
    if len(scaled) < k:
        raise ValueError("k cannot be larger than the number of rows")

    centroids = scaled[:k].copy()
    labels = np.zeros(len(scaled), dtype=int)

    for _ in range(iterations):
        distances = np.linalg.norm(scaled[:, None, :] - centroids[None, :, :], axis=2)
        new_labels = distances.argmin(axis=1)
        new_centroids = centroids.copy()
        for cluster in range(k):
            members = scaled[new_labels == cluster]
            if len(members):
                new_centroids[cluster] = members.mean(axis=0)
        if np.array_equal(labels, new_labels) and np.allclose(centroids, new_centroids):
            break
        labels = new_labels
        centroids = new_centroids

    return labels, centroids


def segment_names(profiles: list[RiskProfile], labels: np.ndarray) -> dict[int, str]:
    names: dict[int, str] = {}
    for cluster in sorted(set(labels.tolist())):
        members = [profiles[index] for index, label in enumerate(labels) if label == cluster]
        avg_risk = np.mean([weighted_risk_score(member) for member in members])
        avg_growth = np.mean([member.growth_potential for member in members])
        avg_regional = np.mean([member.regional_expansion_fit for member in members])

        if avg_growth >= 80 and avg_risk < 70:
            name = "High-growth controllable risk"
        elif avg_regional >= 82:
            name = "Regional scale-out candidate"
        elif avg_risk >= 70:
            name = "Cost/compliance pressure zone"
        else:
            name = "Optimise before scaling"
        names[cluster] = name
    return names


def risk_contributions(profile: RiskProfile) -> list[dict[str, float | str]]:
    raw = asdict(profile)
    contributions = []
    for feature, weight in RISK_WEIGHTS.items():
        value = float(raw[feature])
        weighted = round(value * weight, 2)
        contributions.append(
            {
                "feature": feature,
                "score": value,
                "weight": weight,
                "weighted_points": weighted,
                "share_of_total": round(weighted / weighted_risk_score(profile), 3),
            }
        )
    return sorted(contributions, key=lambda item: float(item["weighted_points"]), reverse=True)


def monte_carlo_stress_test(
    profile: RiskProfile,
    simulations: int = 5000,
    shock_strength: float = 8.0,
    seed: int = 42,
) -> dict[str, float]:
    """Estimate future risk distribution under uncertain macro/policy shocks."""
    rng = np.random.default_rng(seed)
    base = np.array([getattr(profile, feature) for feature in RISK_FEATURES], dtype=float)
    weights = np.array([RISK_WEIGHTS[feature] for feature in RISK_FEATURES], dtype=float)

    # Correlated shocks: cost, talent, and global strategy often move together.
    shared_macro = rng.normal(0, shock_strength, size=(simulations, 1))
    idiosyncratic = rng.normal(0, shock_strength * 0.65, size=(simulations, len(base)))
    shock_vector = np.array([0.75, 0.55, 0.35, 0.25, 0.85])
    simulated_features = np.clip(base + shared_macro * shock_vector + idiosyncratic, 0, 100)
    simulated_scores = simulated_features @ weights

    return {
        "expected_score": round(float(simulated_scores.mean()), 1),
        "p10": round(float(np.percentile(simulated_scores, 10)), 1),
        "p90": round(float(np.percentile(simulated_scores, 90)), 1),
        "prob_high_risk": round(float((simulated_scores >= 70).mean()), 3),
        "prob_medium_or_high": round(float((simulated_scores >= 45).mean()), 3),
    }


def strategy_confidence(profile: RiskProfile) -> float:
    score = weighted_risk_score(profile)
    stress = monte_carlo_stress_test(profile)
    resilience = 100 - stress["prob_high_risk"] * 100
    readiness = (profile.automation_readiness + profile.regional_expansion_fit + profile.growth_potential) / 3
    confidence = 0.45 * readiness + 0.35 * resilience + 0.20 * (100 - score)
    return round(float(np.clip(confidence, 0, 100)), 1)


def board_brief(profile: RiskProfile, segment: str | None = None) -> str:
    score = weighted_risk_score(profile)
    stress = monte_carlo_stress_test(profile)
    top_drivers = risk_contributions(profile)[:3]
    top_driver_text = ", ".join(
        item["feature"].replace("_", " ") for item in top_drivers
    )
    segment_text = f" Segment: {segment}." if segment else ""

    return (
        f"{profile.industry}: total risk is {score}/100 ({risk_band(score)})."
        f"{segment_text} Monte Carlo expected risk is {stress['expected_score']}/100, "
        f"with a {stress['prob_high_risk'] * 100:.1f}% chance of crossing the high-risk threshold. "
        f"The main risk drivers are {top_driver_text}. Recommended response: "
        f"{recommendations(profile)[0]}"
    )


def analyze_portfolio(data_path: str | Path) -> list[dict[str, object]]:
    profiles = load_profiles(data_path)
    labels, _ = kmeans_segments(feature_matrix(profiles), k=3)
    names = segment_names(profiles, labels)
    results: list[dict[str, object]] = []

    for profile, label in zip(profiles, labels):
        results.append(
            {
                "industry": profile.industry,
                "risk_score": weighted_risk_score(profile),
                "risk_band": risk_band(weighted_risk_score(profile)),
                "segment": names[int(label)],
                "strategy_confidence": strategy_confidence(profile),
                "stress_test": monte_carlo_stress_test(profile),
                "top_drivers": risk_contributions(profile)[:3],
                "board_brief": board_brief(profile, names[int(label)]),
            }
        )
    return results
