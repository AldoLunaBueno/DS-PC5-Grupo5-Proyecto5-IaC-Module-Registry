import json
import os
from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import Module

router = APIRouter()

DATA_FILE = os.path.join("data", "modules_index.json")


@router.get("/modules", response_model=List[Module])
async def get_modules():
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail="Archivo de datos no encontrado.")

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return [Module(**item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modules/{module_id}", response_model=Module)
async def get_module_by_id(module_id: str):
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail="Archivo de datos no encontrado.")

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for item in data:
        if item["id"] == module_id:
            return Module(**item)

    raise HTTPException(status_code=404, detail="Módulo no encontrado")
