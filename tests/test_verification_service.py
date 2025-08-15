from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.services.verification_service import VerificationService
from datetime import datetime, timedelta

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)

def test_email_verification_flow():
    db = TestingSessionLocal()
    service = VerificationService(db)
    
    # Initiate verification
    email = "test@example.com"
    result = service.initiate_email_verification(email)
    assert "transaction_id" in result
    assert "status" in result
    
    # Get the OTP from the database (in real app, it would be emailed)
    otp_record = db.query(VerificationOTPModel).filter(
        VerificationOTPModel.email == email
    ).first()
    assert otp_record is not None
    
    # Test correct OTP
    assert service.verify_otp(otp_record.transaction_id, otp_record.otp_code) == True
    
    # Test incorrect OTP
    assert service.verify_otp(otp_record.transaction_id, "wrong") == False
    
    db.close()

def test_pan_verification():
    db = TestingSessionLocal()
    service = VerificationService(db)
    
    # Test file-based verification
    file_result = service.verify_pan({
        "file_ref": "PAN_ABCDE1234F_19900101_JOHN_DOE.png"
    })
    assert file_result["is_valid"] == True
    assert file_result["pan_number"] == "ABCDE1234F"
    assert file_result["name"] == "JOHN DOE"
    assert file_result["dob"] == "1990-01-01"
    
    # Test direct input verification
    direct_result = service.verify_pan({
        "pan_number": "ABCDE1234F",
        "name": "John Doe",
        "dob": "1990-01-01"
    })
    assert direct_result["is_valid"] == True
    
    # Test invalid input
    invalid_result = service.verify_pan({
        "pan_number": "",
        "name": "",
        "dob": ""
    })
    assert invalid_result["is_valid"] == False
    
    db.close()