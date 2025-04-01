# main.py
import logging
from scripts.query_long_term import run_query
import pandas as pd
import os

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Querying long-term data...")
    df = run_query()

    # Ensure 'data' directory exists
    os.makedirs("data", exist_ok=True)
    output_path = "data/daily_kmeans_input.csv"
    df.to_csv(output_path, index=False)
    logging.info(f"Saved filtered data to {output_path}")

if __name__ == "__main__":
    main()

