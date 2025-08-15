from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from .database import Base

class SubmissionModel(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    schema_id = Column(String, ForeignKey('form_schemas.id'), nullable=False)
    payload = Column(Text, nullable=False)
    computed_fields = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    client_ip = Column(String)
    user_agent = Column(String)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')