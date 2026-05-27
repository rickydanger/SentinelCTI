from mitreattack.stix20 import MitreAttackData
import os

# Download latest STIX data (run once)
# You can manually download from: https://github.com/mitre-attack/attack-stix-data
# Place enterprise-attack.json in your project folder

if not os.path.exists("enterprise-attack.json"):
    print("Please download enterprise-attack.json first!")
else:
    mitre_data = MitreAttackData("enterprise-attack.json")
    print("✅ MITRE ATT&CK library loaded successfully!")
    print(f"Total Techniques: {len(mitre_data.get_techniques())}")