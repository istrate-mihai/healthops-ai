// AgentCard.tsx
import { AgentStatus } from "../api/client";

const COLORS: Record<string, string> = {
  call_center: "#3b82f6",
  billing: "#f59e0b",
  marketing: "#10b981",
  recruiting: "#8b5cf6",
};

export const AgentCard = ({ agent, selected, onClick }: {
  agent: AgentStatus;
  selected: boolean;
  onClick: () => void;
}) => (
  <div
    onClick={onClick}
    style={{
      background: selected ? "#1e2d40" : "#1e2330",
      border: `1px solid ${selected ? COLORS[agent.id] ?? "#3b82f6" : "#2d3748"}`,
      borderRadius: 8,
      padding: "1rem",
      cursor: "pointer",
      transition: "border-color 0.15s",
    }}
  >
    <div style={{ fontSize: "0.7rem", color: COLORS[agent.id] ?? "#64748b", fontWeight: 600, marginBottom: 4 }}>
      {agent.department.toUpperCase()}
    </div>
    <div style={{ fontWeight: 600, fontSize: "0.9rem", marginBottom: 4 }}>{agent.name}</div>
    <div style={{ fontSize: "0.75rem", color: "#64748b" }}>{agent.description}</div>
  </div>
);
