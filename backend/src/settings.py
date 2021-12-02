import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    AVAILABLE_LICENSE_PLATES: List[str] = ["WF80350", "SBI91126", "PZ825UA", "WN2845M", "WPI1694G"]

    ALLOWED_FILE_TYPES: List[str] = ["video/mp4"]
    MAX_ALLOWED_FILE_LENGTH: float = 15.0

    VIDEO_SAMPLING_MS: int = 500

    AZURE_CUSTOM_VISION_URL: str = ""
    AZURE_CUSTOM_VISION_API_KEY: str = ""
    AZURE_CUSTOM_VISION_PROBABILITY_THRESHOLD: float = 0.9

    AZURE_OCR_URL: str = ""
    AZURE_OCR_API_KEY: str = ""

    # Allow to use local .env file with secrets or other variables
    class Config:
        case_sensitive = True
        env_file = os.environ.get("SETTINGS_ENV", ".env")


settings = Settings()
