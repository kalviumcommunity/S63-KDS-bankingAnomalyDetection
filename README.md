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

## 1. Launching Jupyter Notebook

- Run from terminal:

```bash
conda activate base
jupyter notebook
```

- Practical verification:
  - Jupyter opens automatically in the browser.
  - Notebook home page opens at the directory where the command was run.

## 2. Jupyter Home Interface Overview

- **File/folder listing area:** Shows project files and folders.
- **Navigation breadcrumbs:** Shows current path and allows quick back navigation.
- **New button:** Creates new notebook files (Python 3 kernel).
- **File type indicators:** Differentiates folders, notebooks (`.ipynb`), and other files.

## 3. Folder Navigation

- Open a folder by clicking its name in the listing.
- Move back by clicking a previous path in breadcrumbs.
- Always confirm you are in the correct project folder before creating notebooks.

## 4. Creating and Running a Notebook

- Click **New** -> **Python 3**.
- A new notebook opens in a new tab.
- Verify kernel in top-right is **Python 3** (or the expected Conda environment).
- Run sample cell:

```python
print("Jupyter is working")
```

- Expected output:

```text
Jupyter is working
```

## 5. Notebook Management

- Rename: Click notebook title (top) and enter a new name.
- Save: Press **Ctrl + S** or use **File -> Save and Checkpoint**.
- Close: **File -> Close and Halt**.
- Reopen: Return to Jupyter home page and click the notebook filename.

## 6. Conclusion

- Jupyter Notebook launches correctly from terminal.
- Folder and breadcrumb navigation is understood.
- Notebook creation, kernel verification, and code execution work correctly.

## PR Section: Code vs Markdown Cells (Notebook Proof)

### Notebook File

- `Jupyter_Code_vs_Markdown_Demo.ipynb`

### Structure Used

- Markdown cell: title and notebook purpose
- Markdown cell: explanation before code
- Code cell: simple Python (`print`)
- Markdown cell: output explanation
- Markdown cell: explanation before code
- Code cell: simple math
- Markdown cell: output explanation and usage summary

### Cell Content Snapshot

**Markdown (title and purpose)**

```markdown
# Code vs Markdown Cells Demo

Purpose: Show correct usage of Markdown cells for explanation and Code cells for execution.
```

**Markdown (before code cell 1)**

```markdown
This code cell prints a message to verify Python execution in Jupyter.
```

**Code cell 1**

```python
print("Hello from a Code cell")
```

**Markdown (after code cell 1)**

```markdown
Output shows the text message. This confirms the cell executed correctly.
```

**Markdown (before code cell 2)**

```markdown
This code cell performs basic arithmetic and prints the result.
```

**Code cell 2**

```python
a = 8
b = 4
print("Sum:", a + b)
print("Product:", a * b)
```

**Markdown (after code cell 2)**

```markdown
The output displays Sum: 12 and Product: 32.
Use Markdown cells for notes, headings, and interpretation.
Use Code cells for Python execution and results.
```

### 2-Minute Video Script (Code vs Markdown)

**Intro and notebook setup (0:00 - 0:20)**
"In this short demo, I show the difference between Markdown and Code cells in Jupyter Notebook using a simple structured flow."

**Creating a Markdown cell (0:20 - 0:45)**
"I create a Markdown cell first, add a title and purpose, then press Shift + Enter to render it. Markdown is used for headings, explanations, and result notes."

**Creating and running a Code cell (0:45 - 1:15)**
"Now I create a Code cell, write `print(\"Hello from a Code cell\")`, and run it with Shift + Enter. The output appears below the cell, confirming execution."

**Switching cell types (1:15 - 1:35)**
"To switch cell types, I use the toolbar dropdown and change between Markdown and Code. This keeps the notebook clean: explanation in Markdown, execution in Code."

**Second code example and interpretation (1:35 - 2:00)**
"I run a second Code cell for simple math, then add a Markdown cell to explain the output. This is the expected submission pattern: explanation, code, then interpretation."

## PR Section: Kernel Control Proof

### Running Cells & Execution Order

- Cell 1 (run first):

```python
x = 10
print("x =", x)
```

- Expected output:

```text
x = 10
```

- Cell 2 (depends on Cell 1):

```python
print("x + 5 =", x + 5)
```

- Expected output:

```text
x + 5 = 15
```

- If Cell 2 is run before Cell 1, expected error:

```python
print(x)
```

```text
NameError: name 'x' is not defined
```

### Restarting the Kernel

- Action: **Kernel -> Restart Kernel**, then run:

```python
print(x)
```

- Expected outcome after restart:

```text
NameError: name 'x' is not defined
```

- Proof point: Restart clears variables and execution state.

### Interrupting Execution

- Run this cell:

```python
while True:
    pass
```

- Action: **Kernel -> Interrupt Kernel**
- Expected outcome: cell stops running and kernel becomes responsive again.

### When to Use Restart vs Interrupt

- Use **Interrupt** when one cell is stuck (infinite loop/long run) and you want to stop only current execution.
- Use **Restart** when notebook state is inconsistent or you need a clean run from the top.

### Conclusion

- Cell execution depends on order.
- Kernel restart clears memory (variables are removed).
- Kernel interrupt safely stops a running cell.
- Kernel control basics are verified for notebook workflow.

### 2-Minute Video Script (Kernel Run/Restart/Interrupt)

**Running cells (0:00 - 0:40)**
"I first run a cell that defines `x = 10`, then run a second cell that uses `x`. The output is correct, showing execution order is working. If I run the second cell first, I get a NameError, which proves cell dependency."

