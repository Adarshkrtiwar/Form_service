from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .models.database import Base, engine
from .api.form_api import router as form_router
from .api.submission_api import router as submission_router
from .api.verification_api import router as verification_router
from .api.admin_api import router as admin_router
import json


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Form Service API",
    description="Dynamic form schema and submission service",
    version="1.0.0"
)


app.include_router(form_router, prefix="/api/v1")
app.include_router(submission_router, prefix="/api/v1")
app.include_router(verification_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1/admin")

@app.get("/")
def read_root():
    return {"message": "Form Service API is running"}


@app.get("/hybridaction/zybTrackerStatisticsAction")
async def handle_tracker_stats(request: Request):
    try:
    
        raw_data = request.query_params.get("data", "{}")
        callback = request.query_params.get("__callback__", "")
        
        
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            data = {}
        
        
        response_data = {
            "status": "success",
            "data": data,
            "service": "Form Service API"
        }
        
       
        if callback:
            return JSONResponse(
                content=f"{callback}({json.dumps(response_data)})",
                media_type="application/javascript"
            )
        return response_data
    
    except Exception as e:
        error_response = {"status": "error", "message": str(e)}
        if callback:
            return JSONResponse(
                content=f"{callback}({json.dumps(error_response)})",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                media_type="application/javascript"
            )
        return JSONResponse(
            content=error_response,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )