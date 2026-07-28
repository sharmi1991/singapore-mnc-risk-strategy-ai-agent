"""
advanced_ml_engine.py

Advanced ML layer for the Singapore MNC Risk & Strategy AI Agent.

This module adds three capabilities on top of the base weighted risk score
produced by risk_engine.py:

1. K-Means strategic segmentation  — groups industries into strategic archetypes
2. Monte Carlo stress testing      — estimates probability of an industry
                                      crossing into high-risk territory under
                                      simulated future shocks
3. Explainability                  — breaks down each risk score into its
                                      weighted contributing factors and ranks
                                      the top drivers per industry

Extracted and adapted from the project's research notebook
(singapore-mnc-risk-strategy-ai-agent.ipynb).
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ---------------------------------------------------------------------------
# Risk weights (kept in sync with risk_engine.py)
# ---------------------------------------------------------------------------
RISK_WEIGHTS = {
    "cost_pressure": 0.25,
    "talent_labour": 0.20,
    "competition_growth": 0.18,
    "regulation_compliance": 0.17,
    "global_strategy": 0.20,
}

ML_FEATURES = [
    "cost_pressure",
    "talent_labour",
    "competition_growth",
    "regulation_compliance",
    "global_strategy",
    "growth_potential",
    "automation_readiness",
    "regional_expansion_fit",
]

RISK_FEATURES = list(RISK_WEIGHTS.keys())

# Human-readable names for the 3 K-Means clusters, based on cluster profile
# analysis performed on the 20-industry dataset. Cluster membership was
# inspected directly (mean feature values + industry list per cluster)
# rather than assumed:
#   Cluster 0 -> high regulation/talent intensity + high growth potential
#                (Finance, Tech/AI, Pharma, Professional services, Biotech,
#                 Healthcare, Cybersecurity, Renewable energy)
#   Cluster 1 -> lower intensity across most dimensions, more domestic/
#                consumer-facing (Telecom, Real estate, Hospitality,
#                Agri-food tech, EdTech, Media)
#   Cluster 2 -> high global-strategy exposure + regional expansion fit
#                (Manufacturing, Logistics, Oil & gas, Aerospace, E-commerce,
#                 Marine engineering)
CLUSTER_NAMES = {
    0: "High-Value Hub Candidates",
    1: "Domestic & Consumer-Facing Segment",
    2: "Regional Trade & Supply-Chain Exposure",
}

# NOTE on k=3: silhouette analysis on this dataset (k=2..6) gives scores in
# the 0.195-0.211 range with no single sharply-optimal k. k=3 was chosen for
# business interpretability (three actionable strategic archetypes) rather
# than pure statistical optimality. See evaluate_cluster_counts() below to
# reproduce this analysis, and README.md -> "Data Source & Methodology".


# ---------------------------------------------------------------------------
# K Selection Justification (silhouette analysis)
# ---------------------------------------------------------------------------
def evaluate_cluster_counts(df: pd.DataFrame, k_range=range(2, 7), random_state: int = 42) -> pd.DataFrame:
    """
    Reproduces the silhouette analysis used to justify k=3. Returns a small
    table of inertia + silhouette score for each candidate k, so the choice
    of k is verifiable rather than asserted.

    On the 20-industry dataset, silhouette scores fall in a narrow 0.195-0.211
    band across k=2..6 -- there is no single sharply-optimal k. k=3 is used
    for business interpretability (three actionable strategic archetypes),
    not because it statistically dominates the alternatives.
    """
    from sklearn.metrics import silhouette_score

    X = StandardScaler().fit_transform(df[ML_FEATURES])
    rows = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10).fit(X)
        rows.append({
            "k": k,
            "inertia": round(km.inertia_, 1),
            "silhouette_score": round(silhouette_score(X, km.labels_), 3),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 1. K-Means Strategic Segmentation
# ---------------------------------------------------------------------------
def add_strategic_segments(df: pd.DataFrame, n_clusters: int = 3, random_state: int = 42) -> pd.DataFrame:
    """
    Groups industries into strategic segments using K-Means clustering on
    standardised risk/growth features, then maps cluster IDs to
    business-friendly segment names.
    """
    df = df.copy()
    X = df[ML_FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)
    df["strategic_segment"] = df["cluster"].map(CLUSTER_NAMES)

    return df


# ---------------------------------------------------------------------------
# 2. Monte Carlo Stress Testing
# ---------------------------------------------------------------------------
def monte_carlo_stress_test(row: pd.Series, simulations: int = 5000, shock_strength: float = 8, seed: int = 42) -> pd.Series:
    """
    Simulates future macro and industry-specific shocks to estimate the
    probability that an industry's risk score crosses into the "High" band
    (>= 70) under stress.
    """
    np.random.seed(seed)

    base_values = row[RISK_FEATURES].values.astype(float)
    weights = np.array([RISK_WEIGHTS[feature] for feature in RISK_FEATURES])

    # Shared macro shock affects cost, talent, and global strategy together
    shared_macro_shock = np.random.normal(0, shock_strength, size=(simulations, 1))

    # Individual shocks for each risk factor
    individual_shocks = np.random.normal(
        0, shock_strength * 0.65, size=(simulations, len(RISK_FEATURES))
    )

    # Sensitivity of each risk factor to the shared macro shock
    shock_vector = np.array([0.75, 0.55, 0.35, 0.25, 0.85])

    simulated_values = base_values + shared_macro_shock * shock_vector + individual_shocks
    simulated_values = np.clip(simulated_values, 0, 100)

    simulated_scores = simulated_values @ weights

    return pd.Series({
        "expected_stressed_risk": round(simulated_scores.mean(), 1),
        "p10_risk": round(np.percentile(simulated_scores, 10), 1),
        "p90_risk": round(np.percentile(simulated_scores, 90), 1),
        "prob_high_risk": round((simulated_scores >= 70).mean(), 3),
    })


def add_stress_test_results(df: pd.DataFrame, simulations: int = 5000, shock_strength: float = 8, seed: int = 42) -> pd.DataFrame:
    """Applies monte_carlo_stress_test() across every row in the dataframe."""
    df = df.copy()
    stress_results = df.apply(
        lambda row: monte_carlo_stress_test(row, simulations, shock_strength, seed),
        axis=1,
    )
    return pd.concat([df, stress_results], axis=1)


# ---------------------------------------------------------------------------
# 3. Explainability — Risk Contribution Analysis
# ---------------------------------------------------------------------------
def calculate_risk_contributions(row: pd.Series) -> pd.Series:
    """Breaks a row's total risk score into its weighted per-factor contributions."""
    contributions = {}
    for feature, weight in RISK_WEIGHTS.items():
        contributions[feature] = round(row[feature] * weight, 2)
    return pd.Series(contributions)


