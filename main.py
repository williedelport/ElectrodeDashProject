import logging
from utils.query_long_term import run_long_term_query
from utils.query_short_term import run_short_term_query
from utils.kmeans_clustering import run_kmeans_clustering
from utils.kmeans_generator import run_kmeans_overlay
from dashboard_app import app

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting Electrode Dashboard workflow...")

    # 1. Query long-term data
    run_long_term_query()

    # 2. Run KMeans clustering
    run_kmeans_clustering()

    # 3. Query short-term data
    run_short_term_query()

    # 4. Generate overlay
    run_kmeans_overlay()

    # 5. Start dashboard
    app.run(debug=True, port=8050)

if __name__ == "__main__":
    main()
