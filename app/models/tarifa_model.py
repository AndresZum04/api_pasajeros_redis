from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

ObjectIdStr = Annotated[str, BeforeValidator(str)]


class TarifaModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[ObjectIdStr] = Field(default=None, alias="_id")
    codigo_ruta: str
    nombre_ruta: Optional[str] = None
    nombre_fraccionamiento: Optional[str] = None
    km_por_viaje: Optional[float] = None
    tarifa_regular: Optional[float] = None
    tarifa_adulto_mayor: Optional[float] = None
    resolucion: Optional[str] = None
    fecha_resolucion: Optional[datetime] = None
    gaceta: Optional[int] = None
    alcance: Optional[int] = None
    fecha_gaceta: Optional[datetime] = None
    fecha_vigencia: Optional[datetime] = None
    expediente: Optional[str] = None
    operadores: Optional[str] = None
    cedulas: Optional[str] = None


class ResumenTarifasModel(BaseModel):
    codigo_ruta: str
    nombre_ruta: Optional[str] = None
    anno_pasajeros: int
    tarifas_vigentes: List[TarifaModel]
    ramales_considerados: int
    promedio_pasajeros: Optional[float] = None