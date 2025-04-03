import dash
import logging
from dash import html, Output, Input
from components.scada_layout import layout
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Electrode SCADA Dashboard"
app.layout = layout

# For gunicorn / production
server = app.server

# Callback to reload short-term data every minute
@app.callback(
    Output("refresh-short-term", "n_intervals"),
    Input("refresh-short-term", "n_intervals")
)
def refresh_data(n):
    try:
        df = pd.read_csv("data/electrode_1_short_term.csv")
        df["TS"] = pd.to_datetime(df["TS"], errors="coerce")
        df.to_csv("data/electrode_1_short_term.csv", index=False)  # You could replace this with a DB call
        logging.info("Short-term data reloaded")
    except Exception as e:
        logging.error(f"Failed to refresh short-term data: {e}")
    return n

if __name__ == "__main__":
    logging.info("Starting SCADA-style Electrode Dashboard...")
    app.run_server(debug=True, port=8050)

