# MLOps Batch Signal Pipeline

## Overview

This project implements a minimal **MLOps-style batch pipeline** for generating trading signals from OHLCV data.

It is designed to demonstrate **production-oriented engineering principles**:

* Reproducibility via configuration and deterministic execution
* Observability through structured logging and metrics
* Deployment readiness using Docker

---

## Tech Stack

* Python 3.9
* pandas
* numpy
* PyYAML
* Docker

---

## Key Features

### Reproducibility

* YAML-based configuration (`config.yaml`)
* Deterministic runs using fixed random seed

### Observability

* Structured logs with full execution trace (`run.log`)
* Machine-readable metrics output (`metrics.json`)
* Run-level traceability using unique Run IDs

### Robust Data Handling

* Handles malformed CSV formats (quoted rows, delimiter inconsistencies)
* Schema validation and required column checks (`close`)
* Clear, actionable error messages

### Deployment Ready

* Fully Dockerized pipeline
* One-command execution
* No hardcoded paths (CLI-driven)

---

## Dataset

The input dataset (`data.csv`) contains OHLCV (Open, High, Low, Close, Volume) data with ~10,000 rows.

* Only the `close` column is used for signal computation
* Additional columns are preserved for completeness but not used in processing
* The pipeline validates schema and handles inconsistencies in input format

---

## Pipeline Workflow

1. Load and validate configuration (YAML)
2. Load and validate dataset (CSV)
3. Compute rolling mean on `close`
4. Generate binary signal:

   * `1` if `close > rolling_mean`
   * `0` otherwise
5. Compute metrics:

   * `rows_processed`
   * `signal_rate`
   * `latency_ms`

---

## Setup (Local Environment)

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

2. Activate the environment:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Local Execution

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Docker Execution

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

---

## Example Output (`metrics.json`)

```json
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 17,
  "seed": 42,
  "status": "success"
}
```

---

## Logging (`run.log`)

The pipeline provides detailed logs including:

* Job start and end timestamps
* Run metadata (Run ID, input/config paths)
* Config validation details
* Dataset schema and row counts
* Processing steps and transformations
* Metrics summary
* Error traces (if any)

---

## Error Handling

The pipeline gracefully handles:

* Missing or invalid config files
* Empty or malformed CSV inputs
* Missing required columns (`close`)
* Runtime failures

A valid `metrics.json` is always generated — even in failure cases.

---

## Design Decisions

* **NaN Handling:** Initial `window-1` rows are dropped to ensure deterministic signal computation
* **Column Normalization:** Input columns are standardized to avoid schema inconsistencies
* **Robust CSV Ingestion:** Handles real-world formatting issues such as quoted rows and delimiter ambiguity
* **Separation of Concerns:** Modular structure (`utils/`) for maintainability and clarity

---

## Summary

This project demonstrates how to build a **clean, reproducible, and observable batch pipeline**, closely aligned with real-world MLOps workflows used in data and trading systems.
