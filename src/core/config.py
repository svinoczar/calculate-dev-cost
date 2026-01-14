from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "code-analyzer"
    debug: bool = False

    model_dir: Path = Path("src/models/lang_detect")

    basic_threshold: float = 0.75
    ml_threshold: float = 0.7

    ignore_file: Path = Path(".dcoignore")
    use_ignore_file: bool = True
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()