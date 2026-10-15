import asyncio
from typing import List

from app.config import settings
from app.db.mongo import db


async def get_all_rutas() -> List[dict]:
    # Simula una consulta pesada
    await asyncio.sleep(settings.slow_query_seconds)
    return await db.passengers.find().to_list()


async def get_ruta(codigo_ruta: str) -> List[dict]:
    return await db.passengers.find({"codigo_ruta": codigo_ruta}).to_list()
