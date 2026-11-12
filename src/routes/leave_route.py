
from fastapi import APIRouter, Depends, HTTPException

from src.auth.api_auth import verify_api_key
from src.schemas.leave_schema import LeaveApplicationRequest
from src.services.leave_service import apply_leave

router = APIRouter(
    prefix="/leave",
    tags=["Leave Applications"],
)



@router.post("/apply")
def submit_leave(
    request: LeaveApplicationRequest,
    api_key: str = Depends(verify_api_key),
):
    try:
        return apply_leave(
            request.employee_id,
            request.start_date,
            request.end_date,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error