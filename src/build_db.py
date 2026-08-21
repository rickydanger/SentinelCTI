# build_mca_telemetry.py

from src.mitre.mitre_tech_patterns import get_techniques_for_malware, get_techniques_for_group
from src.mitre.mitre_tech_analytics import get_analytics_for_technique
from src.mitre.mitre_log_sources import get_log_sources_for_analytic

def get_mca_telem_json(names, platform, mitre_data):
    """
    Builds a flat list of telemetry records.
    Automatically detects whether each name is malware or a group (APT).
    """
    mca_telemetry_json = []

    for name in names:
        # Try malware first
        tech_list = get_techniques_for_malware(name, mitre_data)
        entity_type = "malware"

        # If not found as malware, try as group/APT
        if not tech_list:
            tech_list = get_techniques_for_group(name, mitre_data)
            entity_type = "group"

        if not tech_list:
            print(f"→ Skipping '{name}' (not found as malware or group)")
            continue

        print(f"→ Processing {entity_type}: {name}")

        for pattern_id, pattern_name in tech_list:
            analytics = get_analytics_for_technique(pattern_id, platform, mitre_data)

            for a in analytics:
                analytic_id, analytic_name, platform_name = a

                for log_source_name, channel in get_log_sources_for_analytic(analytic_id, mitre_data):
                    record = {
                        "entity_type": entity_type,
                        "entity_name": name,
                        "technique_id": pattern_id,
                        "technique_name": pattern_name,
                        "analytic_id": analytic_id,
                        "analytic_name": analytic_name,
                        "platform": platform_name,
                        "log_source_name": log_source_name,
                        "log_source_channel": channel
                    }
                    mca_telemetry_json.append(record)

    return mca_telemetry_json