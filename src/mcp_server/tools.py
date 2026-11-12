from datetime import date

from fastmcp.exceptions import ToolError

from src.mcp_server.app import mcp
from src.services.leave_service import (
    apply_leave,
    get_leave_balance,
)
from src.services.leave_service import (
    get_pending_leave_requests as fetch_pending_requests,
)
from src.services.leave_service import (
    review_leave_application as process_leave_review,
)


@mcp.tool()
def check_leave_balance(employee_id: str) -> dict:
    """
    Check the available annual leave balance of an employee.

    Args:
        employee_id: The employee's unique ID, e.g. EMP001.
    """
    return get_leave_balance(employee_id)

@mcp.tool()
def submit_leave_application(
    employee_id: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Submit an annual leave application.
    """
    try:
        parsed_start_date = date.fromisoformat(start_date)
        parsed_end_date = date.fromisoformat(end_date)

        return apply_leave(
            employee_id,
            parsed_start_date,
            parsed_end_date,
        )

    except ValueError as error:
        raise ToolError(str(error)) from error
    
@mcp.tool()
def get_pending_leave_requests() -> list:
    """
    Get all leave applications waiting for manager approval.
    """
    try:
        return fetch_pending_requests()
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def review_leave_application(
    application_id: str,
    decision: str,
) -> dict:
    """
    Approve or reject a pending leave application.

    Args:
        application_id: Unique ID of the leave application.
        decision: Manager's decision, either 'approve' or 'reject'.
    """
    try:
        return process_leave_review(application_id, decision)
    except ValueError as error:
        raise ToolError(str(error)) from error