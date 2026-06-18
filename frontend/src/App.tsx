// App.tsx
import { useState, useEffect } from "react";
import { api, AgentStatus, RunResult, LogEntry, KPIs } from "./api/client";
import { KpiGrid } from "./components/KpiGrid";
import { AgentCard } from "./components/AgentCard";
import { RunAgentPanel } from "./components/RunAgentPanel";
import { LogsTable } from "./components/LogsTable";

const DEFAULT_TASKS: Record<string, string> = {
  call_center: "Review all high-priority tickets and reschedule any missed appointments. Update contact statuses where needed.",
  billing: "Audit all open billing tickets, prioritize by value, and recommend resolution actions for high-priority disputes.",
  marketing: "Analyze the contact database and generate a targeted re-engagement campaign recommendation for inactive patients.",
  recruiting: "Review the candidate pipeline, check available interview slots for 2025-06-25, and advance qualified candidates.",
};

export default function App() {
  const [agents, setAgents] = useState<AgentStatus[]>([]);
  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [result, setResult] = useState<RunResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<string>("call_center");
  const [task, setTask] = useState(DEFAULT_TASKS["call_center"]);

  const refresh = async () => {
    const [a, k, l] = await Promise.all([api.getAgents(), api.getKPIs(), api.getLogs()]);
    setAgents(a);
    setKpis(k);
    setLogs(l);
  };

  useEffect(() => { refresh(); }, []);

  const handleRun = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await api.runAgent(selected, task);
      setResult(res);
      await refresh();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Inter, sans-serif", background: "#0f1117", minHeight: "100vh", color: "#e2e8f0", padding: "2rem" }}>
      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 700, color: "#fff" }}>
          🏥 HealthOps AI <span style={{ fontSize: "0.9rem", color: "#64748b", fontWeight: 400 }}>Agent Ecosystem</span>
        </h1>
      </header>

      {kpis && <KpiGrid kpis={kpis} />}

      <section style={{ marginTop: "2rem" }}>
        <h2 style={{ fontSize: "1rem", fontWeight: 600, color: "#94a3b8", marginBottom: "1rem" }}>AGENTS</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "1rem" }}>
          {agents.map(a => (
            <AgentCard
              key={a.id}
              agent={a}
              selected={selected === a.id}
              onClick={() => { setSelected(a.id); setTask(DEFAULT_TASKS[a.id] ?? ""); }}
            />
          ))}
        </div>
      </section>

      <RunAgentPanel
        task={task}
        onTaskChange={setTask}
        onRun={handleRun}
        loading={loading}
        result={result}
      />

      <section style={{ marginTop: "2rem" }}>
        <h2 style={{ fontSize: "1rem", fontWeight: 600, color: "#94a3b8", marginBottom: "1rem" }}>RECENT RUNS</h2>
        <LogsTable logs={logs} />
      </section>
    </div>
  );
}
