# MLOps Batch Signal Pipeline

## Overview

This project implements a minimal MLOps-style batch pipeline for generating trading signals from OHLCV data.
It is designed with a focus on reproducibility, observability, and deployment readiness.

---

## Features

* **Reproducibility**

  * Config-driven execution via YAML
  * Deterministic runs using fixed random seed

* **Observability**

  * Structured logging with execution trace
  * Machine-readable metrics output (JSON)

* **Robust Data Handling**

  * Handles malformed CSV formats (quoted rows, delimiter issues)
  * Validates schema and required columns

* **Deployment Ready**

  * Fully Dockerized
  * One-command execution

---

## Pipeline Steps

1. Load and validate configuration (YAML)
2. Load and validate dataset (CSV)
3. Compute rolling mean on `close`
4. Generate binary signal:

   * `1` if close > rolling_mean
   * `0` otherwise
5. Compute metrics:

   * rows_processed
   * signal_rate
   * latency_ms

---

## Local Run

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Docker Run

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

---

## Example Output

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

## Error Handling

The pipeline gracefully handles:

* Missing or invalid config files
* Empty or malformed CSVs
* Missing required columns
* Runtime failures (always outputs metrics JSON)

---

## Tech Stack

* Python 3.9
* pandas
* numpy
* PyYAML
* Docker

---

## Notes

* Rolling mean drops initial `window-1` rows to ensure deterministic signal computation.
* Column normalization ensures robustness against inconsistent input formats.
* Implemented robust CSV ingestion to handle real-world data inconsistencies such as quoted rows and delimiter ambiguity.