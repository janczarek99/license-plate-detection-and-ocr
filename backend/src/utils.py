import tempfile
from io import BytesIO
from typing import Dict, List, Optional

import cv2
import numpy as np
from fastapi import UploadFile
from PIL import Image

from .exceptions import NotAllowedFileTypeException, TooLongVideoFileException
from .settings import settings


# Utils connected with detecting license plates
def get_frames_every_n_ms(
    video_file: tempfile.NamedTemporaryFile, n_ms: int = settings.VIDEO_SAMPLING_MS
) -> List[np.array]:
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


def convert_frame_to_bytes_img(frame: np.array) -> bytes:
    pil_img = Image.fromarray(frame)
    return convert_pilow_image_to_bytes_img(pil_img)


def convert_pilow_image_to_bytes_img(pil_img: Image.Image) -> bytes:
    img_byte_arr = BytesIO()
    pil_img.save(img_byte_arr, format="JPEG")
    return img_byte_arr.getvalue()


def crop_license_plate_from_img(bboxes: List[Dict], frame: np.array) -> Optional[Image.Image]:
    pil_img = Image.fromarray(frame)
    for bbox in bboxes:
        if bbox["probability"] >= settings.AZURE_CUSTOM_VISION_PROBABILITY_THRESHOLD:
            img_width, img_height = pil_img.size
            crop_left = img_width * bbox["boundingBox"]["left"]
            crop_top = img_height * bbox["boundingBox"]["top"]
            crop_width = img_width * bbox["boundingBox"]["width"]
            crop_height = img_height * bbox["boundingBox"]["height"]
            crop_right = crop_left + crop_width
            crop_bottom = crop_top + crop_height

            return pil_img.crop((crop_left, crop_top, crop_right, crop_bottom))


# Utils connected to check if video is not too long, have ok filetype etc.
def check_if_video_pass_conditions(uploaded_video_file: UploadFile) -> tempfile.NamedTemporaryFile:
    current_file_type = uploaded_video_file.content_type.lower()

    if current_file_type not in settings.ALLOWED_FILE_TYPES:
        raise NotAllowedFileTypeException(current_file_type)

    video_file = tempfile.NamedTemporaryFile()
    video_file.write(uploaded_video_file.file.read())

    if (
        current_video_duration := get_video_file_duration(video_file)
    ) > settings.MAX_ALLOWED_FILE_LENGTH:
        video_file.close()
        raise TooLongVideoFileException(current_video_duration)

    return video_file


def get_video_file_duration(video_file: tempfile.NamedTemporaryFile) -> float:
    vidcap = cv2.VideoCapture(video_file.name)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    return duration
