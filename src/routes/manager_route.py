from fastapi import APIRouter, Depends, HTTPException

from src.auth.api_auth import verify_api_key
from src.services.leave_service import (
    get_pending_leave_requests,
    review_leave_application,
)

router = APIRouter(
    prefix="/manager",
    tags=["Manager"],
)


@router.get("/leave_requests")
def pending_requests(
    API_KEY: str = Depends(verify_api_key),
):
    return get_pending_leave_requests()


@router.post("/leave_requests/{application_id}/review")
def review_request(
    application_id: str,
    decision: str,
    api_key: str = Depends(verify_api_key),
):
    try:
        return review_leave_application(application_id, decision)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error