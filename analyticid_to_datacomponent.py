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
    analytic_stix_id = "x-mitre-analytic--791dfdd4-b04d-498a-accc-ee9e2acc7b14"  # Analytic 0411

    if len(sys.argv) > 1:
        analytic_stix_id = sys.argv[1].strip()

    if not os.path.exists(STIX_FILE):
        print("❌ enterprise-attack.json not found.")
        return

    print("Loading ATT&CK data...\n")
    mitre_data = MitreAttackData(STIX_FILE)

    print(f"🔍 ANALYTIC: {analytic_stix_id}")

    try:
        # Get the Analytic
        analytic = mitre_data.get_object_by_stix_id(analytic_stix_id)
        if not analytic:
            print("❌ Analytic not found.")
            return

        print(f"Name: {safe_get_attr(analytic, 'name')}")
        print(f"ID:   {safe_get_attr(analytic, 'id')}\n")

        # === Get the Technique this Analytic detects (T1485) ===
        technique = mitre_data.get_object_by_attack_id("T1485", "attack-pattern")
        if not technique:
            print("❌ Technique T1485 not found.")
            return

        # === Get Data Components that detect this Technique ===
        print("📊 Associated Data Components:")
        
        data_components = mitre_data.get_datacomponents_detecting_technique(technique.id)

        if not data_components:
            print("   No Data Components returned.")
        else:
            for entry in data_components:
                dc = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
                
                dc_id = safe_get_attr(dc, 'x_mitre_id', safe_get_attr(dc, 'id', 'N/A'))
                dc_name = safe_get_attr(dc, 'name', 'N/A')
                
                print(f"   • {dc_name} ({dc_id})")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()