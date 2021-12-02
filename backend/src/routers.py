from http import HTTPStatus

from fastapi import APIRouter, Depends, File, UploadFile

from .clients import AzureClient, get_azure_client
from .schemas import DetectionsResponseSchema, LicensePlatesResponseSchema
from .settings import settings
from .utils import check_if_video_pass_conditions

router = APIRouter()


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
async def get_license_plate_detected_in_video(
    uploaded_file: UploadFile = File(...), azure_client: AzureClient = Depends(get_azure_client)
):
    video_file = check_if_video_pass_conditions(uploaded_file)
    detected_license_plates = await azure_client.detect_license_plates_in_video(
        video_file=video_file
    )

    return {"data": detected_license_plates}
