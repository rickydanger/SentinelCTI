#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
import argparse

from src.write_json import get_json
from src.filter_db import get_filtered_json
from src.plot_mca import get_sankey
from src.config_db import load_config
from src.list_entities import get_entities_list
from src.last_db import get_last_db
from src.new_db import get_new_db

def main():
    mitre_data = MitreAttackData("enterprise-attack.json")
    config = load_config()

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

    # Quickly return the last run
    python main.py -l

    # Use a specific existing database file
    python main.py -d my_old_db.json

    # Keep only the top 10 techniques
    python main.py -e APT29 -p windows -t 10

    # Return last run and keep top 5 techniques
    python main.py -l -t 5
"""
    )

    parser.add_argument("-e", "--entities", nargs="+",
                        help="Malware/APT names, or use 'malware' / 'groups' to list all")
    parser.add_argument("-p", "--platform",
                        help="Platform (e.g. windows). Required when extracting new data.")
    parser.add_argument("-l", "--last", action="store_true",
                        help="Return the last database from the config file")
    parser.add_argument("-d", "--db",
                        help="Path to an existing mca database file to use")
    parser.add_argument("-t", "--technique-top", type=int, default=None,
                        help="Filter technique_name (None=median, 0=all, N=top N)")

    args = parser.parse_args()

    # === Get Entities ===
    if get_entities_list(args, mitre_data):
        return

    # === Get last database ===
    if args.last or args.db:
        mca_telem_json = get_last_db(args, config)
        if mca_telem_json is None:
            return

    # === Get new telemetry data from MITRE ===
    else:
        mca_telem_json = get_new_db(args, mitre_data, config)
        if mca_telem_json is None:
            return

    # === Filter + Sankey ===
    mca_telem_json = get_filtered_json(mca_telem_json, args.technique_top)
    get_json(mca_telem_json, "filtered_mca_db.json")

    get_sankey(mca_telem_json)


if __name__ == "__main__":
    main()