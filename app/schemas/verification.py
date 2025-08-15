from pydantic import BaseModel
from typing import Optional

class EmailVerificationRequest(BaseModel):
    email: str

class EmailVerificationResponse(BaseModel):
    transaction_id: str
    status: str

class VerifyOTPRequest(BaseModel):
    transaction_id: str
    otp: str

class PANVerificationRequest(BaseModel):
    pan_number: Optional[str] = None
    name: Optional[str] = None
    dob: Optional[str] = None
    file_ref: Optional[str] = None

class PANVerificationResponse(BaseModel):
    pan_number: str
    name: str
    dob: str
    is_valid: bool