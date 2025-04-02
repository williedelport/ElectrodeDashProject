import logging
from scripts.query_long_term import run_long_term_query
from scripts.query_short_term import run_short_term_query
from scripts.kmeans_clustering import run_kmeans_clustering
from scripts.kmeans_overlay import run_kmeans_overlay
from dashboard.dashboard_app import run_dashboard

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting Electrode Dashboard workflow...")

    # 1. Query long-term data (creates data/electrode_1_long_term.csv)
    run_long_term_query()

    # 2. Run KMeans clustering on long-term data
    run_kmeans_clustering()

    # 3. Query short-term data
    run_short_term_query()

    # 4. Overlay short-term on cluster plots
    run_kmeans_overlay()

    # 5. Launch dashboard
    run_dashboard()

if __name__ == "__main__":
    main()