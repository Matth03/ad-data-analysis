import logging
import os
from src.api_client import trends_data
from src.generator import generate_mock_ads
from src.processor import merge_and_clean
from src.database import save_to_sqlite
from src.ai_assistant import get_ai_insight  # <--- Új import az AI-hoz

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Main execution for the Marketing Insight Pipeline.
    The full ETL cycle:
    1. Data Ingestion (API)
    2. Data Simulation (Mock Ads)
    3. Processing & Normalization
    4. Database Persistence
    5. AI Insight Generation (RAG)
    """
    logging.info("--- Starting Marketing Insight Pipeline ---")

    for folder in ['data/raw', 'data/processed']:
        os.makedirs(folder, exist_ok=True)

    # --- Step 1: Data Acquisition & Storage ---
    trends_path = 'data/raw/trends_raw.csv'
    trends_data.to_csv(trends_path)
    logging.info(f"Step 1: Raw Google Trends data cached at {trends_path}")

    # --- Step 2: Simulation (Synthetic Data Generation) ---
    ads_data = generate_mock_ads(trends_data)
    ads_path = 'data/raw/ads_raw.csv'
    ads_data.to_csv(ads_path)
    logging.info(f"Step 2: Synthetic advertisement data generated at {ads_path}")

    # --- Step 3: ETL Processing ---
    logging.info("Step 3: Executing data fusion and feature engineering...")
    master_df = merge_and_clean(trends_path, ads_path)

    if master_df is not None:
        processed_path = 'data/processed/processed_master_data.csv'
        master_df.to_csv(processed_path)
        logging.info(f"Step 3 Success: Processed master dataset saved to {processed_path}")

        # --- Step 4: Database Persistence ---
        logging.info("Step 4: Committing master dataset to SQLite database...")
        save_to_sqlite(master_df, "marketing_data.db")

        # --- Step 5: AI-Driven Insights (RAG) ---
        logging.info("Step 5: Generating AI insights from processed data...")
        insight = get_ai_insight()

        report_path = "weekly_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(insight)

        # --- Step 6: Validation & Statistics ---
        correlation = master_df['norm_trend'].corr(master_df['norm_spend'])

        logging.info("--- Pipeline Execution Complete ---")
        logging.info(f"Calculated Pearson Correlation (Trends vs Spend): {correlation:.2f}")
        logging.info(f"AI Insight Report generated at {report_path}")
        print("\n--- LATEST AI ANALYSIS ---\n", insight, "\n")
    else:
        logging.error("Pipeline failed during the processing stage.")


if __name__ == "__main__":
    main()