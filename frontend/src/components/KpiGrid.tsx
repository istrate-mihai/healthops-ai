// KpiGrid.tsx
import { KPIs } from "../api/client";

const KpiBox = ({ label, value }: { label: string; value: string | number }) => (
  <div style={{ background: "#1e2330", borderRadius: 8, padding: "1rem 1.25rem", border: "1px solid #2d3748" }}>
    <div style={{ fontSize: "0.75rem", color: "#64748b", marginBottom: 4 }}>{label}</div>
    <div style={{ fontSize: "1.5rem", fontWeight: 700, color: "#e2e8f0" }}>{value}</div>
  </div>
);

export const KpiGrid = ({ kpis }: { kpis: KPIs }) => (
  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: "1rem" }}>
    <KpiBox label="Total Contacts" value={kpis.total_contacts} />
    <KpiBox label="Open Leads" value={kpis.leads} />
    <KpiBox label="Pipeline Value" value={`$${kpis.pipeline_value.toLocaleString()}`} />
    <KpiBox label="Open Tickets" value={kpis.open_tickets} />
    <KpiBox label="High Priority" value={kpis.high_priority_tickets} />
    <KpiBox label="Agent Runs" value={kpis.total_agent_runs} />
    <KpiBox label="Depts Active" value={kpis.departments_active} />
  </div>
);
