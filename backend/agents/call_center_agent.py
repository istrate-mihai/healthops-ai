# call_center_agent.py
from .base_agent import BaseAgent
from tools.crm_tool import get_contacts, get_tickets, update_contact_status
from tools.calendar_tool import (
    get_upcoming_appointments,
    reschedule_appointment,
    get_available_slots,
)


class CallCenterAgent(BaseAgent):
    name = "CallCenter Agent"
    department = "call_center"
    description = (
        "Handles appointment scheduling, patient routing, and call queue triage"
    )

    @property
    def system_prompt(self) -> str:
        return """You are an AI agent managing a healthcare call center.
Your job: triage open tickets, check upcoming appointments, reschedule when needed, 
and update contact statuses in the CRM. Always explain your reasoning step by step.
Be concise but thorough. Output a structured summary of actions taken."""

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "get_contacts",
                "description": "Fetch contacts filtered by department",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "Filter by department name",
                        }
                    },
                },
            },
            {
                "name": "get_tickets",
                "description": "Fetch open support tickets, optionally filtered by priority",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "priority": {
                            "type": "string",
                            "enum": ["high", "medium", "low"],
                        }
                    },
                },
            },
            {
                "name": "get_upcoming_appointments",
                "description": "Get scheduled appointments in the next N days",
                "input_schema": {
                    "type": "object",
                    "properties": {"days": {"type": "integer", "default": 7}},
                },
            },
            {
                "name": "reschedule_appointment",
                "description": "Reschedule an appointment to a new date and time",
                "input_schema": {
                    "type": "object",
                    "required": ["appointment_id", "new_date", "new_time"],
                    "properties": {
                        "appointment_id": {"type": "string"},
                        "new_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "new_time": {"type": "string", "description": "HH:MM"},
                    },
                },
            },
            {
                "name": "update_contact_status",
                "description": "Update a contact's CRM status",
                "input_schema": {
                    "type": "object",
                    "required": ["contact_id", "new_status"],
                    "properties": {
                        "contact_id": {"type": "string"},
                        "new_status": {"type": "string"},
                    },
                },
            },
        ]

    def dispatch_tool(self, tool_name: str, tool_input: dict):
        match tool_name:
            case "get_contacts":
                return get_contacts(**tool_input)
            case "get_tickets":
                return get_tickets(**tool_input)
            case "get_upcoming_appointments":
                return get_upcoming_appointments(**tool_input)
            case "reschedule_appointment":
                return reschedule_appointment(**tool_input)
            case "update_contact_status":
                return update_contact_status(**tool_input)
            case _:
                return {"error": f"Unknown tool: {tool_name}"}
