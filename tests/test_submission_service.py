from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.models.form_model import FormSchemaModel
from app.schemas.form_schema import FormSchema, FormCard, FormField, FieldType
from app.services.submission_service import SubmissionService
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    Base.metadata.create_all(bind=engine)
    
    # Add a test schema
    db = TestingSessionLocal()
    schema = FormSchema(
        id="test-schema",
        title="Test Schema",
        cards=[
            FormCard(
                id="card1",
                title="Card 1",
                fields=[
                    FormField(
                        id="name",
                        type=FieldType.TEXT,
                        label="Name",
                        validation={"required": True, "min_length": 2}
                    ),
                    FormField(
                        id="email",
                        type=FieldType.EMAIL,
                        label="Email",
                        validation={"required": True}
                    ),
                    FormField(
                        id="age",
                        type=FieldType.NUMBER,
                        label="Age",
                        validation={"required": True, "min_value": 18}
                    )
                ]
            )
        ]
    )
    
    db_schema = FormSchemaModel(
        id=schema.id,
        title=schema.title,
        schema_json=schema.json()
    )
    db.add(db_schema)
    db.commit()
    db.close()

def teardown_module():
    Base.metadata.drop_all(bind=engine)

def test_valid_submission():
    db = TestingSessionLocal()
    service = SubmissionService(db)
    
    result = service.submit_form(
        schema_id="test-schema",
        answers={"name": "John Doe", "email": "john@example.com", "age": 30},
        client_ip="127.0.0.1",
        user_agent="test"
    )
    
    assert result["status"] == "accepted"
    assert "submission_id" in result
    
    db.close()

def test_invalid_submission():
    db = TestingSessionLocal()
    service = SubmissionService(db)
    
    try:
        service.submit_form(
            schema_id="test-schema",
            answers={"name": "J", "email": "invalid", "age": 10},
            client_ip="127.0.0.1",
            user_agent="test"
        )
        assert False, "Should have raised validation error"
    except ValueError as e:
        errors = e.args[0]["errors"]
        assert "name" in errors
        assert "email" in errors
        assert "age" in errors
    
    db.close()