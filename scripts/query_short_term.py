# scripts/query_short_term.py
import pandas as pd
import adodbapi
import yaml
import os
import logging
from datetime import datetime, timedelta

def load_short_term_config(config_path="config/short_term_config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def query_tags(connection_string, tag_dict, minutes=1440):
    results = []
    now = datetime.now()
    start_time = now - timedelta(minutes=minutes)
    timestamp_format = "%Y-%m-%d %H:%M:%S"

    for tag_desc, tag_name in tag_dict.items():
        try:
            query = f"""
            SELECT TS, Value
            FROM history
            WHERE Name = '{tag_name}'
            AND TS BETWEEN '{start_time.strftime(timestamp_format)}' AND '{now.strftime(timestamp_format)}'
            ORDER BY TS
            """
            with adodbapi.connect(connection_string) as conn:
                df = pd.read_sql(query, conn)
                df.rename(columns={"Value": tag_desc}, inplace=True)
                results.append(df)
        except Exception as e:
            logging.error(f"Error querying tag {tag_desc} ({tag_name}): {e}")

    if results:
        df_merged = results[0]
        for df in results[1:]:
            df_merged = pd.merge(df_merged, df, on="TS", how="outer")
        df_sorted = df_merged.sort_values("TS")
        logging.debug(f"Merged DataFrame preview:\n{df_sorted.head()}")
        return df_sorted
    else:
        return pd.DataFrame()

def save_short_term_data(df, electrode_name):
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{electrode_name}_short_term.csv")
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved short-term data to {csv_path}")

def run_short_term_query():
    config = load_short_term_config()
    for electrode_name, electrode_data in config.items():
        logging.info(f"Querying short-term data for {electrode_name}...")
        conn_str = electrode_data["connection_string"]
        tag_dict = electrode_data["tag_names"]
        df = query_tags(conn_str, tag_dict)
        if not df.empty:
            save_short_term_data(df, electrode_name)
        else:
            logging.warning(f"No data found for {electrode_name}.")

# Expose for import in main.py
__all__ = ["run_short_term_query"]
