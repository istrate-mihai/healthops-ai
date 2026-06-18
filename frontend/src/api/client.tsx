// client.ts — All API calls to FastAPI backend
const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface AgentStatus {
  id: string;
  name: string;
  department: string;
  description: string;
}

export interface RunResult {
  agent: string;
  department: string;
  task: string;
  steps: Array<{ tool: string; input: unknown; output: unknown }>;
  response: string;
}

export interface LogEntry {
  department: string;
  task: string;
  steps_count: number;
  summary: string;
  timestamp: string;
}

export interface KPIs {
  total_contacts: number;
  leads: number;
  pipeline_value: number;
  open_tickets: number;
  high_priority_tickets: number;
  total_agent_runs: number;
  departments_active: number;
}

export const api = {
  getAgents: (): Promise<AgentStatus[]> =>
    fetch(`${BASE}/agents`).then(r => r.json()),

  runAgent: (department: string, task: string): Promise<RunResult> =>
    fetch(`${BASE}/agents/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ department, task }),
    }).then(r => r.json()),

  getLogs: (limit = 20): Promise<LogEntry[]> =>
    fetch(`${BASE}/logs?limit=${limit}`).then(r => r.json()),

  getKPIs: (): Promise<KPIs> =>
    fetch(`${BASE}/kpis`).then(r => r.json()),
};
