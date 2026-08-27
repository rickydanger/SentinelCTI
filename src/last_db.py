import json
import os

DATA_DIR = "data\\mcadbs"


def _resolve_db_path(path):
    """Use the path as-is if it exists; otherwise look under data/."""
    if path is None:
        return None
    if os.path.isabs(path) or os.path.exists(path):
        return path
    under_data = os.path.join(DATA_DIR, os.path.basename(path))
    return under_data


def _load_json(path):
    if not os.path.exists(path):
        print(f"Error: Database file '{path}' not found.")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_last_db(args, config):
    """
    Load database(s) via --last or --db.
    --last reads mca_config.json and concatenates each entity JSON.
    --db still accepts a single file.
    """
    paths = []

    if args.last:
        if not config.get("last_run"):
            print("No previous run found in config. Please extract data first.")
            return None

        last_name = config["last_run"]
        entry = config["configs"].get(last_name)

        if not entry:
            print(f"Config entry '{last_name}' not found.")
            return None

        paths = entry.get("mca_db_paths")
        if not paths:
            old = entry.get("mca_db_path")
            paths = [old] if old else []

        print(f"Reusing last run → {last_name}")
        print(f"Entities: {', '.join(entry.get('entities', []))}")
        print(f"Databases: {', '.join(paths)}")
    else:
        paths = [args.db]
        print(f"Using specified database → {args.db}")

    combined = []
    for path in paths:
        resolved = _resolve_db_path(path)
        data = _load_json(resolved)
        if data is None:
            return None
        if isinstance(data, list):
            combined.extend(data)
        else:
            print(f"Error: '{resolved}' is not a list of records.")
            return None
        print(f"  Loaded {len(data)} records from {resolved}")

    return combined
