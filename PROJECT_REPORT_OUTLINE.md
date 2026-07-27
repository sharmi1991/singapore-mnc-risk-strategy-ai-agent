# Capstone Report Outline

## Title

Singapore MNC Risk & Strategy Analyzer

## Abstract

This project analyses major risks faced by multinational companies operating in Singapore and provides industry-specific strategy recommendations. The system uses a weighted risk scoring model covering cost pressure, talent and labour, competition and growth, regulation and compliance, and global strategy risk. It recommends a high-value hub approach where Singapore is used for strategic functions while routine work is distributed across cost-effective regional locations.

## Problem Statement

Singapore is a strong base for multinational companies because of its stability, talent quality, infrastructure, and regional connectivity. However, high operating costs, strict labour policies, intense talent competition, compliance requirements, small domestic market size, and global supply-chain uncertainty can reduce competitiveness. MNCs need a structured way to assess these risks and choose practical strategies.

## Objectives

- Identify key risks for MNCs in Singapore.
- Calculate industry-wise risk scores.
- Classify risk into low, medium, and high categories.
- Recommend strategies to reduce risk.
- Build a working dashboard for analysis and presentation.

## Methodology

The project uses a weighted scoring model. Each industry receives scores from 0 to 100 for five risk categories. The weighted average becomes the total risk score. Recommendations are generated using rule-based decision logic.

## Risk Categories

- Cost pressure
- Talent and labour
- Competition and growth
- Regulation and compliance
- Global strategy risk

## Proposed Strategy

The best approach is to keep Singapore as a high-value strategic hub, move routine work to cost-effective locations, invest in talent and technology, strengthen compliance, and expand regionally through partnerships.

## Implementation

The prototype includes:

- CSV dataset
- Python risk scoring engine
- K-means strategic segmentation
- Monte Carlo stress testing
- Contribution-based explainability
- Agent-style tool orchestration
- Browser dashboard
- Optional Streamlit dashboard
- Recommendation logic
- Source-backed Singapore policy context

## Expected Outcome

The tool helps companies understand whether an industry is suitable for aggressive expansion, selective scaling, regional partnership, or cost stabilisation. It also supports capstone presentation because the logic is explainable and visible.

## Advanced ML Contribution

The advanced layer improves the project beyond a simple dashboard. K-means segmentation groups industries into strategic clusters. Monte Carlo simulation estimates how risk may change under uncertain cost, talent, compliance, and geopolitical shocks. Contribution analysis explains the main drivers behind each risk score. The agent workflow combines profile retrieval, model output, policy context, and recommendation generation into a decision-ready brief.

## Conclusion

Singapore remains attractive for MNC headquarters and regional operations, but companies must avoid using it as a low-cost scaling base. A high-value hub model with regional diversification, technology adoption, compliance strength, and talent development gives MNCs better long-term competitiveness.

## Future Scope

- Add live APIs for macroeconomic data.
- Add news sentiment analysis.
- Add AI-generated board-level strategy reports.
- Add country comparison across ASEAN.
- Add scenario simulation for tariffs, hiring cost, and demand shocks.
