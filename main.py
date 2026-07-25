#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
from build_mca_db import get_mca_telem_json
from write_output_json import get_json
from filter_mca_db import get_filtered_json
from mitre_tech_patterns import list_all_malware, list_all_groups
from plot_mca import get_sankey
import argparse
import json
import os
from datetime import datetime

CONFIG_FILE = "mca_config.json"


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


def main():
    mitre_data = MitreAttackData("enterprise-attack.json")

    parser = argparse.ArgumentParser(
        description="Generate a Sankey diagram from MITRE ATT&CK telemetry data (malware & APTs).",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Notes:
  - If a malware or group name contains spaces, wrap it in quotes.
    Example: "volt typhoon", "Lazarus Group"

    Examples:
    # List all malware
    python main.py -e malware

    # List all groups / APTs
    python main.py -e groups

    # Extract new data (filename is automatic)
    python main.py -e "volt typhoon" APT29 -p windows

    # Quickly reuse the last run
    python main.py -r

    # Use a specific existing database file
    python main.py -d my_old_db.json

    # Keep only the top 10 techniques
    python main.py -e APT29 -p windows -t 10

    # Reuse last run and keep top 5 techniques
  python main.py -r -t 5
"""
    )

    parser.add_argument("-e", "--entities", nargs="+",
                        help="Malware/APT names, or use 'malware' / 'groups' to list all")
    parser.add_argument("-p", "--platform",
                        help="Platform (e.g. windows). Required when extracting new data.")
    parser.add_argument("-r", "--reuse", action="store_true",
                        help="Reuse the last database from the config file")
    parser.add_argument("-d", "--db",
                        help="Path to an existing mca database file to use")
    parser.add_argument("-t", "--technique-top", type=int, default=None,
                        help="Filter technique_name (None=median, 0=all, N=top N)")
    
    args = parser.parse_args()

    # === List mode ===
    if args.entities == ["malware"]:
        print("Listing all malware...\n")
        for name, mid in list_all_malware(mitre_data):
            print(f"{name:<45} | {mid}")
        return

    if args.entities == ["groups"]:
        print("Listing all groups / APTs...\n")
        for name, gid in list_all_groups(mitre_data):
            print(f"{name:<45} | {gid}")
        return

    config = load_config()

    # === Reuse existing database ===
    if args.reuse or args.db:
        if args.reuse:
            if not config.get("last_run"):
                print("No previous run found in config. Please extract data first.")
                return

            last_name = config["last_run"]
            entry = config["configs"].get(last_name)

            if not entry:
                print(f"Config entry '{last_name}' not found.")
                return

            db_path = entry["mca_db_path"]
            print(f"Reusing last run → {last_name}")
            print(f"Database: {db_path}")
            print(f"Entities: {', '.join(entry['entities'])}")
        else:
            db_path = args.db
            print(f"Using specified database → {db_path}")

        if not os.path.exists(db_path):
            print(f"Error: Database file '{db_path}' not found.")
            return

        with open(db_path, "r") as f:
            mca_telem_json = json.load(f)

    # === Extract new data from MITRE ===
    else:
        if not args.entities:
            print("Error: --entities is required when not using --reuse or --db")
            return

        if not args.platform:
            print("Error: --platform is required when extracting new data.")
            return

        if args.platform.lower() != "windows":
            print("Currently only 'windows' platform is supported.")
            return

        db_name = make_db_name(args.entities)

        print(f"Extracting data for: {args.entities}")
        mca_telem_json = get_mca_telem_json(args.entities, args.platform, mitre_data)

        get_json(mca_telem_json, db_name)
        print(f"Database saved → {db_name}")

        config_name = db_name.replace("_db.json", "")

        config["configs"][config_name] = {
            "mca_db_path": db_name,
            "entities": args.entities,
            "platform": args.platform,
            "created": datetime.now().isoformat(timespec="seconds")
        }
        config["last_run"] = config_name

        save_config(config)
        print(f"Config entry created → {config_name}")

    # === Filter + Sankey ===
    mca_telem_json = get_filtered_json(
        mca_telem_json, args.technique_top
    )
    get_json(mca_telem_json, "filtered_mca_db.json")

    get_sankey(mca_telem_json)


if __name__ == "__main__":
    main()