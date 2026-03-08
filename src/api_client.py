from pytrends.request import TrendReq
import pandas as pd
import logging

# --- Logging Configuration ---
# Setting up basic logging to track API connection status
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_market_trends(keywords=["Hitel"], timeframe='today 3-m', geo='HU'):
    """
    Connects to Google Trends API via PyTrends to retrieve search interest data.

    Args:
        keywords (list): List of search terms to analyze.
        timeframe (str): Time range for the data (default: last 3 months).
        geo (str): Geographic location code (default: Hungary).

    Returns:
        pd.DataFrame: Cleaned time-series data of search interest.
    """
    try:
        # Initialize PyTrends with locale and timezone settings
        pytrends = TrendReq(hl='hu-HU', tz=360)

        logging.info(f"Requesting Google Trends data for: {keywords} in {geo}")

        pytrends.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe=timeframe,
            geo=geo,
            gprop=''
        )

        trends_data = pytrends.interest_over_time()

        if trends_data.empty:
            logging.warning("No data returned from Google Trends API.")
            return pd.DataFrame()

        # --- Data Preprocessing ---
        if 'isPartial' in trends_data.columns:
            trends_data = trends_data.drop(columns=['isPartial'])

        logging.info("Successfully fetched and cleaned Trends data.")
        return trends_data

    except Exception as e:
        logging.error(f"Failed to connect to Google Trends API: {e}")
        return pd.DataFrame()


# Global execution for the pipeline
trends_data = fetch_market_trends()

if __name__ == "__main__":
    # Internal module validation
    if not trends_data.empty:
        print("\n--- Google Trends Data Preview ---")
        print(trends_data.head())