from sqlalchemy import Column, String, Text, TIMESTAMP, Boolean
from .database import Base

class VerificationOTPModel(Base):
    __tablename__ = "verification_otps"

    transaction_id = Column(String, primary_key=True, index=True)
    otp_code = Column(String(6), nullable=False)
    email = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    verified = Column(Boolean, default=False)