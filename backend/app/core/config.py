from pathlib import Path
from dotenv import load_dotenv
import os

# backend/app/core/config.py
BASE_DIR = Path(__file__).resolve().parents[3]

ENV_FILE = BASE_DIR / ".env"

print("Loading .env from:", ENV_FILE)

load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or "1440"
)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

print(DATABASE_URL)