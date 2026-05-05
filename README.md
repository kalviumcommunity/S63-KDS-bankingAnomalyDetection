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

## PR Section: Data Organization (Raw vs Processed vs Outputs)

### Recommended Structure

```text
project-name/
│── data/
│   ├── raw/
│   └── processed/
│── outputs/
│   ├── figures/
│   ├── reports/
│   └── models/
```

### Folder Meaning

- `data/raw/`
  - Original source files exactly as received.
  - Read-only zone; never edit these files directly.

- `data/processed/`
  - Cleaned, transformed, and analysis-ready files.
  - Built from raw data through preprocessing steps.

- `outputs/figures/`
  - Generated visual artifacts (charts, plots, dashboards exports).

- `outputs/reports/`
  - Generated written summaries and final documents.

- `outputs/models/`
  - Generated trained model artifacts and saved model files.

### Data Flow Rules

- Never modify files in `data/raw/`.
- Always read from `data/raw/`.
- Always write cleaned results to `data/processed/`.
- Always write generated artifacts to `outputs/`.
- Maintain one-directional flow: `raw -> processed -> outputs`.

### File Examples

- `data/raw/original.csv`
- `data/processed/cleaned_data.csv`
- `outputs/figures/plot.png`
- `outputs/reports/report.pdf`
- `outputs/models/model.pkl`

### Why Separation Matters

- Prevents accidental overwrite of source data.
- Keeps transformations traceable and reproducible.
- Makes collaboration easier because each stage has a fixed location.

### 2-Minute Video Script (Data Organization)

**Folder walkthrough (0:00 - 0:45)**
"This project separates data into clear stages. `data/raw` holds original files, `data/processed` holds cleaned files, and `outputs` stores generated results like figures, reports, and models."

**Why separation matters (0:45 - 1:25)**
"I treat `raw` as read-only. All transformations happen into `processed`, and all final artifacts go to `outputs`. This makes the pipeline clean, reproducible, and easy to review in PRs."

**Risks of mixing stages (1:25 - 2:00)**
"If stages are mixed, source data can be overwritten, outputs become hard to trace, and debugging becomes difficult. Keeping a one-directional flow from raw to processed to outputs avoids these issues."

## PR Section: Basic Python Analysis Script

### Script Location

- `analysis.py` (project root)

### What the Script Does

- Defines simple variables and sample data.
- Uses a list and dictionary.
- Calculates total, average, highest, and lowest values.
- Prints a clear data summary in terminal output.

### Run Command

```bash
python analysis.py
```

### Expected Output

```text
Basic Analysis Summary
----------------------
Class: data_science_basics
Student Count: 5
Scores: [72, 85, 90, 68, 95]
Total Score: 410
Average Score: 82.00
Highest Score: 95
Lowest Score: 68
```

### Script vs Notebook (Practical Difference)

- **Script (`.py`)**
  - Best for repeatable execution from terminal.
  - Good for automation and shared workflows.
  - Output is linear and easy to version in code reviews.

- **Notebook (`.ipynb`)**
  - Best for interactive exploration and step-by-step analysis.
  - Useful for combining notes, code, and outputs in one place.
  - Better for experimentation, less ideal for repeated automation.

### 2-Minute Video Script (analysis.py)

**Show script file (0:00 - 0:35)**
"This is `analysis.py` in the project root. It contains simple sample data, basic calculations, and clear print statements for a small analysis summary."

**Run script in terminal (0:35 - 1:05)**
"I run the script using `python analysis.py`. The script executes directly in terminal and prints the summary output."

**Explain output (1:05 - 1:35)**
"The output shows class name, student count, score list, total score, average, highest, and lowest score. This confirms the script logic and formatting are working."

**Why scripts are useful (1:35 - 2:00)**
"Scripts are useful for repeatable analysis tasks and automation. Unlike notebooks, scripts run consistently from terminal and are easier to include in production-style workflows."

## PR Section: Numeric and String Data Types in Python

### Script Location

- `data_types_demo.py` (project root)

### Numeric vs String Types (Short)

- **Numeric types (`int`, `float`)** are used for arithmetic.
- **String type (`str`)** is used for text values and concatenation.

