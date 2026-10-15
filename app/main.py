from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.mongo import client
from app.routes import pasajeros


@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.admin.command("ping")
    print("MongoDB: conexión OK")
    yield
    await client.close()


app = FastAPI(
    title="API de Pasajeros",
    description="Consulta de rutas de transporte público",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(pasajeros.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Pasajeros Movilizados"}
