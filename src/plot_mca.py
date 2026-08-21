from collections import defaultdict, Counter
import plotly.graph_objects as go


def _count_connections(mca_telemetry_json):
    """Count all the connections and totals from the records."""
    entity_tech = defaultdict(int)
    tech_channel = defaultdict(int)
    channel_source = defaultdict(int)

    entity_total = Counter()
    tech_total = Counter()
    channel_total = Counter()
    source_total = Counter()

    for r in mca_telemetry_json:
        e = r["entity_name"]
        t = r["technique_name"]
        c = r["log_source_channel"]
        s = r["log_source_name"]

        entity_tech[(e, t)] += 1
        tech_channel[(t, c)] += 1
        channel_source[(c, s)] += 1

        entity_total[e] += 1
        tech_total[t] += 1
        channel_total[c] += 1
        source_total[s] += 1

    return entity_tech, tech_channel, channel_source, entity_total, tech_total, channel_total, source_total


def _sort_nodes(entity_total, tech_total, channel_total, source_total):
    """Sort each layer by connection strength (most connected first)."""
    entity_names = [m for m, _ in entity_total.most_common()]
    technique_names = [t for t, _ in tech_total.most_common()]
    channel_names = [c for c, _ in channel_total.most_common()]
    source_names = [s for s, _ in source_total.most_common()]
    return entity_names, technique_names, channel_names, source_names


def _build_links(entity_tech, tech_channel, channel_source, idx):
    """Build the source, target, and value lists for the Sankey links."""
    source, target, value = [], [], []

    for (e, t), cnt in entity_tech.items():
        source.append(idx[e])
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

    return source, target, value


def get_sankey(mca_telemetry_json):
    """
    Builds a 4-layer Sankey:
    Entity → Technique → Log Source Channel → Log Source
    """
    if not mca_telemetry_json:
        print("No data to plot.")
        return

    # 1. Count connections
    entity_tech, tech_channel, channel_source, entity_total, tech_total, channel_total, source_total = _count_connections(mca_telemetry_json)

    # 2. Sort nodes
    entity_names, technique_names, channel_names, source_names = _sort_nodes(
        entity_total, tech_total, channel_total, source_total
    )

    # 3. Build labels and index
    labels = entity_names + technique_names + channel_names + source_names
    idx = {label: i for i, label in enumerate(labels)}

    # 4. Build links
    source, target, value = _build_links(entity_tech, tech_channel, channel_source, idx)

    # 6. Create and show the chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=18,
            line=dict(color="black", width=0.4),
            label=labels,
            color= (
                ["#1E88E5"] * len(entity_names) +
                ["#43A047"] * len(technique_names) +
                ["#FB8C00"] * len(channel_names) +
                ["#8E24AA"] * len(source_names)
            )
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            hovertemplate="%{source.label} → %{target.label}<br>Records: %{value}<extra></extra>"
        )
    ))

    fig.update_layout(
        title_text=(
            "MCA Telemetry Calculator"
            "<br>Entity → Technique → Log Source Channel → Log Source"
            "<br><span style='font-size:12px'>Powered by MITRE ATT&CK</span>"
        ),
        font_size=14,
        height=900
    )

    fig.show()