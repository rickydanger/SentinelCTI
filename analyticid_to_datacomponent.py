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
    # Get Analytic ID from command line
    if len(sys.argv) > 1:
        analytic_input = sys.argv[1].strip()
    else:
        analytic_input = "x-mitre-analytic--791dfdd4-b04d-498a-accc-ee9e2acc7b14"  # Default (Windows one for T1485)

    if not os.path.exists(STIX_FILE):
        print(f"❌ {STIX_FILE} not found.")
        print("Download it with: wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json -O enterprise-attack.json")
        return

    print("Loading ATT&CK data...\n")
    mitre_data = MitreAttackData(STIX_FILE)

    print(f"{'='*90}")
    print(f"🔍 ANALYTIC: {analytic_input}")

    try:
        # Get the Analytic object
        analytic = mitre_data.get_object(analytic_input)
        
        if not analytic:
            print("❌ Analytic not found.")
            return

        analytic_id = safe_get_attr(analytic, 'x_mitre_id', 'N/A')
        name = safe_get_attr(analytic, 'name', 'N/A')
        platforms = safe_get_attr(analytic, 'x_mitre_platforms', [])

        print(f"Name: {name}")
        print(f"ID:   {analytic_id}")
        if platforms:
            print(f"Platforms: {', '.join(platforms)}")
        print()

        # Get Data Components used by this Analytic
        data_components = mitre_data.get_datacomponents_by_analytic(analytic.id)
        
        print(f"📊 Associated Data Components ({len(data_components)}):")
        
        if not data_components:
            print("   → No Data Components linked to this analytic.")
            return

        for dc_entry in data_components:
            dc = dc_entry.get('object') if isinstance(dc_entry, dict) else getattr(dc_entry, 'object', dc_entry)
            
            dc_id = safe_get_attr(dc, 'x_mitre_id', 'N/A')
            dc_name = safe_get_attr(dc, 'name', 'N/A')
            dc_description = safe_get_attr(dc, 'description', '')[:150]
            
            print(f"   • {dc_id} - {dc_name}")
            if dc_description:
                print(f"     Description: {dc_description}...")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()