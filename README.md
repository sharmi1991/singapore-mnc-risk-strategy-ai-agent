# Singapore MNC Risk & Strategy Analyzer

This capstone project helps analyse risks faced by MNCs operating in Singapore and recommends practical strategies.

## Best Project Option

Build a working dashboard that uses:

- A risk scoring engine
- Industry-wise risk dataset
- Strategy recommendation rules
- Real-time Singapore policy context
- A no-install HTML dashboard for demo
- An optional Streamlit app for a Python-based capstone submission

## Why This Approach Works

Singapore is attractive as a regional headquarters and strategic control hub, but it is not the cheapest place to scale routine operations. The project therefore recommends a high-value hub strategy:

> Keep Singapore as a high-value strategic hub, move routine work to cost-effective locations, invest in talent and technology, strengthen compliance, and expand regionally through partnerships.

## Files

- `index.html` - no-install interactive dashboard. Open directly in a browser.
- `app.py` - optional Streamlit dashboard.
- `risk_engine.py` - scoring and recommendation logic.
- `advanced_ml_engine.py` - k-means segmentation, Monte Carlo stress testing, explainability, and strategy confidence.
- `ai_strategy_agent.py` - agent-style workflow that calls project tools and produces a board brief.
- `data/risk_profiles.csv` - editable industry risk dataset.
- `PROJECT_REPORT_OUTLINE.md` - capstone report structure.
- `MODEL_CARD.md` - ML model purpose, inputs, outputs, limitations, and future scope.
- `SCIENTIST_LEVEL_UPGRADE_PLAN.md` - advanced positioning and viva pitch.
- `requirements.txt` - Python dependencies for Streamlit version.

## How To Demo

### Option 1: No-install browser demo

Open `index.html` in any browser.

### Option 1B: Advanced ML/agent demo

Run:

```bash
python ai_strategy_agent.py --industry "Technology and AI services"
```

The output shows the agent tool trace, risk score, Monte Carlo stress result, strategic segment, top drivers, and LLM-ready prompt.

### Option 2: Streamlit demo

Install Python, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Risk Score Logic

The dashboard calculates:

```text
Total Risk Score =
Cost Pressure * 0.25 +
Talent and Labour * 0.20 +
Competition and Growth * 0.18 +
Regulation and Compliance * 0.17 +
Global Strategy * 0.20
```

Risk bands:

- Low: below 45
- Medium: 45 to 69.9
- High: 70 and above

## Real-Time Context Used

- Singapore remains a strong headquarters location because of regional connectivity, talent, trust, and infrastructure.
- Employment Pass eligibility includes qualifying salary and COMPASS, so foreign professional hiring requires planning.
- Refundable Investment Credit supports approved high-value activities such as headquarters, centres of excellence, R&D, digital services, and supply-chain management.
- 2026 economic context includes resilient growth but higher geopolitical and external-demand uncertainty.

## Official Sources

- EDB Singapore Headquarters: https://www.edb.gov.sg/en/our-industries/headquarters.html
- MOM Employment Pass Eligibility: https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility
- IRAS Refundable Investment Credit: https://www.iras.gov.sg/schemes/disbursement-schemes/refundable-investment-credit-(ric)
- MTI 2026 GDP Forecast: https://www.mti.gov.sg/newsroom/mti-maintains-2026-gdp-growth-forecast-at--2-0-to-4-0-per-cent-/
- MTI 2Q 2026 Advance Estimates: https://www.mti.gov.sg/newsroom/singapore-s-gdp-grew-by-5-7-per-cent-in-the-second-quarter-of-2026/

## Viva Explanation

This is not only a static assignment. It is a working decision-support prototype. The user selects an industry, the system calculates weighted risk, classifies the risk level, and generates strategy recommendations. The advanced version adds k-means strategic segmentation, Monte Carlo stress testing, contribution-based explainability, and an AI-agent-style workflow. The model is transparent because every score, weight, segment, and recommendation can be explained and changed.
