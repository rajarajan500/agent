import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getlogin()

PATHS = {
    "desktop":   f"C:\\Users\\rajarajan\\Desktop",
    "videos":    f"C:\\Users\\rajarajan\\Videos",
    "documents": f"C:\\Users\\rajarajan\\Documents",
    "downloads": f"C:\\Users\\rajarajan\\Downloads",
    "pictures":  f"C:\\Users\\rajarajan\\Pictures",
    "music":     f"C:\\Users\\rajarajan\\Music",
}

GROQ_API_KEY = api_key=os.getenv("GROQ_API_KEY") # ← paste your key here
MODEL = "llama-3.3-70b-versatile"   # fast + very smart on Groq
TEMPERATURE = 0.1