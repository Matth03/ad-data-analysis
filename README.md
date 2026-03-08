# Marketing Insight ETL Pipeline

This repository contains a Python-based data pipeline designed to synchronize market search trends with advertising performance metrics.

## Project Concept
In digital marketing, reacting to market changes quickly is a competitive advantage. This tool aims to automate the observation of search interest (via Google Trends) and compare it with advertising activities. 

**Note:** Since real-world marketing data is often protected by NDAs, this project features a custom **Stochastic Simulation Engine** to generate realistic, noise-corrupted marketing datasets for demonstration and testing purposes.



## Key Modules
- **`api_client.py`**: Handles connection to Google Trends API (via PyTrends).
- **`generator.py`**: Simulates Meta/Google Ads data using Gaussian noise and time-lag logic.
- **`processor.py`**: Performs ETL operations, Min-Max normalization, and KPI engineering.
- **`database.py`**: Manages the persistence layer using a local SQLite instance.
- **`visualizer.py`**: Generates diagnostic plots (Time-series & Correlation heatmaps).
