# backend/config.py
import os
from dotenv import load_dotenv

# Correct path to your env file
load_dotenv(dotenv_path="bot.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
print("Loaded GROQ API Key:", GROQ_API_KEY)
