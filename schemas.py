from pydantic import BaseModel, HttpUrl
from typing import Optional


class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_alias: Optional[str] = None
    expires_in_days: Optional[int] = None


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    long_url: str
