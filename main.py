"""
Main entry point for Electrode Dashboard project.
"""

from scripts.query_long_term import run_query

def main():
    print("Starting Electrode Dashboard workflow...")
    run_query()
    print("Query complete. Add analysis and dashboard steps here.")

if __name__ == "__main__":
    main()