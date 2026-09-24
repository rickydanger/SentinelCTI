"""
Starter Dash app for SentinelCTI.
Run from the project root: python dash_app.py
"""

from types import SimpleNamespace

from dash import Dash, dcc, html, Input, Output, dash_table

from src.config_db import load_config
from src.last_db import get_last_db
from src.filter_db import get_filtered_json
from src.plot_mca import get_sankey, prepare_data


def load_last_records():
    config = load_config()
    args = SimpleNamespace(last=True, db=None)
    return get_last_db(args, config) or []


RECORDS = load_last_records()

COLUMNS = [
    "entity",
    "tactic",
    "technique",
    "technique_count",
    "log_source_channel",
    "log_source_channel_count",
    "related_artifact",
    "related_tool",
]


def records_to_rows(data):
    stats = prepare_data(data)
    rows = {}
    for r in data:
        key = (
            r["entity_name"],
            r["tactic"],
            r["technique_name"],
            r["log_source_channel"],
            r["related_artifact"],
            r.get("related_tool", "Unmapped"),
        )
        if key not in rows:
            rows[key] = {
                "entity": r["entity_name"],
                "tactic": r["tactic"],
                "technique": r["technique_name"],
                "technique_count": stats["tech_total"][r["technique_name"]],
                "log_source_channel": r["log_source_channel"],
                "log_source_channel_count": stats["channel_total"][r["log_source_channel"]],
                "related_artifact": r["related_artifact"],
                "related_tool": r.get("related_tool", "Unmapped"),
            }
    return list(rows.values())


app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("MCA Telemetry Calculator"),
        html.P("Uses the last run in data/mca_config.json"),
        dcc.RadioItems(
            id="view",
            options=[
                {"label": "Sankey", "value": "sankey"},
                {"label": "Table", "value": "table"},
            ],
            value="sankey",
            inline=True,
        ),
        html.Br(),
        dcc.Graph(id="chart"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": c, "id": c} for c in COLUMNS],
            data=[],
            sort_action="native",
            sort_mode="multi",
            page_size=25,
            style_table={"overflowX": "auto"},
            style_header={"fontWeight": "bold"},
            style_cell={"textAlign": "left", "padding": "6px"},
        ),
    ],
    style={"fontFamily": "Segoe UI, sans-serif", "margin": "24px"},
)


@app.callback(
    Output("chart", "figure"),
    Output("chart", "style"),
    Output("table", "data"),
    Output("table", "style_table"),
    Input("view", "value"),
)
def update_view(view):
    data = get_filtered_json(RECORDS, technique_top=None)

    if view == "table":
        return {}, {"display": "none"}, records_to_rows(data), {"overflowX": "auto"}

    fig = get_sankey(data, show=False)
    return fig, {"display": "block"}, [], {"display": "none"}


if __name__ == "__main__":
    app.run(debug=True)