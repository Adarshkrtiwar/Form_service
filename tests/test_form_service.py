from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.schemas.form_schema import FormSchema, FormCard, FormField, FieldType
from app.services.form_service import FormService

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_schema():
    db = TestingSessionLocal()
    service = FormService(db)
    
    schema = FormSchema(
        id="test-schema",
        title="Test Schema",
        cards=[
            FormCard(
                id="card1",
                title="Card 1",
                fields=[
                    FormField(
                        id="field1",
                        type=FieldType.TEXT,
                        label="Field 1"
                    )
                ]
            )
        ]
    )
    
    created = service.create_schema(schema)
    assert created.id == "test-schema"
    
    retrieved = service.get_schema("test-schema")
    assert retrieved.id == "test-schema"
    assert retrieved.title == "Test Schema"
    
    db.close()