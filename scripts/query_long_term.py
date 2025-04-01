# scripts/query_long_term.py
import yaml
import adodbapi
import pandas as pd
import logging

# Load config
def load_config(path="config/long_term_config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

# Query execution
def run_query():
    config = load_config()
    tag_names = config["tag_names"]
    filters = config["filters"]
    conn_str = config["connection_string"]

    query = f"""
    SELECT 
        fap."TS",
        fap."Furnace Active Power(MW)",
        mia."Minstral In Auto",
        ec."Electrode 1 Current(kA)",
        er."Electrode Resistance(mOhm)",
        ep."Electrode 1 Position(mm)",
        et."Electrode 1 Tenor(mm/min)",
        ew."Electrode 1 Wesly"
    FROM (
        SELECT "TS", avg AS "Furnace Active Power(MW)"
        FROM aggregates
        WHERE Name = '{tag_names["Furnace Active Power(MW)"]}'
        AND avg BETWEEN {filters["Furnace Active Power(MW)"]["min"]} AND {filters["Furnace Active Power(MW)"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) fap
    INNER JOIN (
        SELECT "TS", avg AS "Minstral In Auto"
        FROM aggregates
        WHERE Name = '{tag_names["Minstral In Auto"]}'
        AND avg BETWEEN {filters["Minstral In Auto"]["min"]} AND {filters["Minstral In Auto"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) mia ON fap."TS" = mia."TS"
    INNER JOIN (
        SELECT "TS", avg AS "Electrode 1 Current(kA)"
        FROM aggregates
        WHERE Name = '{tag_names["Electrode 1 Current(kA)"]}'
        AND avg BETWEEN {filters["Electrode 1 Current(kA)"]["min"]} AND {filters["Electrode 1 Current(kA)"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) ec ON fap."TS" = ec."TS"
    INNER JOIN (
        SELECT "TS", avg AS "Electrode Resistance(mOhm)"
        FROM aggregates
        WHERE Name = '{tag_names["Electrode Resistance(mOhm)"]}'
        AND avg BETWEEN {filters["Electrode Resistance(mOhm)"]["min"]} AND {filters["Electrode Resistance(mOhm)"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) er ON fap."TS" = er."TS"
    INNER JOIN (
        SELECT "TS", avg AS "Electrode 1 Position(mm)"
        FROM aggregates
        WHERE Name = '{tag_names["Electrode 1 Position(mm)"]}'
        AND avg BETWEEN {filters["Electrode 1 Position(mm)"]["min"]} AND {filters["Electrode 1 Position(mm)"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) ep ON fap."TS" = ep."TS"
    INNER JOIN (
        SELECT "TS", avg AS "Electrode 1 Tenor(mm/min)"
        FROM aggregates
        WHERE Name = '{tag_names["Electrode 1 Tenor(mm/min)"]}'
        AND avg BETWEEN {filters["Electrode 1 Tenor(mm/min)"]["min"]} AND {filters["Electrode 1 Tenor(mm/min)"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) et ON fap."TS" = et."TS"
    INNER JOIN (
        SELECT "TS", avg AS "Electrode 1 Wesly"
        FROM aggregates
        WHERE Name = '{tag_names["Electrode 1 Wesly"]}'
        AND avg BETWEEN {filters["Electrode 1 Wesly"]["min"]} AND {filters["Electrode 1 Wesly"]["max"]}
        AND TS > (CURRENT_TIMESTAMP - 8760:00:00)
        AND Period = '01:00:00'
    ) ew ON fap."TS" = ew."TS"
    """

    logging.debug(f"Executing SQL: {query}")
    conn = adodbapi.connect(conn_str)
    df = pd.read_sql(query, conn)
    conn.close()

    logging.info(f"Query returned {len(df)} rows.")
    return df