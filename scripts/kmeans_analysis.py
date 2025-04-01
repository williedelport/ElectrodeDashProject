# scripts/kmeans_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import logging
import os

def run_kmeans(csv_path):
    logging.info("Running KMeans clustering...")
    df = pd.read_csv(csv_path)

    # Clean column names (remove quotes and whitespace)
    df.columns = df.columns.str.strip().str.replace('"', '')

    input_columns = [
        "Furnace Active Power(MW)",
        "Electrode 1 Wesly",
        "Electrode 1 Position(mm)",
        "Electrode 1 Tenor(mm/min)"
    ]

    df_selected = df[input_columns].dropna()

    # Detect and remove outliers using IsolationForest
    clf = IsolationForest(contamination=0.01, random_state=42)
    outliers = clf.fit_predict(df_selected)
    df_selected = df_selected[outliers == 1]  # 1 indicates inlier

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_selected)

    # Fit KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    df_selected['Cluster'] = labels

    # Sort clusters based on average Furnace Active Power (to apply consistent colors)
    cluster_order = df_selected.groupby('Cluster')["Furnace Active Power(MW)"].mean().sort_values().index.tolist()
    cluster_color_map = {
        cluster_order[0]: '#00FFFF',   # Cyan (low)
        cluster_order[1]: '#90EE90',   # Light Green (mid)
        cluster_order[2]: '#FF6E6E'    # Light Red (high)
    }

    colors = df_selected['Cluster'].map(cluster_color_map)

    # Plot Wesly vs the other three variables
    plots_dir = "plots"
    os.makedirs(plots_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    variables = ["Furnace Active Power(MW)", "Electrode 1 Position(mm)", "Electrode 1 Tenor(mm/min)"]

    for i, var in enumerate(variables):
        axs[i].scatter(df_selected["Electrode 1 Wesly"], df_selected[var], c=colors, s=10, alpha=0.8)
        axs[i].set_xlabel("Electrode 1 Wesly")
        axs[i].set_ylabel(var)
        axs[i].set_title(f"Wesly vs {var}")

    plt.tight_layout()
    fig_path = os.path.join(plots_dir, "kmeans_cluster_plots.png")
    plt.savefig(fig_path)
    plt.close()
    logging.info(f"Cluster plots saved to {fig_path}")
