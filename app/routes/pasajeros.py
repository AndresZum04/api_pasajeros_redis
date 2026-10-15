from typing import List

from fastapi import APIRouter, HTTPException

from app.models.ruta_model import RutaModel
from app.services import pasajeros_service

router = APIRouter(prefix="/pasajeros", tags=["Pasajeros"])


@router.get("/", response_model=List[RutaModel])
async def obtener_rutas():
    """Obtiene todas las rutas desde MongoDB."""
    return await pasajeros_service.get_all_rutas()


@router.get("/{codigo_ruta}", response_model=List[RutaModel])
async def obtener_ruta_por_codigo(codigo_ruta: str):
    """Obtiene los ramales de una ruta según su código."""
    rutas = await pasajeros_service.get_ruta(codigo_ruta)
    if not rutas:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return rutas
