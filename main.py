#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
from build_mca_telem_json import get_mca_telem_json
from create_json_file import get_json
from filter_mca_telem_json import get_filtered_json
from mca_telem_plotly_charts import get_sankey
import argparse

def main():
    mca_telemetry_json = []
    mitre_data = MitreAttackData("enterprise-attack.json")

    parser = argparse.ArgumentParser(
        description="Generate Sankey diagram from MITRE ATT&CK telemetry data"
    )

    parser.add_argument(
        "-m", "--malware",
        nargs="+",                    # Accepts one or more malware names
        required=True,
        help="One or more malware names (e.g. punchtrack blackenergy)"
    )

    parser.add_argument(
        "-p", "--platform",
        required=True,
        help="Platform (e.g. windows, linux, macos)"
    )

    parser.add_argument(
        "-t", "--top",
        type=int,
        default=None,
        help="Top N most frequent log_source_channel to keep (default: keep all)"   
    )

    args = parser.parse_args()

    # You can later expand this to support more platforms
    if args.platform.lower() != "windows":
        print("Currently only 'windows' platform is supported.")
        return

    mca_telemetry_json = get_mca_telem_json(args.malware, args.platform, mitre_data)

    mca_telemetry_json = get_filtered_json(mca_telemetry_json, args.top)
    get_json(mca_telemetry_json)

    get_sankey(mca_telemetry_json)

if __name__ == "__main__":
    main()