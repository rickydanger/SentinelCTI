#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
import argparse

from src.write_json import get_json
from src.filter_db import get_filtered_json
from src.plot_mca import get_sankey, get_table
from src.config_db import load_config
from src.list_entities import get_entities_list
from src.last_db import get_last_db
from src.new_db import get_new_db


def main():
    mitre_data = MitreAttackData("enterprise-attack.json")
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Generate a Sankey diagram or Table from MITRE ATT&CK telemetry data (malware & APTs).",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Notes:
  - Wrap names with spaces in quotes (e.g. "volt typhoon")

Examples:
  # List all malware / groups
  python main.py -e malware
  python main.py -e groups

  # Extract new data and show Sankey
  python main.py -e "volt typhoon" APT29 -p windows -v sankey

  # Use last run (Sankey or Table)
  python main.py -l -v sankey
  python main.py -l -v table

  # Use specific database
  python main.py -d my_old_db.json -v table

  # Filter techniques
  python main.py -l -t 10 -v sankey      # top 10
  python main.py -l -t 0 -v table        # no filter
"""
    )

    parser.add_argument("-e", "--entities", nargs="+",
                        help="Malware/APT names, or use 'malware' / 'groups' to list all")
    parser.add_argument("-p", "--platform",
                        help="Platform (e.g. windows). Required when extracting new data.")
    parser.add_argument("-l", "--last", action="store_true",
                        help="Use the last database from the config file")
    parser.add_argument("-d", "--db",
                        help="Path to an existing mca database file")
    parser.add_argument("-t", "--technique-top", type=int, default=None,
                        help="Filter technique_name (None=median, 0=all, N=top N)")
    parser.add_argument("-v", "--view", choices=["sankey", "table"], required=True,
                        help="Visualization type: sankey or table")

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

    # === Filter ===
    mca_telem_json = get_filtered_json(mca_telem_json, args.technique_top)
    get_json(mca_telem_json, "filtered_mca_db.json")

    # === Visualize ===
    if args.view == "table":
        get_table(mca_telem_json)
    else:
        get_sankey(mca_telem_json)


if __name__ == "__main__":
    main()