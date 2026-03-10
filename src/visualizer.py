import matplotlib.pyplot as plt
import seaborn as sns
import os
import sqlite3
import pandas as pd
import logging
import matplotlib.dates as mdates

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Path Management ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
db_path = os.path.join(project_root, "marketing_data.db")
output_dir = os.path.join(project_root, "docs")
output_file = os.path.join(output_dir, "performance_report.png")


def create_plots():
    """
    Generates high-fidelity visual reports from the analytical database.

    Produces:
    1. A dual time-series plot comparing market demand vs. ad spend.
    2. A correlation heatmap to identify statistical relationships between KPIs.
    """
    logging.info(f"Accessing database for visualization at: {db_path}")

    if not os.path.exists(db_path):
        logging.error("Database file not found. Ensure the pipeline has been executed.")
        return

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM master_table", conn)
        df['date'] = pd.to_datetime(df['date'])  # Ensure datetime objects for plotting
        logging.info("Data successfully loaded into memory.")

        plt.style.use('seaborn-v0_8')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # --- Plot 1: Market Trend vs. Ad Spend ---
        ax1.plot(df['date'], df['norm_trend'], label='Piaci kereslet (Trends)', color='#1f77b4', linewidth=2)
        ax1.plot(df['date'], df['norm_spend'], label='Hirdetési költés (Szimulált)', color='#ff7f0e', linestyle='--')

        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        plt.setp(ax1.get_xticklabels(), rotation=30, ha='right')

        ax1.set_title('Market Demand vs. Advertising Activity', fontsize=14, pad=15)
        ax1.set_xlabel('Timeline')
        ax1.set_ylabel('Normalized Scale (0-1)')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # --- Plot 2: KPI Correlation Matrix (Heatmap) ---
        corr_cols = ['norm_trend', 'spend_huf', 'clicks', 'cpc']
        corr_matrix = df[corr_cols].corr()

        sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', ax=ax2, fmt=".2f")
        ax2.set_title('Key Performance Indicator (KPI) Correlation Matrix', fontsize=14, pad=15)

        # --- Export & Finalization ---
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300)  # Save with high resolution for reports
        logging.info(f"Visual report successfully exported to: {output_file}")

    except Exception as e:
        logging.error(f"Visualization failed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_plots()