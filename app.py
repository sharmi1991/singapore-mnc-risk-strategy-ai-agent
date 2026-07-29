from pathlib import Path

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit(
        "Streamlit is not installed. Install requirements or open index.html for the no-install dashboard."
    ) from exc

from risk_engine import RiskProfile, recommendations, risk_band, strategic_position, weighted_risk_score


DATA_PATH = Path(__file__).parent / "data" / "risk_profiles.csv"


def to_profile(row: pd.Series) -> RiskProfile:
    return RiskProfile(
        industry=row["industry"],
        cost_pressure=row["cost_pressure"],
        talent_labour=row["talent_labour"],
        competition_growth=row["competition_growth"],
        regulation_compliance=row["regulation_compliance"],
        global_strategy=row["global_strategy"],
        growth_potential=row["growth_potential"],
        automation_readiness=row["automation_readiness"],
        regional_expansion_fit=row["regional_expansion_fit"],
    )


st.set_page_config(page_title="Singapore MNC Risk & Strategy AI Agent", layout="wide")
df = pd.read_csv(DATA_PATH)

st.title("Singapore MNC Risk & Strategy AI Agent")
st.caption("Agentic ML decision-support system using weighted risk scoring, K-Means segmentation, and Monte Carlo stress testing.")

industry = st.selectbox("Industry", df["industry"].tolist())
row = df[df["industry"] == industry].iloc[0]
profile = to_profile(row)
score = weighted_risk_score(profile)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk score", f"{score}/100")
col2.metric("Risk band", risk_band(score))
col3.metric("Growth potential", f"{profile.growth_potential}/100")
col4.metric("Regional expansion fit", f"{profile.regional_expansion_fit}/100")

st.subheader("Risk Breakdown")
risk_df = pd.DataFrame(
    {
        "Risk factor": [
            "Cost pressure",
            "Talent and labour",
            "Competition and growth",
            "Regulation and compliance",
            "Global strategy",
        ],
        "Score": [
            profile.cost_pressure,
            profile.talent_labour,
            profile.competition_growth,
            profile.regulation_compliance,
            profile.global_strategy,
        ],
    }
)
st.bar_chart(risk_df, x="Risk factor", y="Score")

st.subheader("Recommended Strategic Position")
st.success(strategic_position(profile))

st.subheader("Action Plan")
for action in recommendations(profile):
    st.write(f"- {action}")

st.subheader("Current Singapore Context")
st.write(
    "- Singapore remains attractive for regional headquarters, high-value services, R&D, finance, and supply-chain control."
)
st.write(
    "- Employment Pass policy and COMPASS make workforce planning important, especially for foreign professional hiring."
)
st.write(
    "- Refundable Investment Credit can support approved high-value investments, HQ activities, R&D, digital services, and supply-chain management."
)
st.write(
    "- External demand, geopolitics, energy costs, and supply-chain shifts should be monitored through scenario planning."
)
