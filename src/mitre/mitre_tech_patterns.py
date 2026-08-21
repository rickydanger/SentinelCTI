#!/usr/bin/env python3

def extract_techniques(entries):
    """Shared helper to extract (technique_id, technique_name, tactics) from technique entries."""
    result = []
    
    for entry in entries:
        tech = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)
        
        pattern_id = getattr(tech, 'id', 'N/A')
        pattern_name = getattr(tech, 'name', 'N/A')
        
        # Extract tactics from kill_chain_phases
        tactics = []
        for phase in getattr(tech, 'kill_chain_phases', []):
            if getattr(phase, 'kill_chain_name', '') == 'mitre-attack':
                tactic = getattr(phase, 'phase_name', None)
                if tactic:
                    tactics.append(tactic)
        
        result.append((pattern_id, pattern_name, tactics))
    
    return result


def get_techniques_for_group(input_name, mitre_data):
    """Return list of (Technique ID, Technique Name, Tactics) used by a group (APT)"""
    
    for group in mitre_data.get_groups():
        if input_name.lower() == group.name.lower():
            print(f"{group.name} was found as a group in the MITRE ATT&CK database.")
            techniques = mitre_data.get_techniques_used_by_group(group.id)
            return extract_techniques(techniques)
    
    return []


def get_techniques_for_malware(input_name, mitre_data):
    """Return list of (Technique ID, Technique Name, Tactics) used by a malware"""
    
    for malware in mitre_data.get_software():
        if malware.type != "malware":
            continue
            
        if input_name.lower() == malware.name.lower():
            print(f"{malware.name} was found in the MITRE ATT&CK database.")
            techniques = mitre_data.get_techniques_used_by_software(malware.id)
            return extract_techniques(techniques)
    
    return []

def list_all_groups(mitre_data):
    """Return list of all groups / APTs (name, ID)"""
    result = []
    
    for group in mitre_data.get_groups():
        name = getattr(group, 'name', 'N/A')
        gid = getattr(group, 'id', 'N/A')
        result.append((name, gid))
    
    return sorted(result)

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