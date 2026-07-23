from collections import Counter
from statistics import median

def get_filtered_json(mca_telem_json, channel_top=None, technique_top=None):
    """
    Filters records by technique_name and/or log_source_channel frequency.

    Behavior for each parameter:
    - None  → keep items with count >= median (default)
    - 0     → bypass filter (keep all)
    - N     → keep only the top N most frequent
    """
    if not mca_telem_json:
        return []

    def apply_filter(data, field, top, label):
        if top == 0 or not data:
            return data

        counter = Counter(r[field] for r in data)

        if top is None:
            med = median(counter.values())
            keep = {k for k, cnt in counter.items() if cnt > med}
            print(f"[{label}] Median: {med:.1f} → keeping {len(keep)} items")
        else:
            keep = {k for k, _ in counter.most_common(top)}
            print(f"[{label}] Top: {top}")

        filtered = [r for r in data if r[field] in keep]
        print(f"[{label}] Records remaining: {len(filtered)}")
        return filtered


    mca_telem_json = apply_filter(mca_telem_json, "technique_name", technique_top, "Technique")
    mca_telem_json = apply_filter(mca_telem_json, "log_source_channel", channel_top, "Channel")


    return mca_telem_json