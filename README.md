# Fraud Detection System Design

This repository is currently a **project blueprint**, not a finished implementation. Its purpose is to define how a banking fraud detection system could be designed using the **Question -> Data -> Insight** lifecycle before moving into code, experiments, and deployment.

## Current Repository Status

At the moment, this repository contains only the project `README`. There are currently no:

- data files
- notebooks
- source code
- model artifacts
- tests
- dependency files
- pipeline or deployment components

That means this repo should be treated as a **design and planning document** for a future anomaly detection project, not as a production-ready or research-complete fraud detection system.

## Project Overview

### Problem

Banking fraud is often hidden inside very large transaction streams. Suspicious behavior may not look obviously fraudulent in isolation, but can become clear when compared against a customer's usual behavior, recent transaction velocity, device changes, location changes, or peer-group patterns.

### Project Type

This is an **anomaly detection** project for fraud analytics. Depending on the available data, it may later evolve into:

- unsupervised anomaly detection
- semi-supervised fraud detection
- supervised fraud classification

### End Goal

The expected outcome is a system that can:

- flag suspicious transactions or accounts early
- rank alerts by risk
- support fraud investigators with explainable signals
- reduce fraud losses while controlling false positives

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

## 7) Repository Gaps

The current repository has major gaps between design and execution.

### What is Missing

- No dataset description or schema
- No sample or synthetic data
- No notebook for EDA
- No preprocessing pipeline
- No feature engineering code
- No model training script
- No evaluation framework
- No environment setup (`requirements.txt`, `pyproject.toml`, etc.)
- No tests
- No deployment or inference design

### Why This Matters

Without these components:

- the project cannot be run
- the methods in this README cannot be validated
- no claims about performance can be tested
- a new contributor cannot reproduce or extend the work

## 8) Suggested Project Structure

To turn this into a real data science repository, a minimal structure should look like:

```text
data/
  raw/
  processed/
notebooks/
src/
  data/
  features/
  models/
  evaluation/
configs/
tests/
README.md
requirements.txt
```

### Lifecycle Mapping

- `data/raw/` -> data collection and source snapshots
- `data/processed/` -> cleaned and feature-ready data
- `notebooks/` -> exploratory analysis and experimentation
- `src/data/` -> ingestion and cleaning logic
- `src/features/` -> feature engineering
- `src/models/` -> anomaly detection and training code
- `src/evaluation/` -> metrics, validation, thresholding
- `configs/` -> parameters, paths, model settings
- `tests/` -> reproducibility and regression checks

## 9) Assumptions and Limitations

This design assumes:

- transaction-level data is available and joinable across systems
- key context fields such as device, location, and authentication signals exist
- customer behavior is stable enough to define a meaningful baseline
- anomalies are useful fraud indicators

Important limitations:

- anomaly does not automatically mean fraud
- fraud labels may be delayed, incomplete, or biased
- rare legitimate behavior may be flagged as suspicious
- different fraud types require different features and thresholds
- no empirical results exist yet in this repository

## 10) Quality Assessment

### Documentation

The documentation is useful for framing the problem, but weak for implementation because it does not explain how to run, test, or validate anything.

### Reproducibility

Reproducibility is currently absent because there is no code, environment file, dataset, or example pipeline.

### Scalability

Scalability cannot yet be assessed in practice. The methods listed here may scale, but the repository has no working system to evaluate.

## 11) Improvement Priorities

The most important next steps are:

1. Add a proper repository structure.
2. Define the dataset schema and fraud labels clearly.
3. Create a baseline EDA notebook.
4. Build one reproducible anomaly detection baseline such as Isolation Forest.
5. Add an evaluation protocol with thresholds, alert volume limits, and fraud capture metrics.

## 12) Contribution Guide

### Where a Beginner Should Start

Start with this `README`, then set up the missing project structure and baseline workflow.

### Safe Areas to Modify

- `README.md`
- new folders such as `notebooks/`, `src/`, `tests/`, and `configs/`
- future baseline experiments and documentation

### What Should Not Be Changed Carelessly

- the problem definition
- fraud evaluation criteria
- assumptions about labels and alerting without documenting why

### Good First Contributions

1. Add a reproducible EDA notebook using synthetic or public transaction-like data.
2. Add a baseline anomaly detection pipeline with feature generation and evaluation.
3. Add dependency management and project setup files so the repository can actually run.

## Python and Anaconda Setup

### System Information

- **Operating System:** Windows
- **Shell Used:** Command Prompt or PowerShell
- **Python (verified):** Python 3.14.4
- **Anaconda/Conda (verified):** Not detected in this terminal (not installed or not on PATH)
- **Target Conda version (recommended):** conda 26.3.1 (latest stable as of 2026-04)

### Python Installation & Verification

- Install Python on Windows.
- Open Command Prompt or PowerShell.
- Run:

```bash
python --version
```

- Expected output:

```bash
Python 3.14.4
```

- Start Python interpreter:

```bash
python
```

- Expected output:

```bash
Python 3.14.4 (default, ...)
[MSC v.**** 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

- Exit interpreter:

```bash
exit()
```

### Anaconda Installation & Setup

- Install Anaconda for Windows.
- Open Anaconda Prompt, Command Prompt, or PowerShell.
- Verify Conda installation:

```bash
conda --version
```

- Expected output (after installation):

```bash
conda 26.3.1
```

- Check Conda environment access:

```bash
conda activate
```

- Expected result:

```bash
(base)
```

- Confirm Python inside Conda:

```bash
python --version
```

- Expected output:

```bash
Python 3.x.x
```

### Environment Validation

- Verify Python is available:

```bash
python --version
```

- Verify Conda is available:

```bash
conda --version
```

- Open Python from the active Conda environment:

```bash
python
```

- Expected confirmation:

```bash
>>>
```

- Exit Python:

```bash
exit()
```

### Commands & Outputs (Proof)

```bash
python --version
Python 3.14.4

conda --version
conda : The term 'conda' is not recognized as the name of a cmdlet, function, script file, or operable program.

conda activate
conda : The term 'conda' is not recognized as the name of a cmdlet, function, script file, or operable program.

python
Python 3.14.4 (default, ...)
>>>
```

### Conclusion

- Python is installed and accessible from the terminal.
- Conda was **not available** in the current terminal session (Anaconda/Miniconda not installed or PATH not configured).
- After installing Anaconda/Miniconda, `conda --version` and `conda activate` should work as shown above.

### Final Checklist

- [ ] Windows system is available
- [ ] `python --version` runs successfully
- [ ] Anaconda/Miniconda is installed
- [ ] `conda --version` runs successfully
- [ ] `conda activate` shows `(base)`
- [ ] `python` opens the interpreter
- [ ] `exit()` closes the interpreter
