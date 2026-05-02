import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getlogin()

PATHS = {
    "desktop":   f"C:\\Users\\{USERNAME}\\Desktop",
    "videos":    f"C:\\Users\\{USERNAME}\\Videos",
    "documents": f"C:\\Users\\{USERNAME}\\Documents",
    "downloads": f"C:\\Users\\{USERNAME}\\Downloads",
    "pictures":  f"C:\\Users\\{USERNAME}\\Pictures",
    "music":     f"C:\\Users\\{USERNAME}\\Music",
}

GROQ_API_KEY = api_key=os.getenv("GROQ_API_KEY") # ← paste your key here
MODEL = "llama-3.3-70b-versatile"   # fast + very smart on Groq
TEMPERATURE = 0.1