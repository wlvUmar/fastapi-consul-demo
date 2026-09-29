from datetime import datetime

from pydantic import BaseModel


class InfoResponse(BaseModel):
    service: str
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    service: str
