from sqlalchemy import Column, String, Integer, Text, TIMESTAMP
from .database import Base

class FormSchemaModel(Base):
    __tablename__ = "form_schemas"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    schema_json = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')