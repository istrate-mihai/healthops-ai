# crm_tool.py — Simulates HubSpot CRM reads/writes (MCP-style tool)
import json
from datetime import datetime
from pathlib import Path

MOCK_DB = {
    "contacts": [
        {
            "id": "c1",
            "name": "Ana Popescu",
            "status": "lead",
            "department": "billing",
            "value": 1200,
        },
        {
            "id": "c2",
            "name": "Ion Gheorghe",
            "status": "appointment_scheduled",
            "department": "call_center",
            "value": 0,
        },
        {
            "id": "c3",
            "name": "Maria Ionescu",
            "status": "candidate",
            "department": "recruiting",
            "value": 0,
        },
        {
            "id": "c4",
            "name": "Radu Popa",
            "status": "patient",
            "department": "marketing",
            "value": 850,
        },
    ],
    "tickets": [
        {
            "id": "t1",
            "contact_id": "c1",
            "issue": "Invoice dispute - overcharged $200",
            "priority": "high",
        },
        {
            "id": "t2",
            "contact_id": "c2",
            "issue": "Missed appointment rescheduling needed",
            "priority": "medium",
        },
    ],
}


def get_contacts(department: str | None = None) -> list[dict]:
    if department:
        return [c for c in MOCK_DB["contacts"] if c["department"] == department]
    return MOCK_DB["contacts"]


def get_tickets(priority: str | None = None) -> list[dict]:
    if priority:
        return [t for t in MOCK_DB["tickets"] if t["priority"] == priority]
    return MOCK_DB["tickets"]


def update_contact_status(contact_id: str, new_status: str) -> dict:
    for c in MOCK_DB["contacts"]:
        if c["id"] == contact_id:
            old = c["status"]
            c["status"] = new_status
            return {
                "updated": True,
                "contact_id": contact_id,
                "old_status": old,
                "new_status": new_status,
            }
    return {"updated": False, "error": "Contact not found"}


def get_kpis() -> dict:
    contacts = MOCK_DB["contacts"]
    return {
        "total_contacts": len(contacts),
        "leads": len([c for c in contacts if c["status"] == "lead"]),
        "pipeline_value": sum(c["value"] for c in contacts),
        "open_tickets": len(MOCK_DB["tickets"]),
        "high_priority_tickets": len(
            [t for t in MOCK_DB["tickets"] if t["priority"] == "high"]
        ),
    }
