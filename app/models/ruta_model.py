from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

ObjectIdStr = Annotated[str, BeforeValidator(str)]


class RutaModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[ObjectIdStr] = Field(default=None, alias="_id")
    nombre_operador: str
    cedula: str
    codigo_ruta: str
    descripcion_ruta: str
    codigo_ramal: str
    descripcion_ramal: Optional[str] = None
    mes: int
    anno: int
    pasajero_equivalente: Optional[float] = None
    pasajerosTotal: Optional[str] = None
    pasajeros_adulto_mayor: Optional[int] = 0
    pasajeros_regulares: Optional[int] = 0
    carreras: Optional[float] = 0
    ingresos: Optional[int] = 0
