from collections import Counter

def get_filtered_json(mca_telem_json, technique_top=None):
    """
    Filters records by technique_name frequency.

    - None or 0 → keep all
    - N         → keep only the top N most frequent technique_name values
    """
    if not mca_telem_json:
        return []

    if not technique_top:
        print(f"[Technique] No filter → {len(mca_telem_json)} records")
        return mca_telem_json

    counter = Counter(r["technique_name"] for r in mca_telem_json)
    keep = {k for k, _ in counter.most_common(technique_top)}
    filtered = [r for r in mca_telem_json if r["technique_name"] in keep]

    print(f"[Technique] Top {technique_top} → keeping {len(keep)} techniques")
    print(f"[Technique] Records remaining: {len(filtered)}")
    return filtered