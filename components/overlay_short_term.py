import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the existing k-means plot data
kmeans_data_file = os.path.join("data", "kmeans_data.csv")
short_term_file = os.path.join("data", "electrode_1_short_term.csv")

# Columns to overlay
overlay_columns = [
    "M1 Furnace Power(MW)",
    "Electrode 1 Wesly",
    "Electrode 1 Position(mm)",
    "Electrode 1 Tenor(mm/min)"
]

# Load data
kmeans_df = pd.read_csv(kmeans_data_file)
short_term_df = pd.read_csv(short_term_file)

# Plot directory
os.makedirs("plots", exist_ok=True)

for col in overlay_columns:
    if col not in kmeans_df.columns or col not in short_term_df.columns:
        print(f"Skipping {col} - not found in one of the datasets.")
        continue

    plt.figure()
    plt.scatter(
        kmeans_df.index,
        kmeans_df[col],
        label="Historical (KMeans)",
        alpha=0.5
    )
    plt.plot(
        short_term_df.index,
        short_term_df[col],
        color="red",
        linewidth=2,
        label="Last 24h"
    )
    plt.title(f"{col} with Last 24h Overlay")
    plt.xlabel("Index")
    plt.ylabel(col)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"overlay_{col.replace(' ', '_')}.png"))
    plt.close()

print("Overlay plots saved in the 'plots' folder.")
