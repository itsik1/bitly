from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from database import Base


class Url(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    custom_alias = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)
    user_id = Column(String, nullable=True)