### Code Snippets

```python
age = 21
height = 5.7
print(type(age))      # <class 'int'>
print(type(height))   # <class 'float'>
print(age + 4)        # 25
print(age / 2)        # 10.5
```

```python
first_name = "Data"
last_name = "Student"
full_name = first_name + " " + last_name
print(full_name)      # Data Student
```

```python
# Common mistake:
# "Age: " + age   -> TypeError (str + int)

# Correct conversion:
print("Age: " + str(age))
print(int("10") + 5)
```

### Expected Output

```text
Numeric Examples
----------------
age = 21 | type: <class 'int'>
height = 5.7 | type: <class 'float'>
total_points = 25
half_age = 10.5

String Examples
---------------
first_name = Data | type: <class 'str'>
full_name = Data Student

Mixing Types
------------
Common mistake: trying to add string + int directly
Example error: "Age: " + age -> TypeError
Correct conversion: Age: 21
int("10") + 5 = 15
```

### Common Mistake (Mixing Types)

- Directly combining string and integer causes `TypeError`.
- Convert numeric to string with `str()` for text output.
- Convert numeric text to number with `int()` when calculation is needed.

### 2-Minute Video Script (Numeric vs String)

**Numeric examples (0:00 - 0:35)**
"I start with numeric variables like `age` as an integer and `height` as a float. I run addition and division to show arithmetic behavior."

**String examples (0:35 - 1:05)**
"Next, I create two string variables and concatenate them to form a full name. This shows how strings are used for text operations."

**Type conversion (1:05 - 1:35)**
"Then I show a common mistake: mixing string and integer directly causes a TypeError. I fix it using `str(age)`. I also convert text to number using `int(\"10\")`."

**Difference summary (1:35 - 2:00)**
"Numeric types are for calculations, string types are for text. Type conversion is important when moving between display output and arithmetic operations."

## PR Section: Lists, Tuples, and Dictionaries in Python

### Script Location

- `data_structures_demo.py` (project root)

### What the Script Demonstrates

- **List:** create, access, modify, add, and remove elements
- **Tuple:** create, access elements, and show immutability behavior
- **Dictionary:** create key-value pairs, access values, update existing key, and add new key

### Code Snapshot

```python
# List
names = ["Asha", "Ravi", "Meera"]
print(names[0])       # access
names[1] = "Rohan"    # modify
names.append("Nina")  # add
names.pop(0)          # remove

# Tuple
coordinates = (10.5, 20.3)
print(coordinates[0])  # access
# coordinates[0] = 99.9  # TypeError (immutable)

# Dictionary
student = {"name": "Asha", "age": 20, "course": "Data Science"}
print(student["name"])  # access
student["age"] = 21     # update
student["city"] = "Pune"  # add new key
```

### Expected Output

```text
List Demo
---------
Original list: ['Asha', 'Ravi', 'Meera']
First element: Asha
After modify/add/remove: ['Rohan', 'Meera', 'Nina']
Removed element: Asha

Tuple Demo
----------
Tuple value: (10.5, 20.3)
First coordinate: 10.5
Attempted change: coordinates[0] = 99.9 -> TypeError (tuple is immutable)

Dictionary Demo
---------------
Original dictionary: {'name': 'Asha', 'age': 20, 'course': 'Data Science'}
Student name: Asha
Updated dictionary: {'name': 'Asha', 'age': 21, 'course': 'Data Science', 'city': 'Pune'}
```

### Difference and Use Cases (Short)

- **List (mutable):** use when items may change (add/remove/update).
- **Tuple (immutable):** use for fixed values (coordinates, constants).
- **Dictionary (key-value):** use when data needs labels (student/product details).

### 2-Minute Video Script (List, Tuple, Dictionary)

**List operations (0:00 - 0:40)**
"I start with a list of names, access the first value, then modify one item, append a new name, and remove one element. This shows list mutability in practice."

**Tuple immutability (0:40 - 1:15)**
"Next, I create a tuple for coordinates and access an element. I also explain that changing a tuple element causes a TypeError because tuples are immutable."

**Dictionary usage (1:15 - 1:45)**
"Then I create a dictionary for student info, access values using keys, update the age, and add a new city key."

