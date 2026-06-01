#!/usr/bin/env python3
from mitre_techniques import get_techniques_for_software,list_all_software
#from mitre_log_sources import get_log_sources_for_analytic   # uncomment when needed
import sys

def main():
    # If no argument is given → exit silently (no output)
    if len(sys.argv) <= 1:
        return

    user_input = sys.argv[1].strip()

    print("=== MITRE ATT&CK Orchestrator ===\n")

    #List all software
    if user_input == "software":
        print("Listing ALL MITRE ATT&CK Software / Malware...\n")
        software_list = list_all_software()
        
        print(f"Found {len(software_list)} software entries:\n")
        print(f"{'NAME':<40} | ID")
        print("-" * 70)
        for name, mid in software_list:
            print(f"{name:<40} | {mid}")
        return

    print(f"Input received: {user_input}\n")

    # Get techniques for the software/malware
    tech_list = get_techniques_for_software(user_input)
    
    if tech_list:
        print("Techniques:")
        for tcode, name in tech_list:
            print(f"   {tcode} → {name}")
    else:
        print(f"No techniques found for '{user_input}'")

if __name__ == "__main__":
    main()