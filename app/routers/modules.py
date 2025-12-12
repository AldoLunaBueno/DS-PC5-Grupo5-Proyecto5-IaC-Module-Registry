
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas import Module
from app.services.metadata_loader import load_modules_with_quality

router = APIRouter()


@router.get("/modules", response_model=List[Module])
async def get_modules(filter: Optional[str] = Query(None)):
    modules = load_modules_with_quality()
    if filter and filter.startswith("quality_state:"):
        allowed = filter.split(":", 1)[1].split("|")
        modules = [m for m in modules if m.get("quality_state") in allowed]
    return [Module(**item) for item in modules]



@router.get("/modules/{module_id}", response_model=Module)
async def get_module_by_id(module_id: str):
    modules = load_modules_with_quality()
    for item in modules:
        if item["id"] == module_id:
            return Module(**item)
    raise HTTPException(status_code=404, detail="Módulo no encontrado")
