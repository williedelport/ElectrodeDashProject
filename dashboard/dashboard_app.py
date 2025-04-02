import dash
from dash import html
import logging
import os

# Path to the overlay image
overlay_image_path = "assets/kmeans_cluster_overlay.png"

# Check if the image exists
if not os.path.exists(overlay_image_path):
    logging.warning(f"Overlay image not found at: {overlay_image_path}")
else:
    logging.info(f"Overlay image found at: {overlay_image_path}")

# Initialize the app
app = dash.Dash(__name__)
server = app.server  # Expose for external deployment if needed

# Layout
app.layout = html.Div([
    html.H1("Electrode Dashboard"),
    html.Img(src=dash.get_asset_url("kmeans_cluster_overlay.png"), style={"width": "100%", "border": "1px solid #ccc"}),
])

def run_dashboard():
    logging.info("Launching Dash dashboard...")
    app.run(debug=False, port=8050)
