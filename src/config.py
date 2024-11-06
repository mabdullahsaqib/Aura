import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

# GEMINI API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
