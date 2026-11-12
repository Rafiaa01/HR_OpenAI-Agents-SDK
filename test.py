from datetime import date

import pytest
from src.services.leave_service import (
    apply_leave,
    calculate_working_days,
)


def test_calculate_working_days():
    assert calculate_working_days(
        date(2026, 11, 9),
        date(2026, 11, 11)
    ) == 3


def test_apply_leave():
    result = apply_leave(
        "EMP001",
        date(2026, 11, 16),
        date(2026, 11, 18)
    )

    assert result["employee_id"] == "EMP001"
    assert result["days_requested"] == 3
    assert result["status"] == "pending"


def test_invalid_employee():
    with pytest.raises(ValueError):
        apply_leave(
            "EMP999",
            date(2026, 11, 16),
            date(2026, 11, 18)
        )


def test_end_date_before_start_date():
    with pytest.raises(ValueError):
        apply_leave(
            "EMP001",
            date(2026, 11, 18),
            date(2026, 11, 16)
        )