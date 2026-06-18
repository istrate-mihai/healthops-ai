// RunAgentPanel.tsx
import { RunResult } from "../api/client";

export const RunAgentPanel = ({ task, onTaskChange, onRun, loading, result }: {
  task: string;
  onTaskChange: (v: string) => void;
  onRun: () => void;
  loading: boolean;
  result: RunResult | null;
}) => (
  <section style={{ marginTop: "2rem" }}>
    <h2 style={{ fontSize: "1rem", fontWeight: 600, color: "#94a3b8", marginBottom: "1rem" }}>RUN AGENT</h2>
    <textarea
      value={task}
      onChange={e => onTaskChange(e.target.value)}
      rows={3}
      style={{
        width: "100%", background: "#1e2330", border: "1px solid #2d3748",
        color: "#e2e8f0", borderRadius: 8, padding: "0.75rem", fontSize: "0.9rem",
        resize: "vertical", boxSizing: "border-box",
      }}
    />
    <button
      onClick={onRun}
      disabled={loading}
      style={{
        marginTop: "0.75rem", background: loading ? "#374151" : "#3b82f6",
        color: "#fff", border: "none", borderRadius: 6, padding: "0.6rem 1.5rem",
        fontWeight: 600, cursor: loading ? "not-allowed" : "pointer", fontSize: "0.9rem",
      }}
    >
      {loading ? "Running..." : "▶ Run Agent"}
    </button>

    {result && (
      <div style={{ marginTop: "1rem", background: "#1e2330", borderRadius: 8, padding: "1rem", border: "1px solid #2d3748" }}>
        <div style={{ fontSize: "0.75rem", color: "#64748b", marginBottom: "0.5rem" }}>
          {result.steps.length} tool calls · {result.agent}
        </div>
        <div style={{ fontSize: "0.85rem", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>{result.response}</div>
        {result.steps.length > 0 && (
          <details style={{ marginTop: "0.75rem" }}>
            <summary style={{ fontSize: "0.75rem", color: "#64748b", cursor: "pointer" }}>Tool call trace</summary>
            <pre style={{ fontSize: "0.7rem", color: "#94a3b8", overflowX: "auto", marginTop: "0.5rem" }}>
              {JSON.stringify(result.steps, null, 2)}
            </pre>
          </details>
        )}
      </div>
    )}
  </section>
);
