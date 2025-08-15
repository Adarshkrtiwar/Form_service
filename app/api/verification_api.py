from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..schemas.verification_schema import (
    EmailVerificationRequest,
    EmailVerificationResponse,
    VerifyOTPRequest,
    PANVerificationRequest,
    PANVerificationResponse
)
from ..services.verification_service import VerificationService
from ..utils.rate_limiter import RateLimiter

router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key")
rate_limiter = RateLimiter(requests_limit=5, time_window=60)

@router.post("/verify/email", response_model=EmailVerificationResponse)
def initiate_email_verification(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(api_key_header)
):
    if not rate_limiter.check_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    service = VerificationService(db)
    try:
        return service.initiate_email_verification(request.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify/otp")
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    service = VerificationService(db)
    success = service.verify_otp(request.transaction_id, request.otp)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP or transaction")
    return {"status": "verified"}

@router.post("/verify/pan", response_model=PANVerificationResponse)
def verify_pan(
    request: PANVerificationRequest,
    db: Session = Depends(get_db)
):
    service = VerificationService(db)
    try:
        return service.verify_pan(request.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))