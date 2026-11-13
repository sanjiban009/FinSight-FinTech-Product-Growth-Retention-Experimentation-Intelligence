# Data dictionary and relationships

**All records are generated.** No production or individual customer data was used. Dates use ISO strings, and FY labels use April–March Indian financial years.

## ActivityMonthly
**Rows:** 29,109. **File:** `data/csv/ActivityMonthly.csv`.

| Column | Meaning |
|---|---|
| `user_id` | Surrogate synthetic user ID; joins to User dimension |
| `activity_month` | Month with at least one modeled app session |
| `activity_fy` | Indian financial year of activity month |
| `sessions` | Simulated sessions in user/month; integer |
| `active_days` | Simulated active days in user/month |
| `most_used_feature` | Largest modeled in-app feature category in that month |
| `support_tickets` | Synthetic count of month-level support tickets (0/1) |

## Campaigns
**Rows:** 192. **File:** `data/csv/Campaigns.csv`.

| Column | Meaning |
|---|---|
| `campaign_id` | Channel-month synthetic campaign identifier |
| `campaign_month` | Month associated with channel-level marketing activity |
| `campaign_fy` | April–March campaign FY |
| `channel` | Channel with simulated spend, impressions and clicks |
| `spend_inr` | Synthetic channel-month marketing spend in INR; zero for Organic |
| `impressions` | Synthetic campaign impressions |
| `clicks` | Synthetic campaign clicks |

## ModelValidation
**Rows:** 1. **File:** `data/csv/ModelValidation.csv`.

| Column | Meaning |
|---|---|
| `metric` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `sample_size` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `positive_rate` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `roc_auc` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `pr_auc` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `brier_score` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `train_snapshots` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `predictive_target` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `scope` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |
| `model` | Model-validation run metadata or test statistic; refer to MODEL_CARD.md |

## SIPInstallments
**Rows:** 641. **File:** `data/csv/SIPInstallments.csv`.

| Column | Meaning |
|---|---|
| `installment_id` | Synthetic recurring-investment installment identifier |
| `user_id` | Surrogate synthetic user ID; joins to User dimension |
| `scheduled_month` | Month payment scheduled |
| `fy` | FY of scheduled installment |
| `planned_amount_inr` | Planned INR installment |
| `paid_amount_inr` | Modeled INR paid amount, zero when missed |
| `status` | Success, Failed, Pending; in SIP also Paid, Missed |

## Trades
**Rows:** 21,969. **File:** `data/csv/Trades.csv`.

| Column | Meaning |
|---|---|
| `trade_id` | Synthetic order identifier |
| `user_id` | Surrogate synthetic user ID; joins to User dimension |
| `trade_date` | ISO date of executed trade |
| `trade_month` | Calendar month of trade |
| `trade_fy` | April–March FY of trade |
| `product` | Spot, Futures or Earn / SIP simulated trading type |
| `asset` | BTC, ETH, SOL or Other category |
| `notional_inr` | Synthetic executed notional in INR; not fee or profit |
| `fee_inr` | Synthetic fee earned in INR at modeled rate |

## Users
**Rows:** 4,100. **File:** `data/csv/Users.csv`.

| Column | Meaning |
|---|---|
| `user_id` | Surrogate synthetic user ID; joins to User dimension |
| `signup_date` | ISO signup date used for acquisition cohort FY |
| `signup_month` | Calendar month YYYY-MM |
| `signup_fy` | Indian April–March financial year of registration |
| `acquisition_channel` | Simulated first-touch channel |
| `region` | Illustrative four-way location region, not city/person geography |
| `device` | Android, iOS or Web acquisition device |
| `behavior_segment` | Predefined synthetic behavioral archetype; not a model score |
| `experiment_group` | Control A, Variant B or Not exposed (test from Apr 2026) |
| `kyc_date` | First verified-KYC date; blank when not completed |
| `first_deposit_date` | Date of first simulated completed deposit, if applicable |
| `first_trade_date` | Date of first executed trade, if applicable |
| `churn_risk_score` | Model-estimated inactivity probability from Oct 2026 snapshot; blank for Nov signups |

## WalletTransactions
**Rows:** 5,815. **File:** `data/csv/WalletTransactions.csv`.

| Column | Meaning |
|---|---|
| `transaction_id` | Synthetic deposit/withdrawal transaction identifier |
| `user_id` | Surrogate synthetic user ID; joins to User dimension |
| `transaction_date` | Wallet transaction calendar date |
| `transaction_month` | Wallet transaction month |
| `transaction_fy` | Wallet transaction FY |
| `transaction_type` | Deposit or Withdrawal |
| `payment_method` | UPI, IMPS, NEFT or Card |
| `amount_inr` | Amount in INR |
| `status` | Success, Failed, Pending; in SIP also Paid, Missed |

## Data model

- `Users.user_id` → `ActivityMonthly.user_id`, `Trades.user_id`, `WalletTransactions.user_id`, `SIPInstallments.user_id` (one-to-many).
- `Campaigns` is linked to Users only by `campaign_month` + `channel`, not through a user-level campaign ID.
- Filtered marketing spend is estimated by allocating channel-month spend using a filtered cohort share of new sign-ups.
- Transaction facts have their own FY; a 2025 signup can trade in FY2026–27. Signup funnel measures always apply to signup cohorts.
