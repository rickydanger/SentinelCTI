#!/usr/bin/env python3
from mitreattack.stix20 import MitreAttackData

def get_techniques_for_malware(malware_name="blackenergy", stix_file="enterprise-attack.json"):
    """Return list of (Technique Pattern ID, Technique Name) used by a malware"""
    mitre_data = MitreAttackData(stix_file)
    
    # Find the malware
    for malware in mitre_data.get_software():
        if malware.type != "malware":
            continue
            
        name = malware.name.lower()
        aliases = [a.lower() for a in getattr(malware, 'x_mitre_aliases', [])]
        
        if malware_name.lower() in name or any(malware_name.lower() in a for a in aliases):
            # Get all techniques used by this malware
            techniques = mitre_data.get_techniques_used_by_software(malware.id)
            
            result = []
            for entry in techniques:
                tech = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
                tpattern = getattr(tech, 'id', 'N/A')
                tname = getattr(tech, 'name', 'N/A')
                result.append((tpattern, tname))
            return result
    
    return []

def list_all_malware(stix_file="enterprise-attack.json"):
    """Return list of all malware (name, ID)"""
    mitre_data = MitreAttackData(stix_file)
    result = []
    
    for malware in mitre_data.get_software():
        if malware.type != "malware":
            continue
        name = getattr(malware, 'name', 'N/A')
        mid = getattr(malware, 'id', 'N/A')
        result.append((name, mid))
    
    # Sort alphabetically
    return sorted(result)