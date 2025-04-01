# Electrode Dashboard Project

This project builds a SCADA-like dashboard for electrode monitoring and analysis using:

- Python
- Dash (for web interface)
- K-means clustering
- Aspen data query (via SQLplus or adodbapi)

## Folder Structure

- `config/` – YAML config files
- `scripts/` – Data acquisition scripts
- `analysis/` – K-means and other analytics
- `dashboard/` – Dash app layout and display
- `utils/` – Helper functions
- `data/` – Output data (ignored by Git)

## Getting Started

```bash
python main.py
```