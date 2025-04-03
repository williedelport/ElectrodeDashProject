import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def run_kmeans_overlay():
    logging.info("Running KMeans overlay data generation...")

    # Load long-term data
    long_df = pd.read_csv("data/electrode_1_long_term.csv")
    long_df.columns = long_df.columns.str.strip('"')
    long_df["TS"] = pd.to_datetime(long_df["TS"], errors="coerce")

    # Load short-term data
    short_df = pd.read_csv("data/electrode_1_short_term.csv")
    short_df.columns = short_df.columns.str.strip('"')
    short_df["TS"] = pd.to_datetime(short_df["TS"], errors="coerce")

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

    X_long = long_df[long_columns].dropna()

    # Filtering long-term data
    X_long = X_long[
        (X_long["Furnace Active Power(MW)"] > 35) &
        (X_long["Electrode 1 Wesly"] > 10) &
        (X_long["Electrode 1 Wesly"] < 20)
    ]

    X_short = short_df[short_columns].dropna()

     #Filtering short-term data
    X_short = X_short[
         (X_short["Furnace Active Power(MW)"] > 35) &
         (X_short["Electrode 1 Wesly"] > 10) &
         (X_short["Electrode 1 Wesly"] < 20)
     ]

    X_short = X_short.rename(columns={v: k for k, v in column_mapping.items()})

    scaler = StandardScaler()
    X_long_scaled = scaler.fit_transform(X_long)
    X_short_scaled = scaler.transform(X_short)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_long_scaled)

    long_with_cluster = long_df.loc[X_long.index, long_columns].copy()
    long_with_cluster["cluster"] = cluster_labels
    long_with_cluster["Source"] = "long"

    short_overlay = short_df.loc[X_short.index, short_columns].rename(columns={v: k for k, v in column_mapping.items()}).copy()
    short_overlay["cluster"] = -1
    short_overlay["Source"] = "short"

    combined_df = pd.concat([long_with_cluster, short_overlay])
    combined_df.to_csv("data/kmeans_clustered.csv", index=False)
    logging.info("Saved combined KMeans overlay data to data/kmeans_clustered.csv")


if __name__ == "__main__":
    run_kmeans_overlay()
