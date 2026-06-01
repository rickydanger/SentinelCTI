# mitre_log_sources.py
from mitreattack.stix20 import MitreAttackData

def get_log_sources_for_analytic(analytic_id, stix_file="enterprise-attack.json"):
    mitre_data = MitreAttackData(stix_file)
    analytic = mitre_data.get_object_by_stix_id(analytic_id)
    if not analytic:
        return []
    
    sources = getattr(analytic, 'x_mitre_log_source_references', [])
    return [(s.get('name', 'N/A'), s.get('channel', 'N/A')) for s in sources]