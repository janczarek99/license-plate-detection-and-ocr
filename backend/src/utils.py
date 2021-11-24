import tempfile
from typing import List

import cv2
import numpy as np
from fastapi import Header, Request

from src.exceptions import UnauthorizedException
from src.settings import settings


def get_frames_every_n_ms(video_file: tempfile.NamedTemporaryFile, n_ms: int) -> List[np.array]:
    frames = []

    vidcap = cv2.VideoCapture(video_file.name)
    success, frame = vidcap.read()
    count = 0
    while success:
        frames.append(frame)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * n_ms))
        success, frame = vidcap.read()
        count += 1

    return frames


def get_video_file_duration(video_file: tempfile.NamedTemporaryFile) -> float:
    vidcap = cv2.VideoCapture(video_file.name)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    return duration


async def check_authorization(
    request: Request,
    username: str = Header(..., alias="username"),
    password: str = Header(..., alias="password"),
) -> None:
    if username != settings.API_AUTH_USERNAME or not request.app.pwd_context.verify(
        password, settings.API_AUTH_PASSWORD
    ):
        raise UnauthorizedException
