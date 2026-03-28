import yaml

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # 🚨 CRITICAL FIX
    if config is None:
        raise ValueError("Config file is empty or invalid YAML")

    required = ["seed", "window", "version"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    return config