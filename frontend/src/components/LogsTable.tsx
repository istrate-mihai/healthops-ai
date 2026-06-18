// LogsTable.tsx
import { LogEntry } from "../api/client";

export const LogsTable = ({ logs }: { logs: LogEntry[] }) => (
  <div style={{ overflowX: "auto" }}>
    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.8rem" }}>
      <thead>
        <tr style={{ color: "#64748b", textAlign: "left" }}>
          {["Timestamp", "Department", "Steps", "Summary"].map(h => (
            <th key={h} style={{ padding: "0.5rem 0.75rem", borderBottom: "1px solid #2d3748" }}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {logs.map((log, i) => (
          <tr key={i} style={{ borderBottom: "1px solid #1e2330" }}>
            <td style={{ padding: "0.5rem 0.75rem", color: "#64748b" }}>
              {new Date(log.timestamp).toLocaleString()}
            </td>
            <td style={{ padding: "0.5rem 0.75rem", color: "#94a3b8" }}>{log.department}</td>
            <td style={{ padding: "0.5rem 0.75rem", color: "#94a3b8" }}>{log.steps_count}</td>
            <td style={{ padding: "0.5rem 0.75rem", color: "#e2e8f0", maxWidth: 400 }}>{log.summary}</td>
          </tr>
        ))}
        {logs.length === 0 && (
          <tr><td colSpan={4} style={{ padding: "1rem", color: "#64748b", textAlign: "center" }}>No runs yet</td></tr>
        )}
      </tbody>
    </table>
  </div>
);
