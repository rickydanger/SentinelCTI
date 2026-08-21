import json
import os

def get_last_db(args, config):
    """Load a database via --last or --db. Returns the data or None on error."""
    if args.last:
        if not config.get("last_run"):
            print("No previous run found in config. Please extract data first.")
            return None

        last_name = config["last_run"]
        entry = config["configs"].get(last_name)

        if not entry:
            print(f"Config entry '{last_name}' not found.")
            return None

        db_path = entry["mca_db_path"]
        print(f"Reusing last run → {last_name}")
        print(f"Database: {db_path}")
        print(f"Entities: {', '.join(entry['entities'])}")
    else:
        db_path = args.db
        print(f"Using specified database → {db_path}")

    full_path = os.path.join("data", db_path)

    if not os.path.exists(full_path):
        print(f"Error: Database file '{full_path}' not found.")
        return None

    with open(full_path, "r") as f:
        return json.load(f)