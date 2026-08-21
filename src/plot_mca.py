from collections import defaultdict, Counter
import plotly.graph_objects as go


def prepare_data(mca_telemetry_json):
    """
    Count connections and sort nodes.
    Returns everything needed by both Sankey and Table views.
    """
    entity_tactic = defaultdict(int)
    tactic_tech = defaultdict(int)
    tech_channel = defaultdict(int)
    channel_source = defaultdict(int)

    entity_total = Counter()
    tactic_total = Counter()
    tech_total = Counter()
    channel_total = Counter()
    source_total = Counter()

    for r in mca_telemetry_json:
        e = r["entity_name"]
        tac = r["tactic"]
        t = r["technique_name"]
        c = r["log_source_channel"]
        s = r["log_source_name"]

        entity_tactic[(e, tac)] += 1
        tactic_tech[(tac, t)] += 1
        tech_channel[(t, c)] += 1
        channel_source[(c, s)] += 1

        entity_total[e] += 1
        tactic_total[tac] += 1
        tech_total[t] += 1
        channel_total[c] += 1
        source_total[s] += 1

    # Sort each layer (most connected first, then by your priority)
    entity_names = [m for m, _ in entity_total.most_common()]
    tactic_names = [t for t, _ in tactic_total.most_common()]
    technique_names = [t for t, _ in tech_total.most_common()]
    channel_names = [c for c, _ in channel_total.most_common()]
    source_names = [s for s, _ in source_total.most_common()]

    return {
        "entity_tactic": entity_tactic,
        "tactic_tech": tactic_tech,
        "tech_channel": tech_channel,
        "channel_source": channel_source,
        "entity_names": entity_names,
        "tactic_names": tactic_names,
        "technique_names": technique_names,
        "channel_names": channel_names,
        "source_names": source_names,
        "entity_total": entity_total,
        "tactic_total": tactic_total,
        "tech_total": tech_total,
        "channel_total": channel_total,
        "source_total": source_total,
    }


def get_sankey(mca_telemetry_json):
    """
    Builds a 5-layer Sankey:
    Entity → Tactic → Technique → Log Source Channel → Log Source
    """
    if not mca_telemetry_json:
        print("No data to plot.")
        return

    data = prepare_data(mca_telemetry_json)

    # Build labels and index
    labels = (data["entity_names"] + data["tactic_names"] +
              data["technique_names"] + data["channel_names"] + data["source_names"])
    idx = {label: i for i, label in enumerate(labels)}

    # Build links
    source, target, value = [], [], []

    for (e, tac), cnt in data["entity_tactic"].items():
        source.append(idx[e])
        target.append(idx[tac])
        value.append(cnt)

    for (tac, t), cnt in data["tactic_tech"].items():
        source.append(idx[tac])
        target.append(idx[t])
        value.append(cnt)

    for (t, c), cnt in data["tech_channel"].items():
        source.append(idx[t])
        target.append(idx[c])
        value.append(cnt)

    for (c, s), cnt in data["channel_source"].items():
        source.append(idx[c])
        target.append(idx[s])
        value.append(cnt)

    # Create and show the chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=18,
            line=dict(color="black", width=0.4),
            label=labels,
            color=(
                ["#1E88E5"] * len(data["entity_names"]) +
                ["#00897B"] * len(data["tactic_names"]) +
                ["#43A047"] * len(data["technique_names"]) +
                ["#FB8C00"] * len(data["channel_names"]) +
                ["#8E24AA"] * len(data["source_names"])
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
            "<br>Entity → Tactic → Technique → Log Source Channel → Log Source"
            "<br><span style='font-size:12px'>Powered by MITRE ATT&CK</span>"
        ),
        font_size=14,
        height=950
    )

    fig.show()


def get_table(mca_telemetry_json):
    """
    Displays an interactive table in the browser.
    Columns:
    entity | tactic | technique | technique count | log source channel | log source channel count | log source
    """
    if not mca_telemetry_json:
        print("No data to display.")
        return

    data = prepare_data(mca_telemetry_json)

    # Build unique rows and attach counts
    rows = {}
    for r in mca_telemetry_json:
        key = (
            r["entity_name"],
            r["tactic"],
            r["technique_name"],
            r["log_source_channel"],
            r["log_source_name"]
        )

        if key not in rows:
            rows[key] = {
                "entity": r["entity_name"],
                "tactic": r["tactic"],
                "technique": r["technique_name"],
                "technique_count": data["tech_total"][r["technique_name"]],
                "log_source_channel": r["log_source_channel"],
                "log_source_channel_count": data["channel_total"][r["log_source_channel"]],
                "log_source": r["log_source_name"]
            }

    # Sort by counts with this priority (technique strongest):
    # technique_count → channel_count → tactic → source → entity
    table_data = list(rows.values())
    table_data.sort(key=lambda r: (
        -r["technique_count"],                 # highest technique count first
        -r["log_source_channel_count"],        # then highest channel count
        r["tactic"],
        r["log_source"],
        r["entity"]
    ))

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Entity", "Tactic", "Technique", "Technique Count",
                    "Log Source Channel", "Channel Count", "Log Source"],
            fill_color="#1E88E5",
            font=dict(color="white", size=13),
            align="left"
        ),
        cells=dict(
            values=[
                [row["entity"] for row in table_data],
                [row["tactic"] for row in table_data],
                [row["technique"] for row in table_data],
                [row["technique_count"] for row in table_data],
                [row["log_source_channel"] for row in table_data],
                [row["log_source_channel_count"] for row in table_data],
                [row["log_source"] for row in table_data],
            ],
            fill_color="#F5F5F5",
            align="left",
            font=dict(size=12)
        )
    )])

    fig.update_layout(
        title_text="MCA Telemetry Calculator – Table View",
        height=1000
    )

    fig.show()