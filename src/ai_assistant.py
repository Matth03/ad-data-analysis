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
            model="gemini-2.0-flash",
            contents=f"Te egy marketing elemző vagy. Adatok: {data_summary}. Kérlek elemezd magyarul!"
        )
        return response.text
    except Exception as e:
        # Itt egy kis trükk: ha 404, kiíratjuk, milyen modelleket lát a rendszer
        if "404" in str(e):
            return "AI Hiba: Modell nem található. Ellenőrizd a modell nevét (gemini-1.5-flash)."
        return f"AI Hiba: {e}"


if __name__ == "__main__":
    print("--- Starting AI Assistant analysis... ---")
    print(get_ai_insight())