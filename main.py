# main.py
import logging
from scripts.query_long_term import run_query as run_long_term_query
from scripts.kmeans_analysis import run_kmeans
from scripts.query_short_term import run_short_term_query

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Electrode Dashboard workflow...")

    # Step 1: Query long-term data and save it
    df_long = run_long_term_query()

    # Step 2: Run KMeans clustering on saved CSV
    run_kmeans("data/daily_kmeans_input.csv")

    # Step 3: Query and save short-term data
    run_short_term_query()

if __name__ == "__main__":
    main()

