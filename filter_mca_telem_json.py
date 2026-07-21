import jmespath
from collections import Counter

def get_filtered_json(mca_telemetry_json, top=None):
    """
    Keep only records whose log_source_channel is in the top N most frequent.
    If top is None, return the original data unfiltered.
    """
    if not mca_telemetry_json:
        return []

    if top is None:
        return mca_telemetry_json

    counter = Counter(r["log_source_channel"] for r in mca_telemetry_json)
    top_channels = [ch for ch, _ in counter.most_common(top)]

    print(f"Keeping top {top}: {top_channels}")

    channels_str = ", ".join(f"'{ch}'" for ch in top_channels)
    expression = f"[?contains([{channels_str}], log_source_channel)]"

    filtered = jmespath.search(expression, mca_telemetry_json)
    print(f"Records remaining: {len(filtered)}")
    
    return filtered