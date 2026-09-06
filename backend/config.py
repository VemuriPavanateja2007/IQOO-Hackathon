import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings

def get_default_db_url() -> str:
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        import tempfile
        import shutil
        tmp_db_path = os.path.join(tempfile.gettempdir(), "vitalmind.db")
        project_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vitalmind.db")
        if not os.path.exists(tmp_db_path) and os.path.exists(project_db_path):
            try:
                shutil.copyfile(project_db_path, tmp_db_path)
            except Exception:
                pass
        return f"sqlite:///{tmp_db_path}"
    return "sqlite:///./vitalmind.db"

class Settings(BaseSettings):
    PROJECT_NAME: str = "VitalMind AI - Antigravity Health Platform"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", get_default_db_url())
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vitalmind-antigravity-secret-key-2026")
    STATION_NAME: str = "Orbital Outpost Alpha (Zero-G)"

settings = Settings()

