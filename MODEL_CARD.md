# Model Card: Singapore MNC Risk & Strategy Analyzer

## Model Purpose

This model supports strategic risk analysis for multinational companies operating in Singapore. It helps decide whether an industry should scale in Singapore, operate Singapore as a high-value hub, distribute routine work regionally, or delay expansion until cost and compliance risks are stabilised.

## Intended Users

- Business analysts
- Strategy teams
- Capstone evaluators
- Students demonstrating applied ML, analytics, and AI-agent thinking

## ML Components

- Weighted risk scoring model
- Deterministic k-means segmentation from scratch
- Monte Carlo stress testing
- Contribution-based explainability
- Strategy confidence score
- Agent-style tool orchestration

## Input Features

- Cost pressure
- Talent and labour risk
- Competition and growth risk
- Regulation and compliance risk
- Global strategy risk
- Growth potential
- Automation readiness
- Regional expansion fit

## Output

- Total risk score
- Risk band
- Strategic segment
- High-risk probability under stress
- Top risk drivers
- Recommended action plan
- Board-level brief

## Why This Is Stronger Than a Simple Dashboard

A simple dashboard only displays data. This project makes decisions:

1. It scores risk using transparent weights.
2. It groups industries into strategic segments.
3. It simulates uncertainty through Monte Carlo stress testing.
4. It explains which factors drive risk.
5. It uses an agent workflow to combine data, policy context, model output, and recommendations.

## Real-Time Singapore Fit

The model is aligned with 2026 Singapore context:

- Singapore remains a strong headquarters and regional hub location.
- Employment Pass and COMPASS rules make workforce planning important.
- Refundable Investment Credit supports high-value activities such as headquarters, centres of excellence, R&D, digital services, and supply-chain management.
- AI-related demand supports some sectors, but geopolitics and external demand still create downside risk.

## Limitations

- Current dataset is curated for capstone demonstration and should be replaced with live APIs for production.
- Risk scores are strategic estimates, not audited financial forecasts.
- The recommendation engine is transparent and rule-based; an LLM can be added later for natural-language board reports.

## Future Improvements

- Connect to World Bank, MTI, MAS, and news APIs.
- Add live web retrieval.
- Add LightGBM or XGBoost when a larger labelled dataset is available.
- Add SHAP explainability for supervised models.
- Add interactive scenario sliders.
- Deploy as Streamlit Cloud or Hugging Face Space.
