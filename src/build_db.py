# build_mca_telemetry.py

from src.mitre.mitre_tech_patterns import get_techniques_for_malware, get_techniques_for_group
from src.mitre.mitre_tech_analytics import get_analytics_for_technique
from src.mitre.mitre_log_sources import get_log_sources_for_analytic
import json
from pathlib import Path

LOOKUP_PATH = Path("data/lookup/channel_artifact_lookup.json")

def load_channel_lookup():
    with open(LOOKUP_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("channel_to_artifacts", {})

def get_mca_telem_json(names, platform, mitre_data):
    """
    Builds a flat list of telemetry records.
    Automatically detects whether each name is malware or a group (APT).
    """
    channel_lookup = load_channel_lookup()
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

        for pattern_id, pattern_name, tactics in tech_list:

            if not tactics:
                tactics = ["unknown"]

            analytics = get_analytics_for_technique(pattern_id, platform, mitre_data)
            

            for a in analytics:
                analytic_id, analytic_name, platform_name = a

                for channel in get_log_sources_for_analytic(analytic_id, mitre_data):
                    artifacts = channel_lookup.get(channel) or ["Unmapped"]

                    for tactic in tactics:
                        for artifact in artifacts:
                            record = {
                                "entity_type": entity_type,
                                "entity_name": name,
                                "tactic": tactic,
                                "technique_id": pattern_id,
                                "technique_name": pattern_name,
                                "analytic_id": analytic_id,
                                "analytic_name": analytic_name,
                                "platform": platform_name,
                                "log_source_channel": channel,
                                "related_artifact": artifact
                            }
                            mca_telemetry_json.append(record)

    return mca_telemetry_json