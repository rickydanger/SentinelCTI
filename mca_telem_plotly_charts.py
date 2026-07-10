from collections import defaultdict
import plotly.graph_objects as go

def get_sankey(name, mca_telemetry_json, threshold=1):
    """
    Creates a 4-layer Sankey diagram:
    Malware Name → Technique → Channel → Log Source

    Parameters:
        name (str): Name of the malware/MCA (used in title)
        mca_telemetry_json (list): Your structured data
        threshold (int): Minimum count required for Channel → Log Source links.
                         Links with count < threshold are removed.
                         Default = 1 (show all)
    """
    print(f"Generating Sankey diagram for {name} (threshold={threshold})")

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

    # === Calculate totals ===
    channel_total = defaultdict(int)
    for (channel, _), count in channel_logsource_count.items():
        channel_total[channel] += count

    logsource_total = defaultdict(int)
    for (_, log_name), count in channel_logsource_count.items():
        logsource_total[log_name] += count

    # === Filter channels based on threshold ===
    filtered_channels = {ch for ch, count in channel_total.items() if count >= threshold}

    # === Calculate effective technique total (only valid channels) ===
    effective_technique_total = defaultdict(int)
    for (t, ch), cnt in technique_channel_count.items():
        if ch in filtered_channels:
            effective_technique_total[t] += cnt

    # === Only keep techniques that still have connections after threshold filtering ===
    valid_techniques = {t for t, total in effective_technique_total.items() if total > 0}

    sorted_techniques = sorted(
        [(t, effective_technique_total[t]) for t in valid_techniques],
        key=lambda x: x[1], reverse=True
    )
    sorted_technique_names = [t[0] for t in sorted_techniques]

    # === Sort and filter Channels ===
    sorted_channels = sorted(
        [(ch, count) for ch, count in channel_total.items() if ch in filtered_channels],
        key=lambda x: x[1], reverse=True
    )
    sorted_channel_names = [c[0] for c in sorted_channels]

    # === Sort and filter Log Sources ===
    valid_logsources = {
        ln for (ch, ln) in channel_logsource_count.keys() if ch in filtered_channels
    }
    sorted_logsources = sorted(
        [(ln, logsource_total[ln]) for ln in valid_logsources],
        key=lambda x: x[1], reverse=True
    )
    sorted_logsource_names = [l[0] for l in sorted_logsources]

    # Final label order
    labels = [name] + sorted_technique_names + sorted_channel_names + sorted_logsource_names
    label_to_index = {label: i for i, label in enumerate(labels)}

    source = []
    target = []
    value = []

    # Link 0: Malware Name → Technique
    for tech_name in sorted_technique_names:
        count = effective_technique_total[tech_name]   # ← Use the filtered total
        source.append(label_to_index[name])
        target.append(label_to_index[tech_name])
        value.append(count)

    # Link 1: Technique → Channel
    for tech_name in sorted_technique_names:
        connected_channels = [
            (ch, cnt) for (t, ch), cnt in technique_channel_count.items() 
            if t == tech_name and ch in filtered_channels
        ]
        connected_channels.sort(key=lambda x: sorted_channel_names.index(x[0]))

        for channel, count in connected_channels:
            source.append(label_to_index[tech_name])
            target.append(label_to_index[channel])
            value.append(count)

    # Link 2: Channel → Log Source (already filtered)
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
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["#1E88E5"] +                           # Malware Name
                  ["#43A047"] * len(sorted_technique_names) +   # Techniques
                  ["#FB8C00"] * len(sorted_channel_names) +     # Channels
                  ["#8E24AA"] * len(sorted_logsource_names)     # Log Sources
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            hovertemplate='%{source.label} → %{target.label}<br>Count: %{value}<extra></extra>'
        )
    )])

    fig.update_layout(
        title_text=f"Sankey Diagram - {name}",
        font_size=12,
        height=1000
    )

    fig.show()