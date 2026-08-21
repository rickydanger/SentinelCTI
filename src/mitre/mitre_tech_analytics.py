#!/usr/bin/env python3
def safe_get_attr(obj, attr, default="N/A"):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def get_analytics_for_technique(technique_stix_id, platform, mitre_data):
    """
    Takes a technique STIX ID and returns + prints all related Analytic IDs.
    """
    results = []

    # Get the technique
    tech = mitre_data.get_object_by_stix_id(technique_stix_id)
    if not tech:
        print(f"Technique {technique_stix_id} not found.")
        return []

    # Get detection strategies for this technique
    strategies = mitre_data.get_detection_strategies_detecting_technique(tech.id)

    for entry in strategies:
        strategy = entry.get('object') if isinstance(entry, dict) else getattr(entry, 'object', entry)

        strat_id = safe_get_attr(strategy, 'id')
        #print(f"\t{strat_id}")

        # Get analytics for this strategy
        analytics = mitre_data.get_analytics_by_detection_strategy(strategy.id)

        if not analytics:
            print("No analytics linked to this strategy.\n")
            continue

        for a_entry in analytics:
            analytic = a_entry.get('object', a_entry) if isinstance(a_entry, dict) else getattr(a_entry, 'object', a_entry)
            
            analytic_platform = safe_get_attr(analytic, 'x_mitre_platforms', [])
            if analytic_platform[0].lower() == platform.lower():
                analytic_id = safe_get_attr(analytic, 'id')
                analytic_name = safe_get_attr(analytic, 'name')

                #print(f"\t\t{analytic_id} : {analytic_name} : {analytic_platform[0]}")
                results.append((analytic_id, analytic_name, analytic_platform[0]))

    return results