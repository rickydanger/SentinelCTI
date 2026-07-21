from collections import defaultdict, Counter
import plotly.graph_objects as go

def get_sankey(mca_telemetry_json):
    """
    Builds a 4-layer Sankey:
    Malware → Technique → Log Source Channel → Log Source
    Nodes are sorted by connection strength for better readability.
    """
    if not mca_telemetry_json:
        print("No data to plot.")
        return

    # Counters for connections
    malware_tech = defaultdict(int)
    tech_channel = defaultdict(int)
    channel_source = defaultdict(int)

    malware_total = Counter()
    tech_total = Counter()
    channel_total = Counter()
    source_total = Counter()

    for r in mca_telemetry_json:
        m = r["malware_name"]
        t = r["technique_name"]
        c = r["log_source_channel"]
        s = r["log_source_name"]

        malware_tech[(m, t)] += 1
        tech_channel[(t, c)] += 1
        channel_source[(c, s)] += 1

        malware_total[m] += 1
        tech_total[t] += 1
        channel_total[c] += 1
        source_total[s] += 1

    # Sort nodes by strength (most connected first)
    malware_names = [m for m, _ in malware_total.most_common()]
    technique_names = [t for t, _ in tech_total.most_common()]
    channel_names = [c for c, _ in channel_total.most_common()]
    source_names = [s for s, _ in source_total.most_common()]

    # Build labels and index
    labels = malware_names + technique_names + channel_names + source_names
    idx = {label: i for i, label in enumerate(labels)}

    # Build links
    source, target, value = [], [], []

    for (m, t), cnt in malware_tech.items():
        source.append(idx[m])
        target.append(idx[t])
        value.append(cnt)

    for (t, c), cnt in tech_channel.items():
        source.append(idx[t])
        target.append(idx[c])
        value.append(cnt)

    for (c, s), cnt in channel_source.items():
        source.append(idx[c])
        target.append(idx[s])
        value.append(cnt)

    # Create Sankey
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=18,
            line=dict(color="black", width=0.4),
            label=labels,
            color=(
                ["#1E88E5"] * len(malware_names) +      # Blue - Malware
                ["#43A047"] * len(technique_names) +    # Green - Technique
                ["#FB8C00"] * len(channel_names) +      # Orange - Channel
                ["#8E24AA"] * len(source_names)         # Purple - Log Source
            )
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            hovertemplate="%{source.label} → %{target.label}<br>Count: %{value}<extra></extra>"
        )
    ))

    fig.update_layout(
        title_text="Sankey: Malware → Technique → Log Source Channel → Log Source",
        font_size=12,
        height=900
    )

    fig.show()