import os
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secrete_dev_man")
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()