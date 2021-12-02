import asyncio
import tempfile
from http import HTTPStatus
from typing import Dict, List, Optional

import aiohttp
import numpy as np
from fastapi import Request
from PIL import Image

from .settings import settings
from .utils import (convert_frame_to_bytes_img, convert_pilow_image_to_bytes_img,
                    crop_license_plate_from_img, get_frames_every_n_ms)


class AzureClient:
    def __init__(
        self,
        custom_vision_url: str = settings.AZURE_CUSTOM_VISION_URL,
        custom_vision_api_key: str = settings.AZURE_CUSTOM_VISION_API_KEY,
        ocr_url: str = settings.AZURE_OCR_URL,
        ocr_api_key: str = settings.AZURE_OCR_API_KEY,
    ) -> None:
        self._custom_vision_url = custom_vision_url
        self._custom_vision_api_key = custom_vision_api_key
        self._ocr_url = ocr_url
        self._ocr_api_key = ocr_api_key

    async def detect_license_plates_in_video(
        self, video_file: tempfile.NamedTemporaryFile
    ) -> List[str]:
        frames = get_frames_every_n_ms(video_file)

        tasks = []

        for frame in frames:
            tasks.append(asyncio.ensure_future(self._find_license_plates_and_ocr(frame)))

        results = await asyncio.gather(*tasks)

        license_plates = [result.upper() for result in results if result is not None]

        video_file.close()

        return list(set(license_plates))

    async def _find_license_plates_and_ocr(self, frame: np.array) -> Optional[str]:
        found_license_plates_bboxes = await self._find_license_plate(frame)
        cropped_license_plate = crop_license_plate_from_img(found_license_plates_bboxes, frame)

        if not cropped_license_plate:
            return None

        license_plate_characters_regions = await self._get_characters_from_license_plate(
            cropped_license_plate
        )

        if not license_plate_characters_regions:
            return None

        proper_license_plate = ""

        for region in license_plate_characters_regions:
            for line in region["lines"]:
                for word in line["words"]:
                    proper_license_plate += word["text"].strip()

        return proper_license_plate

    async def _find_license_plate(self, frame: np.array) -> List[Dict]:
        headers = {
            "Content-Type": "application/octet-stream",
            "Prediction-Key": self._custom_vision_api_key,
        }

        data = convert_frame_to_bytes_img(frame)

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(self._custom_vision_url, data=data) as response:
                    if response.status == HTTPStatus.OK:
                        json_response = await response.json()
                        return json_response.get("predictions", [])
        except Exception:
            pass

        return []

    async def _get_characters_from_license_plate(self, pil_img: Image.Image) -> List[Dict]:
        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": self._ocr_api_key,
        }

        data = convert_pilow_image_to_bytes_img(pil_img)

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(self._ocr_url, data=data) as response:
                    if response.status == HTTPStatus.OK:
                        json_response = await response.json()
                        return json_response.get("regions", [])
        except Exception:
            pass

        return []


async def get_azure_client(request: Request) -> AzureClient:
    return request.app.azure_client
