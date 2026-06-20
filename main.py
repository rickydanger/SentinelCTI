#!/usr/bin/env python3
from mitreattack.stix20 import MitreAttackData
from mitre_tech_patterns import get_techniques_for_malware,list_all_malware
from mitre_tech_analytics import get_analytics_for_technique
from mitre_log_sources import get_log_sources_for_analytic
from plotly_charts import get_sankey
import sys

def main():
    analytic_list = []
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
        #print("Techniques:")
        for pattern_id, pattern_name in tech_list:
            print(f"{pattern_id} : {pattern_name}")
            analytics = get_analytics_for_technique(pattern_id, platform_input, mitre_data)
            for analytic_id, analytic_name, analytic_platform in analytics:
                analytic_list.append((pattern_id, pattern_name, analytic_id, analytic_name, analytic_platform))

        for pattern_id, pattern_name, analytic_id, analytic_name, analytic_platform in analytic_list:
            print(f"\t{pattern_id} : {pattern_name} : {analytic_id} : {analytic_name} : {analytic_platform}")
        #Use , Data Destruction to get the analytic_id

        #issues is the pattern_id needs to be used get the analytic_id
        #sourcelist = get_log_sources_for_analytic("x-mitre-analytic--791dfdd4-b04d-498a-accc-ee9e2acc7b14")
        #print(sourcelist)
        #pids = get_analytics_for_technique("attack-pattern--d45a3d09-b3cf-48f4-9f0f-f521ee5cb05c")
        #print(pids)
    else:
        print(f"No techniques found for '{user_input}'")

    #get_sankey(user_input, tech_list)

if __name__ == "__main__":
    main()