import sqlite3
import pandas as pd
import logging

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_to_sqlite(df, db_name="marketing_data.db"):
    """
    Handles data persistence by exporting the processed DataFrame into an SQLite database.

    This function manages the connection to the local SQL engine and ensures that
    the analytical 'master_table' is updated with the latest processed records.

    Args:
        df (pd.DataFrame): The final, cleaned, and normalized dataset.
        db_name (str): The filename of the SQLite database.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)

        logging.info(f"Connecting to database: {db_name}")

        # --- Data Loading (Load phase of ETL) ---
        df.to_sql('master_table', conn, if_exists='replace', index=True)

        logging.info(f"Successfully committed {len(df)} records to 'master_table'.")

    except sqlite3.Error as e:
        logging.error(f"Database error occurred: {e}")

    except Exception as e:
        logging.error(f"An unexpected error occurred during database export: {e}")

    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    print("Database module initialized. Ready for persistence tasks.")