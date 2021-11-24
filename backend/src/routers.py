import tempfile
from http import HTTPStatus

from fastapi import APIRouter, Depends, File, UploadFile

from src.exceptions import NotAllowedFileTypeException, TooLongVideoFileException
from src.schemas import DetectionsResponseSchema, LicensePlatesResponseSchema
from src.settings import settings
from src.utils import check_authorization, get_frames_every_n_ms, get_video_file_duration

router = APIRouter(dependencies=[Depends(check_authorization)])


@router.get(
    "/license-plates",
    description="Returns license plates that are on white list (list prepared by admin user).",
    response_model=LicensePlatesResponseSchema,
    status_code=HTTPStatus.OK,
)
async def get_available_license_plates():
    return {"data": settings.AVAILABLE_LICENSE_PLATES}


@router.post(
    "/detections",
    description="Returns license plate detected in given video.",
    response_model=DetectionsResponseSchema,
    status_code=HTTPStatus.OK,
)
async def get_license_plate_detected_in_video(uploaded_file: UploadFile = File(...)):
    if (current_file_type := uploaded_file.content_type.lower()) not in settings.ALLOWED_FILE_TYPES:
        raise NotAllowedFileTypeException(current_file_type)

    video_file = tempfile.NamedTemporaryFile()
    video_file.write(uploaded_file.file.read())

    if (
        current_video_duration := get_video_file_duration(video_file)
    ) > settings.MAX_ALLOWED_FILE_LENGTH:
        video_file.close()
        raise TooLongVideoFileException(current_video_duration)

    frames = get_frames_every_n_ms(video_file=video_file, n_ms=1000)
    video_file.close()

    return {"data": len(frames)}
