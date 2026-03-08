"""
Redis cache wrapper.
Uses fakeredis for local dev (USE_FAKE_REDIS=true in .env),
or a real Redis connection in production.
"""

import os
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_redis():
    global _client
    if _client is None:
        if os.getenv("USE_FAKE_REDIS", "true").lower() == "true":
            import fakeredis
            _client = fakeredis.FakeRedis(decode_responses=True)
        else:
            import redis
            _client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True,
            )
    return _client


def cache_get(short_code: str) -> str | None:
    return get_redis().get(short_code)


def cache_set(short_code: str, long_url: str, ttl: int = 3600):
    get_redis().setex(short_code, ttl, long_url)
