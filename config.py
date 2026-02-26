from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GMAIL_USER: str = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
SENDER_NAME: str = os.getenv("SENDER_NAME", "")

def validate():
    missing = [k for k, v in {
        "GROQ_API_KEY": GROQ_API_KEY,
        "GMAIL_USER": GMAIL_USER,
        "GMAIL_APP_PASSWORD": GMAIL_APP_PASSWORD,
        "SENDER_NAME": SENDER_NAME,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
