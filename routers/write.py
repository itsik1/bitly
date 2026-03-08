from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import os

from database import get_db
from models import Url
from schemas import ShortenRequest, ShortenResponse
from shortener import generate_short_code
from cache import get_redis

router = APIRouter()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(body: ShortenRequest, db: Session = Depends(get_db)):
    long_url = str(body.long_url)

    # Determine short code
    if body.custom_alias:
        if db.get(Url, body.custom_alias):
            raise HTTPException(status_code=409, detail="Alias already taken")
        short_code = body.custom_alias
    else:
        short_code = generate_short_code(get_redis())

    expires_at = None
    if body.expires_in_days is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(days=body.expires_in_days)

    url_record = Url(
        short_code=short_code,
        long_url=long_url,
        custom_alias=body.custom_alias,
        expires_at=expires_at,
    )
    db.add(url_record)
    db.commit()

    return ShortenResponse(
        short_code=short_code,
        short_url=f"{BASE_URL}/{short_code}",
        long_url=long_url,
    )
