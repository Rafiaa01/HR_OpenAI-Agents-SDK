from fastapi import APIRouter, Depends, HTTPException

from src.auth.api_auth import verify_api_key
from src.services.leave_service import get_leave_balance

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get("/{employee_id}/leave_balance")
def leave_balance(
    employee_id: str,
    api_key: str = Depends(verify_api_key),
):
    try:
        return get_leave_balance(employee_id)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error