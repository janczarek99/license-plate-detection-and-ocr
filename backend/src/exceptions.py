from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from src.settings import settings


class NotAllowedFileTypeException(HTTPException):
    def __init__(self, current_file_type: str, allowed_file_types: List[str] = settings.ALLOWED_FILE_TYPES) -> None:
        super().__init__(
            detail={
                "status": "Not allowed file type.",
                "title": "Not allowed file type.",
                "detail": f"File type '{current_file_type}' not allowed. Must be one from: {allowed_file_types}.",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )


class TooLongVideoFileException(HTTPException):
    def __init__(self, current_video_duration: float, allowed_max_video_duration: float = settings.MAX_ALLOWED_FILE_LENGTH) -> None:
        super().__init__(
            detail={
                "status": "Too long video file.",
                "title": "Too long video file.",
                "detail": f"Video is too long (current duration = {current_video_duration :.1f}s). Maximum allowed duration is {allowed_max_video_duration}s.",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

class UnauthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            detail={
                "status": "User unauthorized.",
                "title": "User unauthorized.",
                "detail": "User unauthorized.",
            },
            status_code=HTTPStatus.UNAUTHORIZED,
        )