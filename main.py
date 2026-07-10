#!/usr/bin/env python3

from html import parser

from mitreattack.stix20 import MitreAttackData
from create_json_file import get_json
from mitre_tech_patterns import get_techniques_for_malware,list_all_malware
from mitre_tech_analytics import get_analytics_for_technique
from mitre_log_sources import get_log_sources_for_analytic
from mca_telem_plotly_charts import get_sankey
import argparse
import sys

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
        "-t", "--threshold",
        type=int,
        default=1,
        help="Threshold for data source channels (default: 1)"
    )

    args = parser.parse_args()

    #DELETE LATER, pulling first malware name from list for now, can expand to support multiple later
    args.malware = args.malware[0]

    # You can later expand this to support more platforms
    if args.platform.lower() != "windows":
        print("Currently only 'windows' platform is supported.")
        return

    print("=== MITRE ATT&CK Orchestrator ===")

    #List all software
    if args.malware == "malware":
        print("Listing ALL MITRE ATT&CK Malware...\n")
        malware_list = list_all_malware()
        
        print(f"Found {len(malware_list)} malware entries:\n")
        print(f"{'NAME':<40} | ID")
        print("-" * 70)
        for pattern_name, mid in malware_list:
            print(f"{pattern_name:<40} | {mid}")
        return



    print(f"Input received: {args.malware} {args.platform}")

    # Get techniques for the malware
    tech_list = get_techniques_for_malware(args.malware, mitre_data)
    
    if tech_list:
        for pattern_id, pattern_name in tech_list:
            print(f"{pattern_id} : {pattern_name}")
            #extract analytics from mitre stix 20 database based on techniques
            analytics = get_analytics_for_technique(pattern_id, args.platform, mitre_data)

            # Build JSON structure
            technique_entry = {
                "technique_id": pattern_id,
                "technique_name": pattern_name,
                "analytics": [
                    {
                        "analytic_id": a[0],
                        "analytic_name": a[1],
                        "platform": a[2],

                        "log_sources": [
                            {"name": s[0], "channel": s[1]} 
                            #extract log sources from mitre stix 20 database based on analytics
                            for s in get_log_sources_for_analytic(a[0], mitre_data)
                        ]
                        
                    }
                    for a in analytics
                ]
            }

            mca_telemetry_json.append(technique_entry)

        get_json(mca_telemetry_json)

    else:
        print(f"No techniques found for '{args.malware}'")

    get_sankey(args.malware, mca_telemetry_json, int(args.threshold))

if __name__ == "__main__":
    main()