# db_tool.py — Persistent JSON log storage (replaces a real DB for demo)
import json
from pathlib import Path
from datetime import datetime

LOGS_FILE = Path(__file__).parent.parent / "storage" / "logs.json"
KPIS_FILE = Path(__file__).parent.parent / "storage" / "kpis.json"


def _ensure_files():
    LOGS_FILE.parent.mkdir(exist_ok=True)
    if not LOGS_FILE.exists() or LOGS_FILE.read_text().strip() == "":
        LOGS_FILE.write_text("[]")
    if not KPIS_FILE.exists() or KPIS_FILE.read_text().strip() == "":
        KPIS_FILE.write_text("{}")


def save_log(entry: dict) -> None:
    _ensure_files()
    logs = json.loads(LOGS_FILE.read_text())
    logs.append({**entry, "timestamp": datetime.utcnow().isoformat()})
    LOGS_FILE.write_text(json.dumps(logs[-100:], indent=2))  # keep last 100


def get_logs(limit: int = 20) -> list[dict]:
    _ensure_files()
    logs = json.loads(LOGS_FILE.read_text())
    return logs[-limit:][::-1]  # most recent first


def save_kpis(kpis: dict) -> None:
    _ensure_files()
    existing = json.loads(KPIS_FILE.read_text())
    existing[datetime.utcnow().isoformat()] = kpis
    KPIS_FILE.write_text(json.dumps(existing, indent=2))
