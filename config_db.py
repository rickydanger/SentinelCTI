import json
import os

CONFIG_FILE = os.path.join("data", "mca_config.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"last_run": None, "configs": {}}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved → {CONFIG_FILE}")


def make_db_name(entities):
    """
    Automatically create a database filename from entity names.
    Uses the first 5 characters of each name (spaces removed).
    Example: ["volt typhoon", "apt29"] → "voltt_apt29_db.json"
    """
    parts = []
    for name in entities:
        clean = name.lower().replace(" ", "")
        parts.append(clean[:5])
    return "_".join(parts) + "_db.json"