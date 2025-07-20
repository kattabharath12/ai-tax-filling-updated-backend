from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # --- App ---
    environment: str = "development"
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # --- Database ---
    database_url: str = "mysql+pymysql://taxuser:taxpassword@localhost:3306/tax_engine"

    # --- File upload ---
    upload_dir: Path = BASE_DIR / "uploads"
    max_file_size: int = 50_000_000  # 50 MB

    # --- Etc. ---
    redis_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # reads .env once