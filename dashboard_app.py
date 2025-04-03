import dash
from dash import html, dcc
import logging
import os
import pandas as pd
import plotly.graph_objs as go

# Paths
overlay_image_path = "assets/kmeans_cluster_overlay.png"
short_term_data_path = "data/electrode_1_short_term.csv"

# Check image exists
if not os.path.exists(overlay_image_path):
    logging.warning(f"Overlay image not found at: {overlay_image_path}")
else:
    logging.info(f"Overlay image found at: {overlay_image_path}")

# Load data
try:
    df = pd.read_csv(short_term_data_path)
    df['TS'] = pd.to_datetime(df['TS'], errors='coerce')
except Exception as e:
    logging.error(f"Failed to load short-term data: {e}")
    df = pd.DataFrame()

# Tags to display
tags_to_display = [
    ("Furnace Active Power(MW)", "Furnace Active Power(SP)"),
    ("Minstral In Auto",),
    ("Furnace Tap Changers in Auto",),
    ("Electrode 1 in Auto",),
    ("Electrode Control Active",),
    ("TX12 Tap Changer Position",),
    ("TX23 Tap Cahnger Position",),
    ("TX31 Tap Changer Position",),
    ("Tap Acummulator",)
]

def create_sparkline(tags):
    trend = go.Figure()
    colors = ["white", "orange"]
    for idx, tag in enumerate(tags):
        if tag in df.columns:
            trend.add_trace(go.Scatter(
                x=df['TS'],
                y=df[tag],
                mode='lines',
                name=tag,
                line=dict(color=colors[idx % len(colors)], width=2)
            ))
    trend.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=40,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        font=dict(size=10, color='white')
    )
    return dcc.Graph(figure=trend, config={"displayModeBar": False}, style={"height": "40px"})

def generate_table_rows():
    rows = []
    for tag_group in tags_to_display:
        display_name = tag_group[0]
        available_tags = [tag for tag in tag_group if tag in df.columns]
        if not available_tags:
            continue
        latest_vals = [df[tag].dropna().iloc[-1] if not df[tag].dropna().empty else None for tag in available_tags]
        min_vals = [df[tag].min() for tag in available_tags]
        max_vals = [df[tag].max() for tag in available_tags]
        latest_display = ", ".join([f"{val:.2f}" if isinstance(val, (int, float)) else "No Data" for val in latest_vals])
        min_display = f"{min(min_vals):.2f}"
        max_display = f"{max(max_vals):.2f}"
        sparkline = create_sparkline(tag_group)
        rows.append(html.Tr([
            html.Td(display_name),
            html.Td(latest_display),
            html.Td(sparkline),
            html.Td(min_display),
            html.Td(max_display)
        ]))
    return rows

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Electrode Dashboard", style={"color": "white", "padding": "10px"}),
    html.Div([
        html.Div([
            html.Table([
                html.Thead(html.Tr([html.Th("Name"), html.Th("Value"), html.Th("Trend"), html.Th("Min"), html.Th("Max")])),
                html.Tbody(generate_table_rows())
            ], style={"width": "100%", "color": "white", "fontSize": "12px"})
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Img(
                src="/kmeans_cluster_overlay.png",
                style={
                    "height": "800px",
                    "width": "auto",
                    "objectFit": "contain",
                    "border": "1px solid #ccc",
                    "marginLeft": "auto"
                }
            )
        ], style={
            "flex": "1", "padding": "10px", "display": "flex", "justifyContent": "flex-end"
        })
    ], style={"display": "flex", "backgroundColor": "#1e1e1e", "color": "white"})
])

def run_dashboard():
    logging.info("Launching Dash dashboard...")
    app.run(debug=False, port=8050)

