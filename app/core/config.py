import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///database.db")
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "secrete_dev_man")
        self.HOST: str = os.getenv("HOST", "localhost")
        self.PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()