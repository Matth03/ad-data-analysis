import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Marketing Analytics Dashboard", layout="wide")

st.title("📈 Marketing ETL & AI Insights Dashboard")
st.markdown("This dashboard displays data automatically updated by the GitHub Actions pipeline.")


# Database Access Layer
def load_data():
    # Ensure the database file exists in the root directory
    conn = sqlite3.connect("marketing_data.db")
    df = pd.read_sql("SELECT * FROM master_table", conn)
    df['date'] = pd.to_datetime(df['date'])
    conn.close()
    return df


try:
    df = load_data()

    # --- 1. Key Performance Indicators (KPIs) ---
    col1, col2, col3 = st.columns(3)

    total_clicks = int(df['clicks'].sum())
    avg_cpc = df['cpc'].mean()
    avg_trend = df['norm_trend'].mean()

    col1.metric("Total Clicks", f"{total_clicks:,}")
    col2.metric("Average CPC", f"{avg_cpc:.2f} HUF")
    col3.metric("Market Demand Index (Avg)", f"{avg_trend:.2f}")

    # --- 2. Interactive Time-Series Analysis ---
    st.subheader("Market Demand vs. Advertising Spend")

    fig = px.line(df, x='date', y=['norm_trend', 'norm_spend'],
                  labels={'value': 'Normalized Scale (0-1)', 'date': 'Date', 'variable': 'Metric'},
                  title="Trend Correlation Over Time")

    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # --- 3. AI Insights Module ---
    st.divider()
    st.subheader("🤖 AI Assistant Weekly Analysis")

    if st.button("Generate/Read Latest Insight"):
        try:
            with open("weekly_report.txt", "r", encoding="utf-8") as f:
                report = f.read()
                st.info(report)
        except FileNotFoundError:
            st.warning("The weekly_report.txt file has not been generated yet.")

except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
    st.info("Check if 'marketing_data.db' exists and has been pushed to the repository.")

# Footer
st.caption("Automated Data Pipeline | Built with Streamlit, Plotly & Gemini AI")