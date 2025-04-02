import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import logging

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Electrode Dashboard"

# Load short-term data
short_df = pd.read_csv("data/electrode_1_short_term.csv")
short_df.columns = short_df.columns.str.strip('"')
short_df["TS"] = pd.to_datetime(short_df["TS"], errors="coerce")

# Choose tags to display
trend_tags = [
    "Furnace Power(MW)",
    "Electrode 1 Wesly",
    "Electrode 1 Position(mm)",
    "Electrode 1 Tenor(mm/min)",
    "Electrode 1 Current(kA)",
    "Electrode Resistance(mOhm)"
]

# Create line charts for each tag
trend_graphs = []
for tag in trend_tags:
    if tag in short_df.columns:
        fig = px.line(short_df, x="TS", y=tag, title=tag)
        trend_graphs.append(dcc.Graph(figure=fig))
    else:
        logging.warning(f"Missing tag in data: {tag}")

# Layout
app.layout = html.Div([
    html.H1("SCADA-like Electrode Dashboard", style={"textAlign": "center"}),
    html.Div(trend_graphs, style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}),
    html.Div([
        html.H2("K-Means Cluster Overlay"),
        html.Img(src="/assets/kmeans_cluster_overlay.png", style={"width": "100%", "border": "1px solid #ccc"})
    ], style={"marginTop": "40px"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
