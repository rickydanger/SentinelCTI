#!/usr/bin/env python3

from mitreattack.stix20 import MitreAttackData
from mitre_tech_patterns import get_techniques_for_malware,list_all_malware
from mitre_tech_analytics import get_analytics_for_technique
from mitre_log_sources import get_log_sources_for_analytic
from mca_telem_plotly_charts import get_sankey
import json
import sys

def main():
    analytic_list = []
    source_list = []
    mca_telemetry_json = []

    mitre_data = MitreAttackData("enterprise-attack.json")

    # If no argument is given → exit silently (no output)
    if len(sys.argv) <= 1:
        return

    user_input = sys.argv[1].strip()
    platform_input = sys.argv[2].strip()

    print("=== MITRE ATT&CK Orchestrator ===")

    #List all software
    if user_input == "malware":
        print("Listing ALL MITRE ATT&CK Malware...\n")
        malware_list = list_all_malware()
        
        print(f"Found {len(malware_list)} malware entries:\n")
        print(f"{'NAME':<40} | ID")
        print("-" * 70)
        for pattern_name, mid in malware_list:
            print(f"{pattern_name:<40} | {mid}")
        return

    print(f"Input received: {user_input} {platform_input}")

    # Get techniques for the malware
    tech_list = get_techniques_for_malware(user_input, mitre_data)
    
    if tech_list:
        for pattern_id, pattern_name in tech_list:
            print(f"{pattern_id} : {pattern_name}")
            #extract analytics from mitre stix 20 database based on techniques
            analytics = get_analytics_for_technique(pattern_id, platform_input, mitre_data)

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

        print(json.dumps(mca_telemetry_json, indent=2))

    else:
        print(f"No techniques found for '{user_input}'")

    get_sankey(user_input, mca_telemetry_json)

if __name__ == "__main__":
    main()