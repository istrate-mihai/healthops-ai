# calendar_tool.py — Simulates appointment/scheduling operations
from datetime import datetime, timedelta
import random

APPOINTMENTS = [
    {
        "id": "a1",
        "contact_id": "c2",
        "date": "2025-06-20",
        "time": "10:00",
        "type": "consultation",
        "status": "scheduled",
    },
    {
        "id": "a2",
        "contact_id": "c4",
        "date": "2025-06-18",
        "time": "14:30",
        "type": "follow-up",
        "status": "completed",
    },
]


def get_upcoming_appointments(days: int = 7) -> list[dict]:
    return [a for a in APPOINTMENTS if a["status"] == "scheduled"]


def reschedule_appointment(appointment_id: str, new_date: str, new_time: str) -> dict:
    for a in APPOINTMENTS:
        if a["id"] == appointment_id:
            a["date"] = new_date
            a["time"] = new_time
            return {"rescheduled": True, "appointment": a}
    return {"rescheduled": False, "error": "Appointment not found"}


def get_available_slots(date: str) -> list[str]:
    # Simulates available booking slots
    base_slots = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
    taken = {a["time"] for a in APPOINTMENTS if a["date"] == date}
    return [s for s in base_slots if s not in taken]
