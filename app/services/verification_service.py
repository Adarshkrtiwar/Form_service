import random
import re
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.verification_model import VerificationOTPModel
from typing import Dict, List, Optional, Union, Any


class VerificationService:
    def __init__(self, db: Session):
        self.db = db

    def initiate_email_verification(self, email: str) -> Dict[str, str]:
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        transaction_id = f"txn_{random.getrandbits(64):016x}"
        
        # Store in DB
        otp_record = VerificationOTPModel(
            transaction_id=transaction_id,
            otp_code=otp,
            email=email,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        self.db.add(otp_record)
        self.db.commit()
        
        # In real app, we would send the OTP via email here
        print(f"Mock OTP for {email}: {otp}")  # For testing purposes
        
        return {
            "transaction_id": transaction_id,
            "status": "otp_sent"
        }

    def verify_otp(self, transaction_id: str, otp: str) -> bool:
        otp_record = self.db.query(VerificationOTPModel).filter(
            VerificationOTPModel.transaction_id == transaction_id
        ).first()
        
        if not otp_record:
            return False
        
        if otp_record.verified:
            return False
        
        if datetime.utcnow() > otp_record.expires_at:
            return False
        
        if otp_record.otp_code != otp:
            return False
        
        otp_record.verified = True
        self.db.commit()
        return True

    def verify_pan(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if request.get("file_ref"):
            # Mock OCR from filename
            filename = request["file_ref"]
            match = re.match(r"PAN_([A-Z]{5}\d{4}[A-Z]{1})_(\d{8})_([A-Z\s]+)\.\w+", filename)
            if not match:
                return {
                    "pan_number": "",
                    "name": "",
                    "dob": "",
                    "is_valid": False
                }
            
            pan_number, dob_str, name = match.groups()
            dob = f"{dob_str[:4]}-{dob_str[4:6]}-{dob_str[6:8]}"
            
            return {
                "pan_number": pan_number,
                "name": name.replace("_", " "),
                "dob": dob,
                "is_valid": True
            }
        else:
            # Simple validation for direct input
            is_valid = bool(
                request.get("pan_number") and 
                request.get("name") and 
                request.get("dob")
            )
            
            return {
                "pan_number": request.get("pan_number", ""),
                "name": request.get("name", ""),
                "dob": request.get("dob", ""),
                "is_valid": is_valid
            }