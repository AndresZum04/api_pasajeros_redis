from typing import List, Optional

from app.cache.redis import redis_cache
from app.config import settings
from app.db.mongo import db


async def _buscar_tarifas_vigentes(codigo_ruta: str) -> List[dict]:
    # Las vigentes son las de la fecha_vigencia más reciente
    ultima = await db.tarifas.find_one(
        {"codigo_ruta": codigo_ruta}, sort=[("fecha_vigencia", -1)]
    )
    if ultima is None:
        return []
    return await db.tarifas.find(
        {"codigo_ruta": codigo_ruta, "fecha_vigencia": ultima["fecha_vigencia"]}
    ).to_list()


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_all_tarifas() -> List[dict]:
    return await db.tarifas.find().to_list()


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_tarifas_vigentes(codigo_ruta: str) -> List[dict]:
    return await _buscar_tarifas_vigentes(codigo_ruta)


@redis_cache(ttl_seconds=settings.redis_ttl)
async def get_resumen(codigo_ruta: str, anno: int) -> Optional[dict]:
    tarifas = await _buscar_tarifas_vigentes(codigo_ruta)
    if not tarifas:
        return None

    pipeline = [
        {"$match": {"codigo_ruta": codigo_ruta, "anno": anno}},
        {
            "$group": {
                "_id": "$codigo_ramal",
                "promedio": {
                    "$avg": {
                        "$add": [
                            {"$ifNull": ["$pasajeros_regulares", 0]},
                            {"$ifNull": ["$pasajeros_adulto_mayor", 0]},
                        ]
                    }
                },
            }
        },
    ]
    ramales = await (await db.passengers.aggregate(pipeline)).to_list()

    promedio = None
    if ramales:
        promedio = round(sum(r["promedio"] for r in ramales) / len(ramales), 2)

    return {
        "codigo_ruta": codigo_ruta,
        "nombre_ruta": tarifas[0].get("nombre_ruta"),
        "anno_pasajeros": anno,
        "tarifas_vigentes": tarifas,
        "ramales_considerados": len(ramales),
        "promedio_pasajeros": promedio,
    }