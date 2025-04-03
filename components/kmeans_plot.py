from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Load precomputed clustered data
try:
    df = pd.read_csv("data/kmeans_clustered.csv")
    df["TS"] = pd.to_datetime(df["TS"], errors="coerce")
    df.dropna(subset=["cluster"], inplace=True)
except:
    df = pd.DataFrame()

# Plot settings
def build_kmeans_overlay():
    if df.empty:
        return html.Div("KMeans data not available", style={"color": "white"})

    x_col = "Electrode 1 Wesly"
    y_cols = [
        "Electrode 1 Position(mm)",
        "Furnace Active Power(MW)",
        "Electrode 1 Tenor(mm/min)"
    ]

    short_term = df[df["Source"] == "short"]
    long_term = df[df["Source"] == "long"]

    plots = []
    for y_col in y_cols:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=long_term[x_col], y=long_term[y_col], mode='markers',
            marker=dict(color=long_term['cluster'].map({0: 'red', 1: 'orange', 2: 'green'}), size=5, opacity=0.6),
            name="Long-Term"
        ))

        fig.add_trace(go.Scatter(
            x=short_term[x_col], y=short_term[y_col], mode='markers',
            marker=dict(color='rgba(0, 255, 255, 0.3)', symbol='circle', size=6),
            name="Short-Term"
        ))

        fig.update_layout(
            title=f"{y_col} vs {x_col}",
            height=300,
            plot_bgcolor="#222", paper_bgcolor="#222",
            font=dict(color="white"),
            xaxis_title=x_col,
            yaxis_title=y_col
        )

        plots.append(dcc.Graph(figure=fig))

    return html.Div(plots)
