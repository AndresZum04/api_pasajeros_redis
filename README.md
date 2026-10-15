# API de Pasajeros (ARESEP) - Laboratorio Redis V2

API en FastAPI + MongoDB (PyMongo async) con caché en Redis.

Guía del laboratorio: `Laboratorio_Redis_V2_Guia.pdf`

## Ramas

- `main`: API base, sin caché
- `cache`: `main` más Redis
- `solucion-tarifas`: `cache` más el ejercicio de tarifas resuelto

## Ejecutar

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs
