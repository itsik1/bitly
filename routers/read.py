from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import get_db
from models import Url
from cache import cache_get, cache_set

router = APIRouter()


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    # 1. Cache hit
    long_url = cache_get(short_code)
    if long_url:
        print(f"[cache HIT] {short_code}")
        return RedirectResponse(url=long_url, status_code=302)

    # 2. Cache miss → query DB
    print(f"[cache MISS] {short_code}")
    url_record: Url | None = db.get(Url, short_code)

    if not url_record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # 3. Check expiry
    if url_record.expires_at:
        expires = url_record.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(status_code=410, detail="Short URL has expired")

    # 4. Populate cache, then redirect
    cache_set(short_code, url_record.long_url)
    return RedirectResponse(url=url_record.long_url, status_code=302)
