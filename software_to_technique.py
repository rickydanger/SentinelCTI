#!/usr/bin/env python3
from mitreattack.stix20 import MitreAttackData
import os
import sys

# ====================== CONFIG ======================
STIX_FILE = "enterprise-attack.json"
# ===================================================

def safe_get_attr(obj, attr, default="N/A"):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def main():
    # Accept input from command line or default to blackenergy
    search_term = sys.argv[1].lower().strip() if len(sys.argv) > 1 else "blackenergy"

    if not os.path.exists(STIX_FILE):
        print("❌ enterprise-attack.json not found!")
        print("Download it with:")
        print("wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json -O enterprise-attack.json")
        return

    print("Loading ATT&CK data...\n")
    mitre_data = MitreAttackData(STIX_FILE)

    print(f"🔍 Searching for malware: {search_term}")

    # Find BlackEnergy (uses get_software() + filter by type == "malware")
    malware = None
    for software in mitre_data.get_software():
        if safe_get_attr(software, 'type') != "malware":
            continue

        name = safe_get_attr(software, 'name', '').lower()
        aliases = [a.lower() for a in safe_get_attr(software, 'x_mitre_aliases', [])]
        attack_id = safe_get_attr(software, 'x_mitre_id', '').lower()

        if (search_term in name or 
            search_term in attack_id or 
            any(search_term in a for a in aliases)):
            malware = software
            print(f"✅ Found: {safe_get_attr(software, 'name')} "
                  f"({safe_get_attr(software, 'x_mitre_id', 'S0089')})")
            break

    if not malware:
        print("❌ BlackEnergy not found.")
        return

    # Get all techniques used by this malware
    techniques = mitre_data.get_techniques_used_by_software(malware.id)

    print(f"\n📋 BlackEnergy uses {len(techniques)} Techniques:\n")
    print("-" * 90)
    print(f"{'T-CODE':<12} | TECHNIQUE NAME")
    print("-" * 90)

    for entry in techniques:
        tech = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
        
        tcode = safe_get_attr(tech, 'id', 'N/A')
        name = safe_get_attr(tech, 'name', 'N/A')
        print(f"{tcode:<12} | {name}")

if __name__ == "__main__":
    main()