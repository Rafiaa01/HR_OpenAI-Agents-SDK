from datetime import date

from pydantic import BaseModel


class LeaveApplicationRequest(BaseModel):
    employee_id: str
    start_date: date
    end_date: date