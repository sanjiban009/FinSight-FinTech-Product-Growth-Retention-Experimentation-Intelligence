# Architecture, analytics model and technical notes

## Stack

- Frontend: `index.html`, hand-authored responsive `assets/css/dashboard.css`, vanilla JS `assets/js/dashboard.js`.
- Visualization: **Plotly.js**, bundled locally as `assets/vendor/plotly.min.js` for offline and GitHub Pages usage.
- Storage and refresh model: complete synthetic records embedded in `data/dashboard-data.js` as `window.FINTECH_DEMO_DATA`. **No fetch, no third-party API, no tracking, no backend.**
- Dataset generation: Python + NumPy + pandas + scikit-learn. Seed fixed to `261113`.
- Data review: CSV (entire history); formatted Excel workbook (full user/campaign/SIP records and event samples).
- Responsive layout: five-to-three-to-two KPI columns and two-to-one chart columns by screen width.

## Entity relationships

- `Users.user_id` → `ActivityMonthly.user_id` (one to many)
- `Users.user_id` → `Trades.user_id` (one to many)
- `Users.user_id` → `WalletTransactions.user_id` (one to many)
- `Users.user_id` → `SIPInstallments.user_id` (one to many)
- `Campaigns` → `Users` through **acquisition_channel + campaign_month/signup_month** for aggregate attributed spend; individual campaign identifiers are **not** captured on user events.

**Avoid double-counting:** Distinct active users / active traders use unique user IDs; revenue and trading volume are sums of the transaction fact records. Signup conversion denominators come from Users registered in the selected FY. Existing prior-FY customers can contribute activity/revenue in the selected transactional FY.

## Global filter semantics

- **FY:** for signup KPIs use `Users.signup_date`; for transactional KPIs use transaction/event date and the same FY range.
- **Region/channel/device/segment:** restrict to users matching dimensions, then their related transaction/event facts.
- **Marketing:** campaign spend is originally recorded per channel/month. For region/device/segment views, the dashboard **allocates each channel-month spend in proportion to selected sign-ups / all sign-ups in that channel-month**. This is a declared cost-allocation assumption, not measured campaign-level targeting or causal attribution.
- **Predictive:** scores from an Oct 2026 feature snapshot. FY selector chooses **signup cohort** for this page. New November 2026 accounts have no Oct 2026 score.
- **Cohort retention:** use eligible cohorts with complete follow-up calendar month; M1 does *not* include November 2026, which is only partially observed.

## Experiment methods

Control A vs Variant B are assigned for signup dates on or after 1 April 2026. First-trade completion is binary. Dashboard computes two-sided pooled-proportion z-test, absolute lift, relative lift and unpooled Wald interval. Historical FYs have no exposed accounts, intentionally.

## Commercial metrics

- Trading Notional = `SUM(Trades.notional_inr)`.
- Gross Trading Fee = `SUM(Trades.fee_inr)`.
- Paid-channel CAC = `SUM(allocated campaign spend) / COUNT(Users where channel != Organic, acquired in period)`; selected-segment allocations use a proportional share of channel-month signups.
- Cost per acquired first trader = same spend / paid-cohort users with a first trade.
- Contribution/Spend proxy = `(0.68 * fee_revenue_from_selected_paid_signup_cohort - paid_spend) / paid_spend`.
- The `0.68` is a deliberately invented margin assumption, and is **not** CoinDCX's margin, financial performance, or business guidance.

## Known limitations

- No real user records or real company operations.
- Simple monthly generation rules and predefined behavioral segments create simplified retention patterns.
- Activity/retention is month-granular rather than event-time exact.
- Grouping can reflect cohort age censoring; activation of recent cohorts has shorter follow-up time.
- Campaign spend is channel-month aggregate. Granular geo/device/segment spend is **allocated from signup share**, not directly observed, and is not valid for causal channel attribution.
- Model performance on a synthetic generator is not evidence of production-grade prediction or fairness.
- The app is deliberately offline: no live crypto prices, authentication or trading integration.

## Recommended next iteration

Add a dashboard-filtered date-range selection, time-to-event analysis with censored cohort conversion, sample-ratio-mismatch detection, robust confidence intervals for low samples, and consented event-level telemetry for actual usage (only in a real, authorized environment).
