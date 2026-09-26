"""Administrator action audit-log queries."""

import sqlite3
from datetime import datetime


class AdminLog:
    @staticmethod
    def record(conn: sqlite3.Connection, admin_id: int, action: str, ip_address: str) -> None:
        conn.execute(
            "INSERT INTO admin_logs (admin_id, action, ip_address, timestamp) VALUES (?, ?, ?, ?)",
            (admin_id, action, ip_address, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()

    @staticmethod
    def recent(conn: sqlite3.Connection, limit: int = 100) -> list[sqlite3.Row]:
        return conn.execute(
            "SELECT * FROM admin_logs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
