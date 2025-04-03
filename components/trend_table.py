from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
import yaml

# Load short-term data and config
df = pd.read_csv("data/electrode_1_short_term.csv")
df["TS"] = pd.to_datetime(df["TS"], errors="coerce")

with open("config/short_term_config.yaml") as f:
    config = yaml.safe_load(f)

limits = config['electrode_1'].get('reference_limits', {})
tags = list(limits.keys())


def create_sparkline(tag):
    if tag not in df.columns:
        return html.Div("No Data")

    trend = go.Figure()
    trend.add_trace(go.Scatter(
        x=df['TS'], y=df[tag], mode='lines', line=dict(color='cyan', width=2), name=tag
    ))

    ref = limits.get(tag, {})
    for limit_type, color in zip(['min', 'sp', 'max'], ['red', 'orange', 'green']):
        if limit_type in ref:
            trend.add_trace(go.Scatter(
                x=df['TS'], y=[ref[limit_type]] * len(df),
                mode='lines', name=limit_type,
                line=dict(dash='dash', color=color, width=1)
            ))

    trend.update_layout(
        height=40, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False
    )
    return dcc.Graph(figure=trend, config={"displayModeBar": False}, style={"height": "40px"})


def build_header_table():
    rows = []
    for tag in tags:
        if tag not in df.columns:
            continue
        latest_val = df[tag].dropna().iloc[-1] if not df[tag].dropna().empty else None
        min_val = df[tag].min()
        max_val = df[tag].max()
        spark = create_sparkline(tag)

        rows.append(html.Tr([
            html.Td(tag),
            html.Td(f"{latest_val:.2f}" if latest_val is not None else "-"),
            html.Td(spark),
            html.Td(f"{min_val:.2f}"),
            html.Td(f"{max_val:.2f}")
        ]))

    return html.Table([
        html.Thead(html.Tr([html.Th("Tag"), html.Th("Latest"), html.Th("Trend"), html.Th("Min"), html.Th("Max")])),
        html.Tbody(rows)
    ], style={"width": "100%", "fontSize": "12px", "color": "white"})
