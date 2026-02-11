import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Stable model for AI Studio API
GEMINI_CHAT_MODEL = "models/gemini-2.0-flash-lite"

# Chroma collection name
CHROMA_COLLECTION = "terraform"
