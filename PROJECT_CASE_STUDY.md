# Portfolio case study — converting fintech data into product decisions

## Project / challenge

The hypothetical stakeholder is a Product & Growth team at a digital-asset fintech. The team wants a single management reporting environment answering three interconnected questions: **(1)** Where are users lost before their first trade? **(2)** Are newly acquired customers returning? **(3)** Which product changes and marketing channels generate better first-trade outcomes without wasting budget?

**Data:** synthetic registration, KYC, deposit and trade dates, app-activity months, fee records, aggregate campaign spend and experimental assignment from FY 2024–25 through FY 2026–27 YTD. Model scoring and validation use this synthetic history. None of this is actual CoinDCX company data.

## Sample findings at FY2026–27 YTD (unfiltered dashboard)

1. **1,298 new registrations**; 75.7% reached KYC verification; 54.2% deposited; 43.2% completed a first trade. **Recommendation:** monitor conditional conversion by stage; prioritize abandonment research and KYC/deposit completion UX.
2. **M1 retention: 72.5%** among 976 fully eligible first-month user cohorts. **Recommendation:** establish a cohort baseline by acquisition channel and segment rather than depending on aggregate MAU.
3. **Synthetic A/B onboarding test:** control first-trade conversion 40.0% vs variant 46.7%, relative lift +16.9%, pooled two-sided p-value 0.0142. **Recommendation:** test guardrails, data quality and incremental value before shipping; do not treat this simulated test as real-world proof.
4. **Synthetic trading volume: ₹40.50 Cr**, fee revenue: **₹3.01 L** within report period. **Recommendation:** distinguish notional throughput from actual fee economics when communicating performance.
5. **Channel spend: ₹8.10 L**, cost per new paid user ~₹875, cost per first trader ~₹2.2 K. Illustrative contribution/spend proxy is **negative**: **−94.4%**. **Recommendation:** investigate acquisition payback and downstream monetization instead of optimizing raw sign-ups alone. Never misrepresent this margin proxy as actual profitability.
6. **Model holdout ROC-AUC: 0.770** on synthetic September→October 2026 test data. **Recommendation:** use as a proof-of-concept risk ranking, then design randomized outreach tests; do not deploy on real customers without prospective validation and privacy review.

## Implementation highlights

- **Decision-oriented dashboard design:** 7 navigation pages, five global slicers, contextual insights, readable bar labels, cohort heatmaps, experimentation uncertainty and transparent formula definitions.
- **Coherent data model:** a single user dimension linked to trading, wallet and activity fact datasets; marketing spend aggregated by period and acquisition channel; documented allocation assumptions.
- **Reproducible predictive component:** an actual scikit-learn logistic regression with time-based train/test evaluation, rather than an unvalidated hard-coded risk label.
- **Offline and deployable:** complete static website, bundled Plotly and data, ready for GitHub Pages; screenshots and LinkedIn copy supplied.
- **Indian standards:** April–March FY reporting and INR Lakhs/Crores presentation.

## Recruiter-ready one-liner

> Developed an end-to-end interactive FinTech Product Analytics platform covering conversion, M1/M3/M6 cohort retention, A/B testing, marketing economics and predictive churn risk using Excel/CSV, HTML/JavaScript, Plotly and Python — with reproducible synthetic data and a holdout-validated logistic regression model.

## Next improvements

Add incremental business metrics (gross margin by fee schedule and product, post-experiment M1 retention guardrails, time-to-event conversion accounting for censoring) and document real BI data governance, should an authorized, consented data source become available.
