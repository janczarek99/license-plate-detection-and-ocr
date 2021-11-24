import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    AVAILABLE_LICENSE_PLATES: List[str] = ["WF80350", "SBI91126", "PZ825UA", "WN2845M", "WPI1694G"]

    ALLOWED_FILE_TYPES: List[str] = ["video/mp4"]
    MAX_ALLOWED_FILE_LENGTH: float = 15.0

    # It's really bad way to handle like this, but it's just additional step from prevent bots to spam our api
    # We want to ommit adding database (with users) or sso, because of no time - it's "prototype"
    # In addition: that creds should be (must be!) overriden in production env.
    API_AUTH_USERNAME: str = "admin"
    API_AUTH_PASSWORD: str = (
        "$2a$12$QmZyPHsgFFF/Kh7c3ABd1.CdIZCy8bfuOhNJBCYg7/wtSqq37w4bK"  # 'password' - bcrypt
    )

    # Allow to use local .env file with secrets or other variables
    class Config:
        case_sensitive = True
        env_file = os.environ.get("SETTINGS_ENV", ".env")


settings = Settings()
