from typing import List

from pydantic import BaseModel, Field


class LicensePlatesResponseSchema(BaseModel):
    data: List[str]


class DetectionsResponseSchema(BaseModel):
    data: int