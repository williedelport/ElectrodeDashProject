import pandas as pd
import adodbapi
import yaml
from datetime import datetime, timedelta
from pathlib import Path

def load_config(config_path="config/long_term_config.yaml"):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def execute_query(config):
    conn_str = config["connection_string"]
    tag_config = config["tag_names"]
    start_time = datetime.now() - timedelta(hours=8760)
    end_time = datetime.now()
    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    tag_dataframes = []

    for tag_alias, tag_value in tag_config.items():
        if tag_alias == "filters":
            continue

        tag_name = tag_value
        filters = tag_config["filters"].get(tag_alias, {"min": -1e9, "max": 1e9})
        tag_min = filters["min"]
        tag_max = filters["max"]

        query = f"""
        SELECT DateTime, Value AS [{tag_alias}]
        FROM OPENQUERY(INSQL,
        'SELECT DateTime, Value
         FROM WideHistory
         WHERE wwRetrievalMode = "Cyclic"
         AND wwCycleCount = 8760
         AND wwVersion = "Latest"
         AND TagName = "{tag_name}"
         AND DateTime >= "{start_str}"
         AND DateTime <= "{end_str}"')
        """

        try:
            with adodbapi.connect(conn_str) as conn:
                df = pd.read_sql(query, conn)
                df["DateTime"] = pd.to_datetime(df["DateTime"])
                df = df[(df[tag_alias] >= tag_min) & (df[tag_alias] <= tag_max)]
                tag_dataframes.append(df)
        except Exception as e:
            print(f"Error retrieving tag {tag_name}: {e}")

    if not tag_dataframes:
        return pd.DataFrame()

    df_merged = tag_dataframes[0]
    for df in tag_dataframes[1:]:
        df_merged = pd.merge(df_merged, df, on="DateTime", how="inner")

    return df_merged

def run_query():
    config = load_config()
    df = execute_query(config)
    print(df.head())
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/daily_kmeans_input.csv", index=False)