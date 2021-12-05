import os
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    CORS_ALLOW_ORIGINS: List[str] = ["https://plate-detection-front.azurewebsites.net"]
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST"]
    CORS_SETTINGS: Optional[Dict] = None

    @validator("CORS_SETTINGS", pre=True)
    def assemble_cors_settings(cls, v: Optional[Dict], values: Dict[str, Any]) -> Any:
        if isinstance(v, dict):
            return v

        return {
            "allow_origins": values.get("CORS_ALLOW_ORIGINS"),
            "allow_methods": values.get("CORS_ALLOW_METHODS"),
        }

    AVAILABLE_LICENSE_PLATES: List[str] = ["WF80350", "SBI91126", "PZ825UA", "WN2845M", "WPI1694G"]

    ALLOWED_FILE_TYPES: List[str] = ["video/mp4"]
    MAX_ALLOWED_FILE_LENGTH: float = 15.0

    VIDEO_SAMPLING_MS: int = 100

    AZURE_CUSTOM_VISION_URL: str = ""
    AZURE_CUSTOM_VISION_API_KEY: str = ""
    AZURE_CUSTOM_VISION_PROBABILITY_THRESHOLD: float = 0.75

    AZURE_OCR_URL: str = ""
    AZURE_OCR_API_KEY: str = ""

    # Allow to use local .env file with secrets or other variables
    class Config:
        case_sensitive = True
        env_file = os.environ.get("SETTINGS_ENV", ".env")


settings = Settings()