**Difference summary (1:45 - 2:00)**
"List is mutable, tuple is immutable, and dictionary stores labeled key-value data. Each is used based on whether data changes and whether labels are needed."

## PR Section: Conditional Statements in Python

### Script Location

- `conditionals_demo.py` (project root)

### What is Covered (Short)

- `if` checks a condition and runs code when it is true.
- `elif` checks another condition if previous one is false.
- `else` runs when no earlier condition is true.

### Logical Operators (Short)

- `and` -> all conditions must be true
- `or` -> at least one condition must be true
- `not` -> reverses a condition

### Code Snippets

```python
# Basic if
num = 7
if num > 0:
    print("positive")

# if-else
temperature = -2
if temperature >= 0:
    print("above or equal to 0")
else:
    print("below 0")
```

```python
# if-elif-else
marks = 78
if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "D"
print(grade)
```

```python
# Logical operators
age = 20
attendance = 82
has_id_card = False

if age >= 18 and attendance >= 75:
    print("Eligible for exam")

if age < 18 or attendance < 75:
    print("Needs special approval")

if not has_id_card:
    print("ID card is missing")
```

### Expected Output

```text
Conditional Statements Demo
---------------------------
1) Basic if statement
7 is positive

2) if-else example
Temperature is below 0

3) if-elif-else example
Marks: 78, Grade: B

4) Logical operators
Using 'and': Eligible for exam
Using 'or': No special approval needed
Using 'not': ID card is missing
```

## PR Section: For and While Loops in Python

### Script Location

- `loops_demo.py` (project root)

### For vs While (Short)

- **for loop:** used when iterating over a known sequence (`range`, list).
- **while loop:** used when repetition depends on a condition.

### break and continue (Short)

- `break` stops the loop immediately.
- `continue` skips current iteration and moves to next one.

### Code Snippets

```python
# for loop with range
for number in range(1, 6):
    print(number)

# for loop with list
names = ["Asha", "Ravi", "Meera"]
for name in names:
    print("Name:", name)
```

```python
# continue example
for value in range(1, 6):
    if value == 3:
        continue
    print("Value:", value)

# break example
for value in range(1, 8):
    if value == 4:
        print("Stopping loop at", value)
        break
    print("Value:", value)
```

```python
# while loop with safe termination
count = 1
while count <= 5:
    print("Count:", count)
    count += 1
print("Loop ended safely")
```

### Expected Output

```text
Loops Demo
----------
1) for loop with range (1 to 5)
1
2
3
4
5

2) for loop with list
Name: Asha
Name: Ravi
Name: Meera

3) continue example (skip value 3)
Value: 1
Value: 2
Value: 4
Value: 5

4) break example (stop at value 4)
Value: 1
Value: 2
Value: 3
Stopping loop at 4

5) while loop with safe termination
Count: 1
Count: 2
Count: 3
Count: 4
Count: 5
Loop ended safely
```

### Infinite Loop Note

- A `while` loop can run forever if the condition never becomes false.
- Avoid this by updating the loop variable (`count += 1`) or using a clear stop condition.

## PR Section: Python Functions

### Script Location

- `functions_demo.py` (project root)

### What Functions Are (Short)

- Functions are reusable code blocks created using `def`.
- They help avoid repetition and keep logic organized.

### Parameters vs Arguments (Short)

- **Parameters** are variables in the function definition.
- **Arguments** are actual values passed during function call.

### Code Snippets

```python
def show_welcome():
    print("Welcome to the Python functions demo")

def calculate_sum(a, b):
    result = a + b
    return result

def check_even_odd(number):
    if number % 2 == 0:
        return "even"
    return "odd"
```

```python
show_welcome()                    # no parameters
total = calculate_sum(12, 8)      # arguments: 12, 8
print(total)
print(check_even_odd(7))
```

### Expected Output

```text
Functions Demo
--------------
Welcome to the Python functions demo
Sum of 12 and 8 is 20
7 is odd
Global variable example: functions_pr_demo
```

### Local vs Global Scope (Short)

- `project_name` in the script is a **global variable** (available outside functions).
- `result` inside `calculate_sum()` is a **local variable** (used only inside that function).