**Restarting kernel (0:40 - 1:20)**
"Now I restart the kernel from the Kernel menu. After restart, I run `print(x)` again and get `NameError: name 'x' is not defined`. This confirms restart clears all previously stored variables."

**Interrupting execution (1:20 - 1:50)**
"Next, I run an infinite loop with `while True: pass`. The notebook keeps running, so I use Kernel -> Interrupt Kernel. Execution stops immediately and the notebook is responsive again."

**Difference summary (1:50 - 2:00)**
"Interrupt stops the current running cell. Restart resets the full kernel state. Both are essential for clean and controlled notebook execution."

## PR Section: Markdown Headings, Lists, and Code Blocks (Notebook Proof)

### Notebook File

- `Jupyter_Markdown_Formatting_Demo.ipynb`

### Markdown Elements Demonstrated

- **Main Markdown title** using `#`
- **Subheadings** using `##` and `###`
- **Unordered list** using `-`
- **Ordered list** using numbered steps
- **Inline code** such as `print()`
- **Code block inside Markdown** using triple backticks

### Notebook Flow (Submission Structure)

- **Markdown cell:** purpose and formatted content
- **Code cell:** simple Python execution
- **Markdown cell:** output explanation

### Cell Snapshot

**Markdown cell**

```markdown
# Markdown Formatting Demo for PR Submission

## Purpose
This notebook demonstrates proper Markdown usage in Jupyter for headings, lists, inline code, and code blocks.

### Key Items Covered
- Main title and section subheadings
- Unordered and ordered lists
- Inline code such as `print()`
- Code block formatting in Markdown

### Steps Followed
1. Create Markdown cell and add structured content.
2. Add a simple Code cell and run it.
3. Add Markdown output explanation.

### Markdown Code Block Example
```python
name = "Data Science"
print("Hello", name)
```
```

**Code cell**

```python
message = "Markdown + Code flow is working"
print(message)
```

**Markdown output explanation**

```markdown
Expected output:
- `Markdown + Code flow is working`
```

### 2-Minute Video Script (Markdown Formatting)

**Creating Markdown cell (0:00 - 0:30)**
"I start by creating a Markdown cell and adding a main title and subheadings to organize the notebook clearly."

**Writing headings and lists (0:30 - 1:00)**
"Next, I add an unordered list for key points and an ordered list for steps. This makes the notebook easy to follow during review."

**Adding inline code and code block (1:00 - 1:25)**
"I include inline code like `print()` inside text, and then add a fenced code block in Markdown to show formatted sample code."

**Switching between Markdown and Code (1:25 - 1:45)**
"I switch from Markdown to a Code cell, run a simple print statement, and then switch back to Markdown for output explanation."

**Why Markdown matters (1:45 - 2:00)**
"Markdown keeps notebooks readable and professional. It separates explanation from execution, which improves clarity in PR submissions."

## PR Section: Data Science Project Folder Structure

### Recommended Structure

```text
project-name/
│── data/
│   ├── raw/
│   └── processed/
│── notebooks/
│── src/
│── outputs/
│   ├── figures/
│   └── reports/
│── README.md
```

### Folder Purpose (What + Why)

- `data/raw/`
  - **Stores:** Original source files exactly as collected.
  - **Why:** Keeps source data unchanged for traceability and reproducibility.

- `data/processed/`
  - **Stores:** Cleaned or transformed datasets ready for analysis/modeling.
  - **Why:** Separates preprocessing results from original raw files.

- `notebooks/`
  - **Stores:** Jupyter notebooks for EDA, experiments, and quick validation.
  - **Why:** Keeps exploratory work organized and separate from reusable code.

- `src/`
  - **Stores:** Reusable Python scripts/modules (data prep, features, training, evaluation).
  - **Why:** Prevents logic duplication and improves maintainability.

- `outputs/figures/`
  - **Stores:** Charts, plots, and visual artifacts.
  - **Why:** Central place for visual results used in reports and PRs.

- `outputs/reports/`
  - **Stores:** Summaries, findings, and final project documents.
  - **Why:** Keeps communication artifacts separate from code and data.

- `README.md`
  - **Stores:** Project overview, structure, and usage notes.
  - **Why:** First reference point for reviewers and collaborators.

### Best Practices

- Do not edit files inside `data/raw/` after ingestion.
- Use clear, relative paths (avoid hardcoded local machine paths).
- Keep code in `src/`, not inside notebooks only.
- Save final visuals in `outputs/figures/` and summaries in `outputs/reports/`.
- Keep folder names simple and lowercase for consistency.

### 2-Minute Video Script (Folder Structure)

**Root overview (0:00 - 0:25)**
"This is my data science project root. It keeps data, notebooks, source code, and outputs clearly separated for clean workflow and easier review."

**Data folders (0:25 - 0:55)**
"Inside `data`, I use `raw` for original source files and `processed` for cleaned versions. This avoids accidental overwrites and keeps preprocessing steps reproducible."

**Work folders (0:55 - 1:25)**
"`notebooks` is for exploratory analysis and experiment notes. `src` is for reusable scripts and functions. This separation keeps experiments and production-style code organized."

**Output folders (1:25 - 1:45)**
"`outputs/figures` stores plots, and `outputs/reports` stores written findings. This makes final artifacts easy to find during PR review."

**Collaboration value (1:45 - 2:00)**
"This structure helps collaboration because every contributor knows where data, code, and results belong, reducing confusion and merge issues."

