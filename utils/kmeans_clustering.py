import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import logging


def run_kmeans_clustering():
    logging.info("Running KMeans clustering...")
    
    # Load long-term data
    df = pd.read_csv("data/electrode_1_long_term.csv")

    # Select variables for clustering
    features = [
    '"Furnace Active Power(MW)"',
    '"Electrode 1 Wesly"',
    '"Electrode 1 Position(mm)"',
    '"Electrode 1 Tenor(mm/min)"'
    ]
    
    X = df[features].dropna()

    # Apply KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    X['Cluster'] = kmeans.fit_predict(X)

    # Save clustered data for later use
    X.to_csv("data/kmeans_clustered.csv", index=False)

    # Plot and save results
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, col in enumerate(features):
        axes[i].scatter(X.index, X[col], c=X['Cluster'], cmap='viridis', s=10)
        axes[i].set_title(f"{col} by Cluster")
        axes[i].set_xlabel("Index")
        axes[i].set_ylabel(col)

    plt.tight_layout()
    plt.savefig("plots/kmeans_cluster_plots.png")
    plt.close()
    logging.info("Cluster plots saved to plots/kmeans_cluster_plots.png")
