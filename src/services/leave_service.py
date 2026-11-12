import uuid
from datetime import date
from pathlib import Path

from logs import logger
from src.storage.storage_json import read_json, write_json

BASE_DIR = Path(__file__).resolve().parents[1]

EMPLOYEES_FILE = BASE_DIR / "data" / "employee.json"
APPLICATIONS_FILE = BASE_DIR / "data" / "leave_application.json"


def get_leave_balance(employee_id: str):
    employees = read_json(EMPLOYEES_FILE)

    employee = employees.get(employee_id)

    if employee is None:
        logger.warning("Employee not found: %s", employee_id)
        raise ValueError(f"Employee {employee_id} does not exist.")

    balance = employee["annual_leave_balance"]

    logger.info("Retrieved leave balance for employee: %s", employee_id)

    return {
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "annual_leave_balance": balance,
    }


# working-days calculation function
def calculate_working_days(start_date: date, end_date: date) -> int:
    days = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:
            days += 1

        current_date = date.fromordinal(current_date.toordinal() + 1)

    return days


def apply_leave(employee_id: str, start_date: date, end_date: date):

    # 1. Validate employee
    employees = read_json(EMPLOYEES_FILE)

    employee = employees.get(employee_id)

    if employee is None:
        raise ValueError(f"Employee {employee_id} does not exist.")

    # 2. Validate dates
    if end_date < start_date:
        raise ValueError("End date cannot be before start date.")

    if start_date < date.today():
        raise ValueError("Leave cannot start in the past.")

    # 3. Calculate working days
    days_requested = calculate_working_days(start_date, end_date)

    if days_requested == 0:
        raise ValueError("Leave request must include at least one working day.")

    # 4. Check leave balance
    balance = employee["annual_leave_balance"]

    if days_requested > balance:
        raise ValueError(
            f"Insufficient leave balance. Available: {balance}, "
            f"Requested: {days_requested}."
        )

    # 5. Check overlapping applications
    applications = read_json(APPLICATIONS_FILE)

    for application in applications:
        if application["employee_id"] != employee_id:
            continue

        if application["status"] not in ("pending", "approved"):
            continue

        existing_start = date.fromisoformat(application["start_date"])
        existing_end = date.fromisoformat(application["end_date"])

        if start_date <= existing_end and end_date >= existing_start:
            raise ValueError(
                "You already have a pending or approved leave request for these dates."
            )

    # 6. Create application
    application = {
        "application_id": str(uuid.uuid4()),
        "employee_id": employee_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "days_requested": days_requested,
        "status": "pending",
    }

    # 7. Save application
    applications.append(application)
    write_json(APPLICATIONS_FILE, applications)

    logger.info("Leave application submitted for employee: %s", employee_id)

    return application


def get_pending_leave_requests():
    applications = read_json(APPLICATIONS_FILE)

    pending_requests = [
        application
        for application in applications
        if application["status"] == "pending"
    ]

    logger.info("Retrieved pending leave requests")
    return pending_requests


def review_leave_application(application_id: str, decision: str):
    # 1. Validate manager's decision
    decision = decision.strip().lower()

    if decision not in ("approve", "reject"):
        raise ValueError("Decision must be 'approve' or 'reject'.")

    # Convert the manager's decision into the application status
    status = "approved" if decision == "approve" else "rejected"

    # 2. Find the application
    applications = read_json(APPLICATIONS_FILE)

    application = next(
        (item for item in applications if item["application_id"] == application_id),
        None,
    )

    if application is None:
        raise ValueError("Leave application not found.")

    # 3. Only pending applications can be reviewed
    if application["status"] != "pending":
        raise ValueError("This application has already been reviewed.")

    # 4. Deduct balance only if approved
    if status == "approved":
        employees = read_json(EMPLOYEES_FILE)

        employee = employees.get(application["employee_id"])

        if employee is None:
            raise ValueError(
                "Employee associated with this application does not exist."
            )

        days_requested = application["days_requested"]
        balance = employee["annual_leave_balance"]

        if days_requested > balance:
            raise ValueError(
                f"Insufficient leave balance. Available: {balance}, "
                f"Requested: {days_requested}."
            )

        employee["annual_leave_balance"] -= days_requested
        write_json(EMPLOYEES_FILE, employees)

    # 5. Update application status
    application["status"] = status
    write_json(APPLICATIONS_FILE, applications)

    logger.info(
        "Leave application %s was %s",
        application_id,
        status,
    )

    return application
