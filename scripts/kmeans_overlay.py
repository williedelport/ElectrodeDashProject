# This script updates k-means cluster plots to overlay short-term data (last 24h)
import pandas as pd
import matplotlib.pyplot as plt
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.cm as cm


def run_kmeans_overlay():
    # Load long-term data
    long_df = pd.read_csv("data/electrode_1_long_term.csv")
    long_df.columns = long_df.columns.str.strip('"')
    long_df["TS"] = pd.to_datetime(long_df["TS"], errors="coerce")

    # Load short-term data
    short_df = pd.read_csv("data/electrode_1_short_term.csv")
    short_df.columns = short_df.columns.str.strip('"')
    short_df["TS"] = pd.to_datetime(short_df["TS"], errors="coerce")

    # Mapping long-term to short-term tag names (without "M1")
    column_mapping = {
        "Furnace Active Power(MW)": "Furnace Active Power(MW)",
        "Electrode 1 Wesly": "Electrode 1 Wesly",
        "Electrode 1 Position(mm)": "Electrode 1 Position(mm)",
        "Electrode 1 Tenor(mm/min)": "Electrode 1 Tenor(mm/min)"
    }

    long_columns = list(column_mapping.keys())
    short_columns = list(column_mapping.values())

    for col in long_columns:
        if col not in long_df.columns:
            raise ValueError(f"Missing column in long-term data: {col}")
    for col in short_columns:
        if col not in short_df.columns:
            raise ValueError(f"Missing column in short-term data: {col}")

    # Prepare and scale
    X_long = long_df[long_columns].dropna()
    X_short = short_df[short_columns].dropna()

    # Optional filtering of short-term data before plotting
    X_short = X_short[(X_short["Furnace Active Power(MW)"] > 35) & (X_short["Electrode 1 Wesly"] > 10) & (X_short["Electrode 1 Wesly"] < 20)]

    # Rename short-term columns to match long-term names
    X_short = X_short.rename(columns={v: k for k, v in column_mapping.items()})

    scaler = StandardScaler()
    X_long_scaled = scaler.fit_transform(X_long)
    X_short_scaled = scaler.transform(X_short)

    # KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    long_df.loc[X_long.index, "cluster"] = kmeans.fit_predict(X_long_scaled)

    # Plot Wesly on x-axis vs each of the other inputs
    y_columns = [col for col in long_columns if col != "Electrode 1 Wesly"]
    x_column = "Electrode 1 Wesly"

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    colors = cm.rainbow([0.1, 0.5, 0.9])
    for i, y_col in enumerate(y_columns):
        ax = axes[i]
        for cluster_id, color in zip(sorted(long_df["cluster"].dropna().unique()), colors):
            cluster_data = X_long[long_df["cluster"] == cluster_id]
            ax.scatter(
                cluster_data[x_column],
                cluster_data[y_col],
                label=f"Cluster {int(cluster_id)}",
                alpha=0.4,
                color=color
            )
        ax.scatter(
            X_short[x_column],
            X_short[y_col],
            color="navy",
            label="Short-Term",
            marker="x",
            s=20
        )
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} vs {x_column}")
        ax.legend()

    plt.tight_layout()
    plt.savefig("plots/kmeans_cluster_overlay.png")
    plt.close()
    logging.info("Overlay plot saved to plots/kmeans_cluster_overlay.png")
