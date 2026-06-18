# orchestrator.py — Routes tasks to the right agent, logs all runs
from agents.call_center_agent import CallCenterAgent
from agents.billing_agent import BillingAgent
from agents.marketing_agent import MarketingAgent
from agents.recruiting_agent import RecruitingAgent
from tools.db_tool import save_log, get_logs
from tools.crm_tool import get_kpis

AGENTS = {
    "call_center": CallCenterAgent(),
    "billing": BillingAgent(),
    "marketing": MarketingAgent(),
    "recruiting": RecruitingAgent(),
}


def run_agent(department: str, task: str) -> dict:
    if department not in AGENTS:
        return {"error": f"Unknown department: {department}"}

    agent = AGENTS[department]
    result = agent.run(task)
    save_log(
        {
            "department": department,
            "task": task,
            "steps_count": len(result["steps"]),
            "summary": result["response"][:300],
        }
    )
    return result


def get_all_agent_statuses() -> list[dict]:
    return [
        {
            "id": key,
            "name": agent.name,
            "department": agent.department,
            "description": agent.description,
        }
        for key, agent in AGENTS.items()
    ]


def get_system_kpis() -> dict:
    crm = get_kpis()
    logs = get_logs(limit=100)
    return {
        **crm,
        "total_agent_runs": len(logs),
        "departments_active": len(AGENTS),
    }
