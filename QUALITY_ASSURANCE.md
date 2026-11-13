# Quality assurance — generated dashboard

Automated real Chromium rendering and interaction testing was run against the generated HTML, CSS, locally bundled Plotly and full synthetic dataset. Seven full-page LinkedIn-ready JPEGs were captured from the real dashboard using Playwright's in-memory-document method. This method avoids browser restrictions on navigating to file URLs but **loads exactly the same HTML, CSS and JS bytes that are shipped**.

| Page | Rendering | Verified 5 KPI values (FY2026–27; no segmentation filters) |
|---|---|---|
| Executive | PASS | 1,298 sign-ups; 43.2% first-trade activation; 1,554 active traders; ₹40.50 Cr trading notional; ₹3.01 L fees |
| Conversion | PASS | 1,298 sign-ups; 75.7% KYC; 54.2% deposit; 43.2% first trade; 13.9-day mean time to trade |
| Retention | PASS | 72.5% M1; 58.9% M3; 44.9% M6; 161 lapsed; 278 reactivated |
| Engagement | PASS | 1,966 latest-month active users; 9,647 orders; 6.2 orders/trader; ₹42.0 K average notional; 91.6% deposit success |
| Experimentation | PASS | 1,298 exposed; control 40.0%; variant 46.7%; +16.9% relative lift; p = 0.0142 |
| Marketing | PASS | ₹8.10 L spend; 926 paid acquisitions; ₹875 per sign-up; ₹2.2 K per first trade; −94.4% illustrative contribution/spend |
| Predictive | PASS | 1,135 scored; 189 high risk; 47.1% average risk; 0.770 ROC-AUC; 534 model-expected inactive |

**Global filter test:** Selecting East changed executive sign-ups from 1,298 to 336. Reset returned filters to all segments. **No JavaScript page errors were reported.**

**Excel test:** The workbook exported correctly with readable headers, frozen header rows, typed numeric fields, formula-driven Data_Checks and representative FY-stratified event samples. Full event facts are supplied separately in CSV and dashboard-data.js.

All metrics were derived from generated synthetic records. Checks are reproducible with `tools/test_dashboard.py` (Playwright + Chromium required) and `tools/generate_dataset.py` (NumPy/pandas/scikit-learn required).
