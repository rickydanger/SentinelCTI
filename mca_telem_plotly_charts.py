from collections import defaultdict
import plotly.graph_objects as go

def get_sankey(name, mca_telemetry_json):
    print(f"Generating Sankey diagram for {name}")

    # Count connections
    technique_channel_count = defaultdict(int)
    channel_logsource_count = defaultdict(int)
    technique_total = defaultdict(int)

    for tech in mca_telemetry_json:
        tech_name = tech["technique_name"]
        for analytic in tech["analytics"]:
            for log in analytic["log_sources"]:
                channel = log["channel"]
                log_name = log["name"]

                technique_channel_count[(tech_name, channel)] += 1
                channel_logsource_count[(channel, log_name)] += 1
                technique_total[tech_name] += 1
    
    # === Sort Techniques (by total connections) ===
    sorted_techniques = sorted(technique_total.items(), key=lambda x: x[1], reverse=True)
    sorted_technique_names = [t[0] for t in sorted_techniques]

    # === Sort Channels (by total appearances) ===
    channel_total = defaultdict(int)
    for (channel, _), count in channel_logsource_count.items():
        channel_total[channel] += count

    sorted_channels = sorted(channel_total.items(), key=lambda x: x[1], reverse=True)
    sorted_channel_names = [c[0] for c in sorted_channels]

    # === Sort Log Sources (by total appearances) ===
    logsource_total = defaultdict(int)
    for (_, log_name), count in channel_logsource_count.items():
        logsource_total[log_name] += count

    sorted_logsources = sorted(logsource_total.items(), key=lambda x: x[1], reverse=True)
    sorted_logsource_names = [l[0] for l in sorted_logsources]

    # Final label order: Techniques → Channels → Log Sources
    labels = sorted_technique_names + sorted_channel_names + sorted_logsource_names
    label_to_index = {label: i for i, label in enumerate(labels)}

    source = []
    target = []
    value = []

    # Link 1: Technique → Channel (already sorted via technique order)
    for tech_name in sorted_technique_names:
        # Get channels connected to this technique, sorted by count
        connected_channels = [(ch, cnt) for (t, ch), cnt in technique_channel_count.items() if t == tech_name]
        connected_channels.sort(key=lambda x: x[1], reverse=True)

        for channel, count in connected_channels:
            source.append(label_to_index[tech_name])
            target.append(label_to_index[channel])
            value.append(count)

    # Link 2: Channel → Log Source (sorted by channel count)
    for channel in sorted_channel_names:
        connected_logs = [(ln, cnt) for (ch, ln), cnt in channel_logsource_count.items() if ch == channel]
        connected_logs.sort(key=lambda x: x[1], reverse=True)

        for log_name, count in connected_logs:
            source.append(label_to_index[channel])
            target.append(label_to_index[log_name])
            value.append(count)

    # Create Sankey
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=22,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["#2E86AB"] * len(sorted_technique_names) +
                  ["#F18F01"] * len(sorted_channel_names) +
                  ["#A23B72"] * len(sorted_logsource_names)
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            hovertemplate='%{source.label} → %{target.label}<br>Count: %{value}<extra></extra>'
        )
    )])

    fig.update_layout(
        title_text=f"Sankey Diagram: {name}",
        font_size=12,
        height=950
    )

    fig.show()