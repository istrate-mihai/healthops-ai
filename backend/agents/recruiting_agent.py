# recruiting_agent.py
from .base_agent import BaseAgent
from tools.crm_tool import get_contacts, update_contact_status
from tools.calendar_tool import get_available_slots


class RecruitingAgent(BaseAgent):
    name = "Recruiting Agent"
    department = "recruiting"
    description = "Screens candidates, schedules interviews, tracks pipeline stages"

    @property
    def system_prompt(self) -> str:
        return """You are an AI agent managing healthcare recruiting operations.
Your job: review candidate contacts, assess pipeline stages, 
schedule interviews using available calendar slots, and advance qualified candidates.
Output a structured recruiting pipeline report with recommended next actions."""

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "get_contacts",
                "description": "Fetch recruiting pipeline candidates",
                "input_schema": {
                    "type": "object",
                    "properties": {"department": {"type": "string"}},
                },
            },
            {
                "name": "get_available_slots",
                "description": "Get available interview slots for a date",
                "input_schema": {
                    "type": "object",
                    "required": ["date"],
                    "properties": {
                        "date": {"type": "string", "description": "YYYY-MM-DD"}
                    },
                },
            },
            {
                "name": "update_contact_status",
                "description": "Advance candidate to next pipeline stage",
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
            case "get_available_slots":
                return get_available_slots(**tool_input)
            case "update_contact_status":
                return update_contact_status(**tool_input)
            case _:
                return {"error": f"Unknown tool: {tool_name}"}
