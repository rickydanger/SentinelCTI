#!/usr/bin/env python3
from mitre_techniques import get_techniques_for_malware,list_all_malware
from plotly_charts import get_sankey
import sys

def main():
    # If no argument is given → exit silently (no output)
    if len(sys.argv) <= 1:
        return

    user_input = sys.argv[1].strip()

    print("=== MITRE ATT&CK Orchestrator ===\n")

    #List all software
    if user_input == "malware":
        print("Listing ALL MITRE ATT&CK Malware...\n")
        malware_list = list_all_malware()
        
        print(f"Found {len(malware_list)} malware entries:\n")
        print(f"{'NAME':<40} | ID")
        print("-" * 70)
        for name, mid in malware_list:
            print(f"{name:<40} | {mid}")
        return

    print(f"Input received: {user_input}\n")

    # Get techniques for the malware
    tech_list = get_techniques_for_malware(user_input)
    
    if tech_list:
        print("Techniques:")
        for pattern_id, name in tech_list:
            print(f"   {pattern_id} → {name}")
    else:
        print(f"No techniques found for '{user_input}'")

    get_sankey(user_input, tech_list)

if __name__ == "__main__":
    main()