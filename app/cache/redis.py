import hashlib
import json
import logging
from functools import wraps
from typing import Callable

from bson import json_util
from redis.asyncio import Redis

from app.config import settings

logger = logging.getLogger("uvicorn.error")

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


async def check_redis_connection():
    try:
        await redis_client.ping()
        print("Redis: conexión OK")
    except Exception as e:
        print(f"Redis: no disponible ({e})")


def redis_cache(ttl_seconds: int = 10):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_raw = f"{func.__module__}.{func.__name__}:" + json.dumps(
                {"args": args, "kwargs": kwargs}, sort_keys=True, default=str
            )
            key = "cache:" + hashlib.sha256(key_raw.encode()).hexdigest()

            # Se busca la llave en Redis
            try:
                cached = await redis_client.get(key)
            except Exception as e:
                logger.warning("Redis no disponible: %s", e)
                return await func(*args, **kwargs)

            if cached is not None:
                logger.info("Cache HIT  %s", func.__name__)
                return json.loads(cached, object_hook=json_util.object_hook)

            logger.info("Cache MISS %s", func.__name__)
            result = await func(*args, **kwargs)

            # Se guarda con tiempo de expiración (TTL)
            try:
                await redis_client.setex(
                    key, ttl_seconds, json.dumps(result, default=json_util.default)
                )
            except Exception as e:
                logger.warning("No se pudo guardar en Redis: %s", e)
            return result

        return wrapper

    return decorator
