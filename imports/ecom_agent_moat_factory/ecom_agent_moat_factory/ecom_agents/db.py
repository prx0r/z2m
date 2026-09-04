from __future__ import annotations
import json, sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from .settings import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  merchant_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  subject_id TEXT,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_merchant_type ON events(merchant_id,event_type);
CREATE TABLE IF NOT EXISTS handoffs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  merchant_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  customer_ref TEXT,
  reason TEXT NOT NULL,
  summary TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS claims (
  claim_id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  sku TEXT NOT NULL,
  claim_type TEXT NOT NULL,
  decision TEXT NOT NULL,
  confidence REAL NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS delivery_cases (
  case_id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  severity INTEGER NOT NULL,
  recommended_action TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS return_cases (
  case_id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  sku TEXT NOT NULL,
  decision TEXT NOT NULL,
  saved_revenue REAL NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reorder_cases (
  case_id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  score REAL NOT NULL,
  action TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@contextmanager
def connect(path: str | None = None):
    db_path = path or settings.database_path
    if db_path != ':memory:':
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()

def record_event(merchant_id: str, event_type: str, payload: dict, subject_id: str | None = None, path: str | None = None) -> int:
    with connect(path) as conn:
        cur = conn.execute(
            "INSERT INTO events(merchant_id,event_type,subject_id,payload_json,created_at) VALUES(?,?,?,?,?)",
            (merchant_id,event_type,subject_id,json.dumps(payload,sort_keys=True),now_iso()),
        )
        return int(cur.lastrowid)
