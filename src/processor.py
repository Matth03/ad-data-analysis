import pandas as pd
import numpy as np


def merge_and_clean(trends_file, ads_file):
    """
    Performs data fusion and feature engineering on raw Trends and Advertising datasets.

    This module handles the 'Transform' phase of the ETL pipeline, including
    time-series alignment, Min-Max normalization, and KPI calculation.
    """

    # --- 1. Data Ingestion ---
    try:
        trends = pd.read_csv(trends_file, parse_dates=['date']).set_index('date')
        ads = pd.read_csv(ads_file, parse_dates=['date']).set_index('date')
    except Exception as e:
        print(f"Error loading source files: {e}")
        return None

    # --- 2. Data Fusion (Inner Join) ---
    master_df = pd.merge(trends, ads, left_index=True, right_index=True)

    # --- 3. Feature Scaling (Normalization) ---
    # Normalize Trend Index
    trend_col = master_df.iloc[:, 0]
    master_df['norm_trend'] = (trend_col - trend_col.min()) / (trend_col.max() - trend_col.min())

    # Normalize Ad Spend
    master_df['norm_spend'] = (master_df['spend_huf'] - master_df['spend_huf'].min()) / (
            master_df['spend_huf'].max() - master_df['spend_huf'].min())

    # --- 4. KPI Engineering ---
    # Calculating Cost Per Click (CPC) as a secondary efficiency metric.
    master_df['cpc'] = master_df['spend_huf'] / master_df['clicks'].replace(0, np.nan)
    master_df['cpc'] = master_df['cpc'].fillna(0)

    return master_df


if __name__ == "__main__":
    print("Processor module loaded. Ready for transformation tasks.")