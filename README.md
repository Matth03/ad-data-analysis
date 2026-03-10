# Marketing Data Pipeline & AI Insights

This project is a fully automated **End-to-End Data Engineering** solution that tracks market trends, correlates them with advertising spend, and generates AI-powered strategic insights.

### Tech Stack
* **Language:** Python 3.12+
* **Data Source:** Google Trends (via Pytrends) & Simulated Ad Data
* **Storage:** SQLite
* **Orchestration:** GitHub Actions
* **AI Engine:** Google Gemini 2.0 Flash
* **Visualization:** Streamlit & Plotly (Interactive Dashboard)



### System Architecture
1.  **ETL Process:** A weekly GitHub Action triggers the extraction of marketing data, which is then cleaned and transformed using Pandas.
2.  **Database Management:** Processed data is stored in an SQLite database (`marketing_data.db`), ensuring data persistence and historical tracking.
3.  **AI Analysis:** The system feeds the latest metrics into the **Gemini 2.0 Flash** model to generate a professional marketing report (`weekly_report.txt`).
4.  **Automated Deployment:** Post-execution, the bot commits the updated database back to the repository, triggering an instant update on the live dashboard.
5.  **Interactive BI:** A hosted **Streamlit** application provides real-time visualization, allowing users to explore trends and read AI insights.

### Key Features
* **Rate-Limit Resilience:** Custom fallback logic to handle API quotas (429 errors).
* **CI/CD Automation:** Completely hands-off operation via GitHub workflows.
* **Interactive Analytics:** Dynamic date scaling and hover-active charts using Plotly.
* **Secure Credential Management:** Implementation of GitHub Secrets for API protection.

---

###  Live Dashboard
You can access the interactive analysis here:
**https://ad-data-analysis-marketing-visualization.streamlit.app/**

---
*Automated Data Pipeline | Built with Streamlit, Plotly & Gemini AI*
