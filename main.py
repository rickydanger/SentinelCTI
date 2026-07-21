#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
from build_mca_telem_json import get_mca_telem_json
from create_json_file import get_json
from filter_mca_telem_json import get_filtered_json
from mitre_tech_patterns import list_all_malware, list_all_groups
from mca_telem_plotly_charts import get_sankey
import argparse

def main():
    mca_telemetry_json = []
    mitre_data = MitreAttackData("enterprise-attack.json")

    parser = argparse.ArgumentParser(
    description="Generate a Sankey diagram from MITRE ATT&CK telemetry data (malware & APTs).",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""
    Notes:
    - If a malware or group name contains spaces, you must wrap it in quotes.
        Example: "volt typhoon", "Lazarus Group"

    Examples:
    # List all malware
    python main.py -e malware

    # List all groups / APTs
    python main.py -e groups

    # Process a single entity
    python main.py -e punchtrack -p windows

    # Process multiple entities (use quotes for names with spaces)
    python main.py -e punchtrack "volt typhoon" APT29 -p windows

    # Keep only the top 5 most frequent log source channels
    python main.py -e "volt typhoon" -p windows -t 5
    """
    )

    parser.add_argument(
        "-e", "--entities",
        nargs="+",
        required=True,
        help="Malware/APT names, or use 'malware' / 'groups' to list all"
    )

    parser.add_argument(
        "-p", "--platform",
        required=False,
        help="Platform (e.g. windows, linux)"
    )

    parser.add_argument(
        "-t", "--top",
        type=int,
        default=None,
        help="Top N most frequent log_source_channel to keep (default: keep all)"   
    )

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

    # === Normal processing ===
    if not args.platform:
        print("Error: --platform is required when processing entities.")
        return

    if args.platform.lower() != "windows":
        print("Currently only 'windows' platform is supported.")
        return

    mca_telemetry_json = get_mca_telem_json(args.entities, args.platform, mitre_data)
    mca_telemetry_json = get_filtered_json(mca_telemetry_json, args.top)
    
    get_json(mca_telemetry_json)
    get_sankey(mca_telemetry_json)

if __name__ == "__main__":
    main()