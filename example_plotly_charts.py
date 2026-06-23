import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle

def get_sankey(name, mca_telemetry_json):
    print(f"Generating Sankey diagram for {name}")

    labels = [
    name           # 0
    ]

    for tech in tech_list:
        labels.append(tech[1])  # Add technique name to labels

    links = []

    for tech in range(1, len(labels)):
        links.append((0, tech, 1.0))

    print(links)

    colors = px.colors.qualitative.Plotly
    color_cycle = cycle(colors)
    node_colors = [next(color_cycle) for _ in range(len(labels))]

    # Build the chart
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 20,
            thickness = 25,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = node_colors

        ),
        link = dict(
            source = [link[0] for link in links],
            target = [link[1] for link in links],
            value  = [link[2] for link in links],
            hovertemplate = '%{source.label} → %{target.label}<br>Hours: %{value}<extra></extra>'
        )
    )])

    fig.update_layout(
        title_text = name,
        font_size = 14,
        height = 700,
        paper_bgcolor = "#1e1e2e",   # Dark theme (optional)
        font = dict(color = "white")
    )

    fig.show()