def build_contribution_table(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe of weighted risk contributions per industry."""
    contribution_df = df.apply(calculate_risk_contributions, axis=1)
    contribution_df["industry"] = df["industry"]
    return contribution_df


def build_top_drivers_table(contribution_df: pd.DataFrame) -> pd.DataFrame:
    """
    For each industry, ranks the risk factors by weighted contribution and
    returns the top 3 drivers — this is what makes the model explainable
    rather than a black box.
    """
    top_driver_rows = []

    for _, row in contribution_df.iterrows():
        industry = row["industry"]
        driver_values = row.drop("industry").sort_values(ascending=False)

        top_driver_rows.append({
            "industry": industry,
            "top_driver_1": driver_values.index[0],
            "top_driver_1_points": driver_values.iloc[0],
            "top_driver_2": driver_values.index[1],
            "top_driver_2_points": driver_values.iloc[1],
            "top_driver_3": driver_values.index[2],
            "top_driver_3_points": driver_values.iloc[2],
        })

    return pd.DataFrame(top_driver_rows)


def add_explainability(df: pd.DataFrame) -> pd.DataFrame:
    """Convenience wrapper: builds contribution + top-drivers tables and
    merges the top-driver columns back onto the main dataframe."""
    contribution_df = build_contribution_table(df)
    top_drivers_df = build_top_drivers_table(contribution_df)
    return df.merge(top_drivers_df, on="industry", how="left")


# ---------------------------------------------------------------------------
# Convenience: run the full advanced ML pipeline on a base risk dataframe
# ---------------------------------------------------------------------------
def run_advanced_ml_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe that already has 'risk_score' and 'risk_band'
    (from risk_engine.py) and adds: strategic segments, Monte Carlo stress
    test results, and explainability (top risk drivers).
    """
    df = add_strategic_segments(df)
    df = add_stress_test_results(df)
    df = add_explainability(df)
    return df


if __name__ == "__main__":
    # Standalone demo: load the dataset, compute the base risk score inline
    # (mirrors risk_engine.py logic), then run the full advanced ML pipeline.
    df = pd.read_csv("data/risk_profiles.csv")

    def calculate_risk_score(row):
        return round(sum(row[f] * w for f, w in RISK_WEIGHTS.items()), 1)

    def assign_risk_band(score):
        if score >= 70:
            return "High"
        elif score >= 45:
            return "Medium"
        return "Low"

    df["risk_score"] = df.apply(calculate_risk_score, axis=1)
    df["risk_band"] = df["risk_score"].apply(assign_risk_band)

    result = run_advanced_ml_pipeline(df)
    cols = [
        "industry", "risk_score", "risk_band", "strategic_segment",
        "prob_high_risk", "top_driver_1", "top_driver_2", "top_driver_3",
    ]
    print(result[cols].sort_values("risk_score", ascending=False).to_string(index=False))
