from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    PROJECT_NAME: str = "CSV_REMAPPER_API"
    PROJECT_VERSION: str = "0.2.0"
    API_APP_HOST=os.environ.get("API_APP_HOST", "127.0.0.1")
    API_APP_PORT=int(os.environ.get("API_APP_PORT", "8000"))
    WEB_APP_HOST=os.environ.get("WEB_APP_HOST", "127.0.0.1")
    WEB_APP_PORT=os.environ.get("WEB_APP_PORT", "3200")

settings = Settings()