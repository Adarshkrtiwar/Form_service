from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..schemas.submission_schema import SubmissionRequest, SubmissionResponse
from ..services.submission_service import SubmissionService

router = APIRouter()

@router.post("/forms/{schema_id}/submit", response_model=SubmissionResponse)
def submit_form(
    schema_id: str,
    submission: SubmissionRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    service = SubmissionService(db)
    try:
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        result = service.submit_form(
            schema_id=schema_id,
            answers=submission.answers,
            client_ip=client_ip,
            user_agent=user_agent
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))