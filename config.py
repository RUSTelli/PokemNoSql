from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Base directory setup: this file’s folder is your project root
BASE_DIR = Path(__file__).parent.resolve()

class Config:
    MONGO_URI     = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "pokemon_db")
    TEMPLATE_DIR  = BASE_DIR / "app" / "templates"
    STATIC_DIR    = BASE_DIR / "app" / "static"
    DATA_DIR      = BASE_DIR / "data"
