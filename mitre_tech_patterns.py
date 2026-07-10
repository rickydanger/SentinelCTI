#!/usr/bin/env python3
def get_techniques_for_malware(input_name, mitre_data):
    """Return list of (Technique Pattern ID, Technique Name) used by a malware"""
    
    # Find the malware
    for malware in mitre_data.get_software():
        if malware.type != "malware":
            continue
            
        name = malware.name.lower()

        # Exact match (case insensitive)
        if input_name.lower() == name:
            print(name + " was found in the MITRE ATT&CK database.")
            # Get all techniques used by this malware
            techniques = mitre_data.get_techniques_used_by_software(malware.id)
            
            result = []
            for entry in techniques:
                tech = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
                pattern_id = getattr(tech, 'id', 'N/A')
                pattern_name = getattr(tech, 'name', 'N/A')
                result.append((pattern_id, pattern_name))
            return result
    
    return []

def list_all_malware(mitre_data):
    """Return list of all malware (name, ID)"""
    result = []
    
    for malware in mitre_data.get_software():
        if malware.type != "malware":
            continue
        name = getattr(malware, 'name', 'N/A')
        mid = getattr(malware, 'id', 'N/A')
        result.append((name, mid))
    
    # Sort alphabetically
    return sorted(result)