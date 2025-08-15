from pydantic import BaseModel
from typing import Dict, Any

class SubmissionRequest(BaseModel):
    answers: Dict[str, Any]

class SubmissionResponse(BaseModel):
    submission_id: int
    status: str
    computed: Dict[str, Any]