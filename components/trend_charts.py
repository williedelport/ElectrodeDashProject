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


def make_trend_graph(tag):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['TS'], y=df[tag], mode='lines', name=tag,
        line=dict(color='cyan', width=2)
    ))

    ref = limits.get(tag, {})
    for limit_type, color in zip(['min', 'sp', 'max'], ['red', 'orange', 'green']):
        if limit_type in ref:
            fig.add_trace(go.Scatter(
                x=df['TS'], y=[ref[limit_type]] * len(df),
                mode='lines', name=limit_type,
                line=dict(dash='dash', color=color, width=1)
            ))

    fig.update_layout(
        title=tag,
        height=150,
        margin=dict(t=30, l=20, r=20, b=20),
        plot_bgcolor='#222', paper_bgcolor='#222',
        font=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(color='white')
    )
    return dcc.Graph(figure=fig)


def build_trend_charts():
    return html.Div([
        make_trend_graph(tag) for tag in tags if tag in df.columns
    ])
