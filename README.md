# Fraud Detection System Design

This document explains how to design a practical banking fraud detection system using the **Question -> Data -> Insight** lifecycle.

## 1) Define the Data Science Question

Use a precise question:

**Given incoming banking transactions, which transactions or accounts are unusual enough to require fraud investigation within a target response time?**

Make this actionable by defining:

- **Detection level:** transaction-level, account-level, or both
- **Latency target:** real-time alerts (seconds/minutes) or batch alerts (hourly/daily)
- **Alert objective:** maximize fraud caught (recall) vs reduce false alarms (precision)
- **Operations constraint:** how many alerts investigators can review per day
- **Success metrics:** precision, recall, false positive rate, fraud captured, and loss prevented

## 2) Data Required

### Core Features

- **Transaction amount** - Amount transferred or spent; unusual values can indicate fraud.
- **Transaction timestamp** - Date and time of event; odd-hour activity may be suspicious.
- **Location (city/country/lat-long)** - Detects first-time regions or impossible travel patterns.
- **Merchant or beneficiary ID** - Identifies repeated suspicious destinations.
- **Merchant category (MCC)** - Some categories naturally carry higher fraud risk.
- **Channel** - ATM, POS, online, mobile, wire; each has different attack patterns.
- **Account/customer ID** - Needed for building normal behavior profiles.
- **Device and IP information** - New or rotating devices can indicate account takeover.
- **Authentication signals** - Failed logins, OTP failures, password reset events.
- **Velocity features** - Count/sum of transactions in recent windows (5m, 1h, 24h).
- **Account context** - Balance, account age, typical transaction range.
- **Historical risk indicators** - Previous disputes, chargebacks, prior alerts.
- **Fraud labels (if available)** - Confirmed fraud vs non-fraud for evaluation and tuning.

### Data Quality Issues to Expect

- Missing values (geo/device/category not captured)
- Inconsistent formats (timezones, currencies, IDs)
- Duplicate transactions (retries/replays)
- Label delay (fraud confirmed much later)
- Class imbalance (fraud is rare)
- Behavioral drift (seasonal changes, product changes)
- Historical bias (old rules influence what got labeled as fraud)
- Noisy labels (uncertain outcomes)

## 3) EDA Guide

Before modeling, understand what "normal" looks like.

### Patterns to Look For

- Heavy-tailed transaction amount distribution
- Unusual time-of-day and day-of-week patterns
- Sudden velocity spikes
- New device + new location combinations
- Repeated transfers to new beneficiaries
- Multiple accounts interacting with a single counterparty
- Segment-specific behavior differences (retail vs business)

### Useful Visualizations

- Histograms (and log-scale histograms) for amount
- Boxplots by channel, merchant category, and customer segment
- Time-series plots for transaction count and value
- Hour x weekday heatmaps
- Scatter plots (amount vs velocity)
- Geo maps for movement and jump patterns
- Network graphs (account-beneficiary relationships)
- Correlation heatmaps for feature relationships

## 4) Anomaly Detection Approaches

### A. Statistical Methods

- **Z-score / Robust Z-score (MAD):** good for numeric deviation
- **IQR thresholds:** simple outlier detection for skewed data
- **Time-series residual spikes:** detect deviations from expected trend
- **Peer-group deviation:** compare with similar user cohorts

Use these when you need:

- Quick baseline
- Strong interpretability
- Fast deployment with low complexity

### B. Machine Learning Methods

- **Isolation Forest:** strong tabular baseline, scales well
- **Local Outlier Factor (LOF):** catches local density anomalies
- **One-Class SVM:** useful but sensitive to scaling and dataset size
- **Autoencoders:** good for high-dimensional nonlinear behavior
- **Clustering-distance methods:** simple unsupervised baseline

Use these when:

- Behavior is complex and nonlinear
- You have sufficient data and monitoring support
- You can tune thresholds with business constraints

### C. Hybrid Strategy (Recommended)

Combine:

- Rule-based checks
- Statistical anomaly signals
- ML anomaly scores
- Business risk context

This usually gives better practical performance than using one method alone.

## 5) Turning Observations into Insights

### Patterns Commonly Linked to Fraud

- Large transaction after long inactivity
- Rapid small transactions followed by a large transfer
- New device + unusual location + odd hour in one event
- Many accounts sending funds to one new beneficiary
- Spike in failed authentications before a successful payment

### Interpreting Results Correctly

- An anomaly score means **suspicion**, not proof of fraud.
- Prioritize top-risk alerts for investigation.
- Track precision by score bands to set thresholds.
- Use investigator feedback to improve future detection.
- Monitor business outcomes (fraud caught, false alerts, losses prevented).
- Recalibrate regularly for changing behavior and new fraud tactics.

## 6) Practical Execution Plan (Question -> Data -> Insight)

1. Define the fraud detection objective and review capacity.
2. Build reliable transaction, behavior, and context features.
3. Perform EDA to establish baseline normal behavior.
4. Start with statistical baseline and compare with Isolation Forest/LOF.
5. Rank and route alerts to investigators with clear explanations.
6. Feed confirmed outcomes back into model/rule updates.
---

If needed, the next step is to convert this into an implementation checklist with data schema, model evaluation protocol, and alert-threshold policy.
