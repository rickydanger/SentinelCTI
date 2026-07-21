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
        description="Generate Sankey diagram from MITRE ATT&CK telemetry data"
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