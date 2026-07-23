#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
from build_mca_db import get_mca_telem_json
from write_output_json import get_json
from filter_mca_db import get_filtered_json
from mitre_tech_patterns import list_all_malware, list_all_groups
from plot_mca import get_sankey
import argparse

def main():
    mca_telemetry_json = []
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

    # Default filters (mean for both technique and channel)
    python main.py -e punchtrack -p windows

    # Bypass both filters (keep everything)
    python main.py -e punchtrack -p windows --channel-top 0 --technique-top 0

    # Keep top 5 channels + mean techniques
    python main.py -e "volt typhoon" -p windows --channel-top 5

    # Keep top 10 techniques + top 3 channels
    python main.py -e APT29 -p windows --technique-top 10 --channel-top 3
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
        "--channel-top",
        type=int,
        default=None,
        help="Filter log_source_channel:\n"
             "  None = keep count >= mean (default)\n"
             "  0    = keep all\n"
             "  N    = keep top N"
    )

    parser.add_argument(
        "--technique-top",
        type=int,
        default=None,
        help="Filter technique_name:\n"
             "  None = keep count >= mean (default)\n"
             "  0    = keep all\n"
             "  N    = keep top N"
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
    get_json(mca_telemetry_json, "mca_db.json")

    mca_telemetry_json = get_filtered_json(
        mca_telemetry_json, args.channel_top, args.technique_top
    )  
    get_json(mca_telemetry_json, "filtered_mca_db.json")
    
    get_sankey(mca_telemetry_json)

if __name__ == "__main__":
    main()