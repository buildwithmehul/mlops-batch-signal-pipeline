import argparse
import time
import json
import numpy as np
import logging
import sys
import uuid

from utils.config import load_config
from utils.data import load_data
from utils.processing import compute_signal
from utils.metrics import compute_metrics
from utils.logger import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(description="MLOps Batch Job")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    setup_logger(args.log_file)

    # 🔥 Run metadata (NEW - HIGH IMPACT)
    run_id = str(uuid.uuid4())[:8]
    logging.info("========== JOB STARTED ==========")
    logging.info(f"Run ID: {run_id}")
    logging.info(f"Input file: {args.input}")
    logging.info(f"Config file: {args.config}")

    start_time = time.time()

    try:
        # ---------------- CONFIG ----------------
        config = load_config(args.config)
        logging.info(
            f"Config validated | seed={config['seed']} | window={config['window']} | version={config['version']}"
        )

        # Determinism
        np.random.seed(config["seed"])
        logging.info(f"Random seed set to {config['seed']}")

        # ---------------- DATA ----------------
        df = load_data(args.input)
        logging.info(f"Dataset loaded successfully | rows={len(df)}")

        # 🔥 Column logging (NEW - HIGH IMPACT)
        logging.info(f"Columns detected: {list(df.columns)}")

        # ---------------- PROCESSING ----------------
        logging.info(f"Computing rolling mean with window={config['window']}")

        before_rows = len(df)

        df = compute_signal(df, config["window"])

        after_rows = len(df)

        logging.info(
            f"Rows before processing: {before_rows}, after dropna: {after_rows}"
        )
        logging.info("Dropped initial NaN rows from rolling mean (for deterministic signal computation)")
        logging.info("Signal generation completed successfully")

        # ---------------- METRICS ----------------
        end_time = time.time()

        rows, signal_rate, latency = compute_metrics(df, start_time, end_time)

        result = {
            "version": config["version"],
            "rows_processed": rows,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency,
            "seed": config["seed"],
            "status": "success"
        }

        logging.info(f"Metrics computed successfully: {result}")

        exit_code = 0

    except Exception as e:
        logging.exception("Pipeline execution failed")

        result = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        exit_code = 1

    # ---------------- OUTPUT ----------------
    try:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        logging.info(f"Metrics written to {args.output}")
    except Exception as write_err:
        logging.error(f"Failed to write metrics file: {write_err}")

    # Print to stdout (Docker requirement)
    print(json.dumps(result, indent=2))

    logging.info("========== JOB FINISHED ==========")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()