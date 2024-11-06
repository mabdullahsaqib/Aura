import os
from dotenv import load_dotenv

load_dotenv()

# Firebase configuration
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Google Custom Search API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
