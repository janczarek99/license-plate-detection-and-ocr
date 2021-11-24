from typing import List

from pydantic import BaseModel


class LicensePlatesResponseSchema(BaseModel):
    data: List[str]


class DetectionsResponseSchema(BaseModel):
    data: int
