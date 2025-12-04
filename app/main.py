from fastapi import FastAPI

from app.routers import modules

app = FastAPI(title="IaC Module Registry", version="1.0.0")

app.include_router(modules.router)


@app.get("/")
async def index():
    return "Practica Calificada 05"


@app.get("/health")
async def health_check():
    return {"status": "ok"}
