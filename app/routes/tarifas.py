from typing import List

from fastapi import APIRouter, HTTPException

from app.models.tarifa_model import ResumenRuta, TarifaModel
from app.services import tarifas_service

router = APIRouter(prefix="/tarifas", tags=["Tarifas"])


@router.get("/", response_model=List[TarifaModel])
async def obtener_tarifas():
    """Todas las tarifas."""
    return await tarifas_service.get_all_tarifas()


@router.get("/{codigo_ruta}/resumen", response_model=ResumenRuta)
async def resumen_ruta(codigo_ruta: str, anno: int = 2024):
    """Tarifas vigentes de la ruta y promedio de pasajeros del año indicado."""
    resumen = await tarifas_service.get_resumen_ruta(codigo_ruta, anno)
    if not resumen:
        raise HTTPException(status_code=404, detail="Ruta sin tarifas")
    return resumen


@router.get("/{codigo_ruta}", response_model=List[TarifaModel])
async def tarifas_por_ruta(codigo_ruta: str):
    """Tarifas vigentes de una ruta."""
    tarifas = await tarifas_service.get_tarifas_ruta(codigo_ruta)
    if not tarifas:
        raise HTTPException(status_code=404, detail="Ruta sin tarifas")
    return tarifas
