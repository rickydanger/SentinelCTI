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


def make_entity_db_name(entity):
    """
    One database file per entity.
    Example: "volt typhoon" → "volt_typhoon_mcadb.json"
    """
    clean = entity.strip().lower().replace(" ", "_")
    return f"{clean}_mcadb.json"


def make_run_name(entities):
    """
    Config key for a multi-entity run (first 5 letters each, spaces removed).
    Example: ["volt typhoon", "apt29"] → "voltt_apt29"
    """
    parts = []
    for name in entities:
        clean = name.lower().replace(" ", "")
        parts.append(clean[:5])
    return "_".join(parts)
