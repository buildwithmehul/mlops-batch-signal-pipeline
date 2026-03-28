def compute_metrics(df, start_time, end_time):
    rows = len(df)

    if rows == 0:
        signal_rate = 0.0
    else:
        signal_rate = df["signal"].mean()

    # Defensive latency (never negative)
    latency = max(0, int((end_time - start_time) * 1000))

    return rows, signal_rate, latency