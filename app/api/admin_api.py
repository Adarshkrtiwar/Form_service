from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.submission_model import SubmissionModel
import csv
from io import StringIO

router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key")

ADMIN_API_KEY = "secret-admin-key"  

@router.get("/admin/submissions")
def list_submissions(
    schema_id: str = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(api_key_header)
):
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    query = db.query(SubmissionModel)
    if schema_id:
        query = query.filter(SubmissionModel.schema_id == schema_id)
    
    submissions = query.all()
    return submissions

@router.get("/admin/submissions/export")
def export_submissions(
    schema_id: str = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(api_key_header)
):
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    query = db.query(SubmissionModel)
    if schema_id:
        query = query.filter(SubmissionModel.schema_id == schema_id)
    
    submissions = query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
   
    writer.writerow([
        "id", "schema_id", "status", "client_ip", 
        "user_agent", "created_at"
    ])
    
   
    for sub in submissions:
        writer.writerow([
            sub.id, sub.schema_id, sub.status,
            sub.client_ip, sub.user_agent, sub.created_at
        ])
    
    output.seek(0)
    return {"csv": output.getvalue()}