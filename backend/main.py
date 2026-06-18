# main.py — FastAPI entry point
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from orchestrator import run_agent, get_all_agent_statuses, get_system_kpis
from tools.db_tool import get_logs

app = FastAPI(title="HealthOps AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunAgentRequest(BaseModel):
    department: str
    task: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/agents")
def list_agents():
    return get_all_agent_statuses()


@app.post("/agents/run")
def trigger_agent(req: RunAgentRequest):
    result = run_agent(req.department, req.task)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/logs")
def logs(limit: int = 20):
    return get_logs(limit=limit)


@app.get("/kpis")
def kpis():
    return get_system_kpis()
