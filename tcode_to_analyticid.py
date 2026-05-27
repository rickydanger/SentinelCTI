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
    # Get T-code from command line or default
    tcode = sys.argv[1].upper().strip() if len(sys.argv) > 1 else "T1485"

    if not os.path.exists(STIX_FILE):
        print(f"{STIX_FILE} not found.")
        print("Download it using:")
        print("wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json -O enterprise-attack.json")
        return

    print("Loading ATT&CK data...\n")
    mitre_data = MitreAttackData(STIX_FILE)

    print(f"{'='*90}")
    print(f"TECHNIQUE: {tcode}")

    try:
        tech = mitre_data.get_object_by_attack_id(tcode, "attack-pattern")
        
        print(f"Name: {safe_get_attr(tech, 'name')}")
        desc = safe_get_attr(tech, 'description', '')[:200]
        print(f"Description: {desc}...\n")

        strategies = mitre_data.get_detection_strategies_detecting_technique(tech.id)
        
        if not strategies:
            print("No Detection Strategies found.")
            return

        print(f"Detection Strategies Found: {len(strategies)}\n")

        for entry in strategies:
            # Handle both object and dict cases
            strategy = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
            
            strat_id = safe_get_attr(strategy, 'id', 'N/A')
            strat_name = safe_get_attr(strategy, 'name', 'N/A')
            
            print(f"Detection Strategy: {strat_id} - {strat_name}")

            # Get Analytics using the correct ID
            strategy_id = safe_get_attr(strategy, 'id', None)
            if not strategy_id:
                print("   Could not get strategy ID")
                continue
                
            analytics = mitre_data.get_analytics_by_detection_strategy(strategy_id)
            
            print(f"   Associated Analytics ({len(analytics)}):")          

            if not analytics:
                print("     → No analytics found for this strategy.")
                continue

            for i, analytic_entry in enumerate(analytics):

                if isinstance(analytic_entry, dict):
                    analytic = analytic_entry.get('object') or analytic_entry

                    analytic_id = safe_get_attr(analytic, 'id', 'N/A')
                    name = safe_get_attr(analytic, 'name', 'N/A')
                    platforms = safe_get_attr(analytic, 'x_mitre_platforms', [])
                    
                    print(f"     • {analytic_id} | {name}")

                if platforms:
                    print(f"       Platforms: {', '.join(platforms)}")
            
            print("-" * 80)

    except Exception as e:
        print(f"Error processing {tcode}: {e}")


if __name__ == "__main__":
    main()