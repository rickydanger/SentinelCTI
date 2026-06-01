#!/usr/bin/env python3
from mitreattack.stix20 import MitreAttackData

def get_techniques_for_software(software_name="blackenergy", stix_file="enterprise-attack.json"):
    """Return list of (T-code, Technique Name) used by a malware/software"""
    mitre_data = MitreAttackData(stix_file)
    
    # Find the malware/software
    for software in mitre_data.get_software():
        if software.type != "malware":
            continue
            
        name = software.name.lower()
        aliases = [a.lower() for a in getattr(software, 'x_mitre_aliases', [])]
        
        if software_name.lower() in name or any(software_name.lower() in a for a in aliases):
            # Get all techniques used by this software
            techniques = mitre_data.get_techniques_used_by_software(software.id)
            
            result = []
            for entry in techniques:
                tech = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
                tcode = getattr(tech, 'id', 'N/A')
                tname = getattr(tech, 'name', 'N/A')
                result.append((tcode, tname))
            return result
    
    return []  # Not found

def list_all_software(stix_file="enterprise-attack.json"):
    """Return list of all software/malware (name, ID)"""
    mitre_data = MitreAttackData(stix_file)
    result = []
    
    for software in mitre_data.get_software():
        if software.type != "malware":
            continue
        name = getattr(software, 'name', 'N/A')
        mid = getattr(software, 'id', 'N/A')
        result.append((name, mid))
    
    # Sort alphabetically
    return sorted(result)