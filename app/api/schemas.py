from fastapi import APIRouter, HTTPException
from app.services.schema_service import get_schema, list_schemas

router = APIRouter()

@router.get("/schemas")
async def list_all_schemas():
    return list_schemas()

@router.get("/schemas/{schema_id}")
async def get_schema_by_id(schema_id: str):
    schema = get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema