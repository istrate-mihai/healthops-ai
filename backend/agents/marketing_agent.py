# marketing_agent.py
from .base_agent import BaseAgent
from tools.crm_tool import get_contacts, get_kpis, update_contact_status


class MarketingAgent(BaseAgent):
    name = "Marketing Agent"
    department = "marketing"
    description = "Segments leads, identifies re-engagement targets, generates campaign recommendations"

    @property
    def system_prompt(self) -> str:
        return """You are an AI agent managing healthcare marketing operations.
Your job: analyze the contact database, segment patients and leads, 
identify re-engagement opportunities, and recommend targeted outreach campaigns.
Output a structured campaign recommendation report."""

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "get_contacts",
                "description": "Fetch all contacts or filter by department",
                "input_schema": {
                    "type": "object",
                    "properties": {"department": {"type": "string"}},
                },
            },
            {
                "name": "get_kpis",
                "description": "Fetch current CRM KPIs and pipeline metrics",
                "input_schema": {"type": "object", "properties": {}},
            },
            {
                "name": "update_contact_status",
                "description": "Tag a contact for a campaign",
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
            case "get_kpis":
                return get_kpis()
            case "update_contact_status":
                return update_contact_status(**tool_input)
            case _:
                return {"error": f"Unknown tool: {tool_name}"}
