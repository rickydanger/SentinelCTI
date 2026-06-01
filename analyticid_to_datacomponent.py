#!/usr/bin/env python3
from mitreattack.stix20 import MitreAttackData
import os
import sys

# ====================== CONFIG ======================
STIX_FILE = "enterprise-attack.json"
# ===================================================

def safe_get_attr(obj, attr, default=None):
    """Safe attribute getter for both dict and object"""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def main():
    # Default to Analytic 0411 (Windows)
    analytic_stix_id = "x-mitre-analytic--791dfdd4-b04d-498a-accc-ee9e2acc7b14"

    # Allow passing ID as command-line argument
    if len(sys.argv) > 1:
        analytic_stix_id = sys.argv[1].strip()

    if not os.path.exists(STIX_FILE):
        print("❌ enterprise-attack.json not found!")
        print("Download it with:")
        print("wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json -O enterprise-attack.json")
        return

    print("Loading ATT&CK data...\n")
    mitre_data = MitreAttackData(STIX_FILE)

    print(f"🔍 ANALYTIC ID: {analytic_stix_id}")

    try:
        # Get the Analytic object
        analytic = mitre_data.get_object_by_stix_id(analytic_stix_id)

        if not analytic:
            print("❌ Analytic not found.")
            return

        name = safe_get_attr(analytic, 'name', 'N/A')
        print(f"Name: {name}\n")

        # === Extract Log Source References ===
        log_sources = safe_get_attr(analytic, 'x_mitre_log_source_references', [])

        if not log_sources:
            print("No log source references found.")
            return

        print(f"📋 Log Sources ({len(log_sources)} found):")
        print("-" * 60)

        for i, source in enumerate(log_sources, 1):
            log_name = safe_get_attr(source, 'name', 'N/A')
            channel = safe_get_attr(source, 'channel', 'N/A')
            
            print(f"{i:2d}. Name    : {log_name}")
            print(f"    Channel : {channel}")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()