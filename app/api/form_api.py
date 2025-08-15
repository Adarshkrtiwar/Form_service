from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..schemas.form_schema import FormSchema, SchemaListResponse
from ..services.form_service import FormService

router = APIRouter()

@router.get("/schemas", response_model=SchemaListResponse)
def list_schemas(db: Session = Depends(get_db)):
    service = FormService(db)
    schemas = service.list_schemas()
    return {"schemas": schemas}

@router.get("/schemas/{schema_id}", response_model=FormSchema)
def get_schema(schema_id: str, db: Session = Depends(get_db)):
    service = FormService(db)
    schema = service.get_schema(schema_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema

@router.post("/schemas", response_model=FormSchema)
def create_schema(schema: FormSchema, db: Session = Depends(get_db)):
    service = FormService(db)
    try:
        return service.create_schema(schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))