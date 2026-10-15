import asyncio
from typing import List

from app.cache.redis import redis_cache
from app.config import settings
from app.db.mongo import db


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_all_rutas() -> List[dict]:
    # Simula una consulta pesada
    await asyncio.sleep(settings.slow_query_seconds)
    return await db.passengers.find().to_list()


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_ruta(codigo_ruta: str) -> List[dict]:
    return await db.passengers.find({"codigo_ruta": codigo_ruta}).to_list()
