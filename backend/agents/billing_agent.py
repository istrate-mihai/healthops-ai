# billing_agent.py
from .base_agent import BaseAgent
from tools.crm_tool import get_contacts, get_tickets, update_contact_status


class BillingAgent(BaseAgent):
    name = "Billing Agent"
    department = "billing"
    description = (
        "Resolves billing disputes, flags high-value accounts, tracks payment statuses"
    )

    @property
    def system_prompt(self) -> str:
        return """You are an AI agent managing healthcare billing operations.
Your job: review open billing tickets, prioritize disputes by value and urgency,
recommend resolution actions, and update CRM statuses. Output a structured report
of findings and actions taken."""

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "get_contacts",
                "description": "Fetch billing department contacts",
                "input_schema": {
                    "type": "object",
                    "properties": {"department": {"type": "string"}},
                },
            },
            {
                "name": "get_tickets",
                "description": "Fetch billing tickets by priority",
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
                "name": "update_contact_status",
                "description": "Update contact billing status in CRM",
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
            case "update_contact_status":
                return update_contact_status(**tool_input)
            case _:
                return {"error": f"Unknown tool: {tool_name}"}
