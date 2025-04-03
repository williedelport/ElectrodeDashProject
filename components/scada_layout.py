from dash import html, dcc
import dash_bootstrap_components as dbc
from components.trend_table import build_header_table
from components.trend_charts import build_trend_charts
from components.kmeans_plot import build_kmeans_overlay

layout = html.Div([

    # Full-screen layout
    dcc.Interval(id="refresh-short-term", interval=60*1000, n_intervals=0),
    html.Div(style={"display": "flex", "flexDirection": "row", "height": "100vh", "backgroundColor": "#1e1e1e"}, children=[

        # LEFT COLUMN
        html.Div(style={"flex": "0 0 35%", "padding": "10px", "color": "white"}, children=[

            # Electrode Header Table (sparkline table)
            html.Div(build_header_table(), style={"marginBottom": "20px"}),

            # Electrode Image (modern mimic)
            html.Div([
                html.Img(
                    src="/assets/electrode_modern.png",
                    style={"width": "100%", "border": "1px solid #555", "borderRadius": "8px"}
                )
            ])
        ]),

        # RIGHT COLUMN (Trends + KMeans)
        html.Div(style={"flex": "0 0 65%", "display": "flex", "flexDirection": "row", "padding": "10px"}, children=[

            # 7 Short-Term Trends
            html.Div(build_trend_charts(), style={"flex": "0 0 60%", "marginRight": "10px"}),

            # KMeans Plot
            html.Div(build_kmeans_overlay(), style={
                "flex": "1",
                "overflowY": "auto",
                "maxHeight": "100vh",
                "border": "1px solid #444",
                "borderRadius": "8px"
            })

        ])
    ])
])
