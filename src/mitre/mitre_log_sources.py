# mitre_log_sources.py
def get_log_sources_for_analytic(analytic_id, mitre_data):
    analytic = mitre_data.get_object_by_stix_id(analytic_id)
    if not analytic:
        return []
    
    sources = getattr(analytic, 'x_mitre_log_source_references', [])
    return [(s.get('channel', 'N/A')) for s in sources]