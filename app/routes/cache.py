from fastapi import APIRouter

from app.cache.redis import redis_client

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.delete("/")
async def limpiar_cache():
    """Borra todo lo que hay en Redis."""
    await redis_client.flushdb()
    return {"message": "Caché limpiada"}
