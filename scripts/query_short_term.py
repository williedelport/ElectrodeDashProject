import os
import pandas as pd
import yaml
import logging
import adodbapi

# Load configuration from YAML
with open("config/short_term_config.yaml", "r") as f:
    config = yaml.safe_load(f)

def query_tags(conn_str, tag_dict, time_window, period):
    conn = adodbapi.connect(conn_str)
    df_merged = None

    for label, tag in tag_dict.items():
        query = f'''
            SELECT TS, avg AS "{label}"
            FROM aggregates
            WHERE Name = '{tag}'
            AND TS > (CURRENT_TIMESTAMP - {time_window})
            AND Period = '{period}'
        '''

        try:
            df = pd.read_sql(query, conn)
            df["TS"] = pd.to_datetime(df["TS"], format="%d-%b-%y %H:%M:%S.%f", errors="coerce").dt.floor("min")
            df.dropna(subset=["TS"], inplace=True)  # Drop rows with unparseable TS

            if df_merged is None:
                df_merged = df
            else:
                df_merged = pd.merge(df_merged, df, on="TS", how="inner")
        except Exception as e:
            logging.error(f"Error querying tag {label} ({tag}): {e}\nQuery:\n{query}")

    conn.close()

    if df_merged is not None and not df_merged.empty:
        print("Sample of merged short-term data:")
        print(df_merged.head())

    return df_merged

def run_short_term_query():
    for section, details in config.items():
        logging.info(f"Querying short-term data for {section}...")
        conn_str = details["connection_string"]
        tag_dict = details["tag_names"]
        time_window = details["time_window"]
        period = details["period"]

        df = query_tags(conn_str, tag_dict, time_window, period)

        if df is not None and not df.empty:
            output_file = os.path.join("data", f"{section}_short_term.csv")
            os.makedirs("data", exist_ok=True)
            df.sort_values("TS", inplace=True)
            df.to_csv(output_file, index=False)
            logging.info(f"Saved short-term data to {output_file}")
        else:
            logging.warning(f"No data found for {section}.")