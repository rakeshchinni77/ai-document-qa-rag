from fastapi import APIRouter, status
from backend.app.schemas.response import ReportResponse

router = APIRouter()

@router.get("/report", response_model=ReportResponse, status_code=status.HTTP_200_OK)
async def get_report():
    return ReportResponse(
        context_precision=0.90,
        faithfulness=0.85,
        system_status="healthy"
    )
