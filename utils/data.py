import pandas as pd
import os
from io import StringIO

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Input file not found")

    try:
        # Step 1: read raw lines
        with open(path, "r") as f:
            lines = f.readlines()

        if not lines:
            raise ValueError("CSV file is empty")

        # Step 2: remove surrounding quotes from each line
        cleaned_lines = [line.strip().strip('"') for line in lines]

        # Step 3: convert back to CSV format
        cleaned_csv = "\n".join(cleaned_lines)

        # Step 4: read with pandas
        df = pd.read_csv(StringIO(cleaned_csv))

    except Exception as e:
        raise ValueError(f"Invalid CSV format: {str(e)}")

    if df.empty:
        raise ValueError("Dataset has no rows")

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    if "close" not in df.columns:
        raise ValueError(f"Missing required column: 'close'. Found columns: {list(df.columns)}")

    return df