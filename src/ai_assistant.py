import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load sensitive environment variables (API keys) from the hidden .env file
load_dotenv()

# Initialize the Gemini AI client using the secure API key from our environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_ai_insight():
    """
    This function acts as a mini-RAG (Retrieval-Augmented Generation) system.
    It fetches local data and feeds it to the AI for a smart summary.
    """

    # --- Path Configuration ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    db_path = os.path.join(project_root, "marketing_data.db")

    if not os.path.exists(db_path):
        return "Error: Database not found in the root directory."

    # --- Step 1: Data Retrieval ---
    # Connect to SQLite and grab the last 7 days of processed marketing data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM master_table ORDER BY date DESC LIMIT 7", conn)
    conn.close()

    # --- Step 2: Prompt Preparation ---
    # Convert the dataframe to a simple string so the AI can 'read' the table
    data_summary = df[['date', 'norm_trend', 'spend_huf', 'clicks']].to_string()

    # --- Step 3: AI Generation ---
    try:
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=f"""
            Role: You are a Senior Marketing Analyst.
            Data from the last 7 days:
            {data_summary}

            Task: Provide a concise, professional analysis in HUNGARIAN:
            1. Main trends observed.
            2. Ad spend efficiency vs. search interest.
            3. One specific recommendation for next week.
            """
        )
        return response.text

    except Exception as e:
        if "429" in str(e):
            return "AI Insight: Google API quota reached. Please try again in 1 minute!"
        return f"AI Error: {e}"


if __name__ == "__main__":
    print("--- Starting AI Assistant analysis... ---")
    print(get_ai_insight())