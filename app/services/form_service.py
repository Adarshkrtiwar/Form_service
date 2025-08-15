from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from ..models.form_model import FormSchemaModel
from ..schemas.form_schema import FormSchema

class FormService:
    def __init__(self, db: Session):
        self.db = db

    def create_schema(self, schema: FormSchema) -> FormSchemaModel:
        db_schema = FormSchemaModel(
            id=schema.id,
            title=schema.title,
            schema_json=schema.json()
        )
        self.db.add(db_schema)
        self.db.commit()
        self.db.refresh(db_schema)
        return db_schema

    def get_schema(self, schema_id: str) -> Optional[FormSchema]:
        db_schema = self.db.query(FormSchemaModel).filter(FormSchemaModel.id == schema_id).first()
        if not db_schema:
            return None
        return FormSchema.parse_raw(db_schema.schema_json)

    def list_schemas(self) -> List[Dict[str, str]]:
        schemas = self.db.query(FormSchemaModel).all()
        return [{"id": schema.id, "title": schema.title} for schema in schemas]