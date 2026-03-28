def compute_signal(df, window):
    df = df.copy()

    # Rolling mean
    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    # Drop NaNs (first window-1 rows)
    df = df.dropna()

    # Signal generation
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    return df