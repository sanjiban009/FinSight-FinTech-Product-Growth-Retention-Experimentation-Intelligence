# FinSight — FinTech Product Growth, Retention & Experimentation Intelligence

**Seven-page interactive FinTech product analytics portfolio dashboard**, inspired by the analytical questions asked of Business Analysts and Product Analysts at digital-asset trading platforms and other fintechs.

> **Independent simulated case study.** Not affiliated with, commissioned by, sponsored by or based on internal data from CoinDCX. Every number is generated for demonstration. The project is *not* a live cryptocurrency trading service.



## Why this project matters

Growing a fintech app requires understanding which users activate, how onboarding steps affect conversion, whether acquisition channels bring engaged traders, whether product experiments actually improve outcomes, and which inactive users may need re-engagement. **FinSight connects those decisions in one filterable, FY-aligned product analytics workspace.**

### The 7 interactive pages

| Page | Business question | Key metrics and analysis |
|---|---|---|
| **01 Executive Command Center** | Are product growth and monetization improving? | New registrations, first-trade activation, monthly engagement, trading notional, gross trading fees, acquisition/region breakdowns |
| **02 Conversion Funnel** | At which activation step do users stop progressing? | Registration → KYC → first deposit → first trade; channel quality; cohort activation; time to first trade |
| **03 Retention & Cohorts** | Which acquisition cohorts return and how quickly do they churn? | M1, M3, M6 retention, cohort heatmap, retention decay, lapse/reactivation signals |
| **04 Product Engagement** | What drives recurring platform activity? | MAU, trades per trader, trading product mix, fee-related behavior, wallet completion, feature popularity |
| **05 Experimentation Lab** | Does an onboarding variant improve first-trade activation? | Randomized synthetic A/B groups, percentage-point & relative lift, pooled two-proportion z test, 95% Wald confidence interval |
| **06 Marketing ROI** | Which channels acquire users efficiently? | Paid CAC, cost per first trade, spend trends, conversion, spend allocation, *illustrative* fee-contribution proxy |
| **07 Predictive Insights** | Which users are likely to stop being active next month? | Logistic-regression churn scores, high/medium/low risk bands, segment & channel drill-down, holdout ROC-AUC, PR-AUC, Brier |



## Quick start — no installation needed

1. Download the project ZIP and **extract it completely**.
2. Open **`index.html`** in Chrome, Edge, Safari or Firefox. The dashboard bundles Plotly locally, with no API calls, login, external font requests or internet requirement.
3. Use the **Financial Year, Channel, Region, Device and Behavior Segment** selectors. Click relevant bars to cross-filter, or choose **Export filtered CSV**.
4. Navigate with the left sidebar or press keys **1–7**.
5. To modify the demo, edit the CSV/data generator and rerun `tools/generate_dataset.py` (requires Python dependencies). Data files must retain their relative directory names.

**Important:** Do not upload the ZIP as a single GitHub file if you want a working GitHub Pages site. Upload the extracted folder **contents**, so `index.html` is at repository root.

## India financial-year coverage

- **FY 2024–25** — 1 April 2024 to 31 March 2025.
- **FY 2025–26** — 1 April 2025 to 31 March 2026.
- **FY 2026–27 YTD** — 1 April 2026 to 13 November 2026.
- **All FYs** — 1 April 2024 through 13 November 2026.

All currency is **₹ INR**. Large values are rendered in **Lakhs (L)** and **Crores (Cr)**, using Indian grouping.

## Data and reproducibility

| Path | Contents |
|---|---|
| `data/csv/` | Complete synthetic Users, ActivityMonthly, Trades, WalletTransactions, SIPInstallments, Campaigns, ModelValidation CSV tables |
| `data/dashboard-data.js` | Full preloaded data for immediate offline filtering; no `fetch()` calls |
| `data/excel/FinSight_Synthetic_Dataset_FY2024_2027.xlsx` | Formatted Excel review workbook: all users, campaigns, SIP rows, model-validation data **plus FY-stratified activity/trade/wallet samples**. Full event-level history remains in the CSV folder. |
| `data/metadata.json` | Period, definitions, seed, event totals and model-validation facts |
| `tools/generate_dataset.py` | Deterministic synthetic generation and real sklearn logistic model training/scoring |
| `tools/build_excel.py` | Workbook creation script via `artifact_tool` (preinstalled in authoring environment) |
| `index.html` | Interactive app entry point |
| `assets/js/dashboard.js` | FY-aware metrics, filtering, Plotly charts and dynamic decision insights |
| `assets/css/dashboard.css` | Responsive dark enterprise styling |
| `assets/vendor/plotly.min.js` | Locally bundled Plotly for offline operation |
| `screenshots/` | Seven genuine browser-rendered full-page JPEGs, plus a LinkedIn cover |
| `docs/` | Metric dictionary, technical methodology, model card, GitHub upload steps, LinkedIn copy and testing |

**Dataset sizes:** 4,100 synthetic users, 29,109 active-user-month records, 21,969 executed trades, 5,815 wallet transactions, 641 SIP installments and 192 campaign/month records.

The sample assigns synthetic IDs, not names or contact information, and makes no factual claims about real-company performance.

## Skills demonstrated

`Product Analytics` · `Business Intelligence` · `HTML` · `CSS` · `JavaScript` · `Plotly.js` · `Python` · `Excel` · `Cohort Retention` · `Funnel Analysis` · `A/B Testing` · `Marketing Attribution` · `Statistical Testing` · `Predictive Modeling` · `Executive Storytelling` · `FY Reporting`




## Statistical honesty and caveats

- The A/B test is **simulated**: the variant lift is a property of the generator, not real-world causal evidence.
- Retention is **calendar-month M1/M3/M6**, not strict 30/90/180-day retention. Only fully observed follow-up months are counted.
- The marketing contribution ratio is a **transparent illustrative proxy**, not a true attributed incremental ROI or LTV forecast.
- The churn model is **actually trained and tested on synthetic records**; its reported performance says nothing about live-population performance.
- The current YTD month is partial. Sign-up cohorts from recent months have less time to convert.

Read the data dictionary and model card for definitions and methodology.

## Author

**Sanjiban Das** — Business Intelligence & Product Analytics

- Portfolio: https://sanjiban009-analytics.redrat130.chatgpt.site/
- GitHub: https://github.com/sanjiban009

**Code license:** MIT (see LICENSE). All synthetic data and analytics are intended for teaching and portfolio demonstration.
