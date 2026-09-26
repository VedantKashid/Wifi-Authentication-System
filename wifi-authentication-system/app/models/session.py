"""Network/portal session queries."""

import sqlite3
from datetime import datetime


class Session:
    @staticmethod
    def create(conn: sqlite3.Connection, user_id: int, ip_address: str, device_type: str) -> None:
        conn.execute(
            """INSERT INTO sessions (user_id, ip_address, device_type, login_time, status)
               VALUES (?, ?, ?, ?, 'active')""",
            (user_id, ip_address, device_type, datetime.now().isoformat(timespec="seconds")),
        )

    @staticmethod
    def close_active_for_user(conn: sqlite3.Connection, user_id: int) -> None:
        conn.execute(
            """UPDATE sessions SET logout_time = ?, status = 'closed'
               WHERE user_id = ? AND status = 'active'""",
            (datetime.now().isoformat(timespec="seconds"), user_id),
        )
        conn.commit()

    @staticmethod
    def count_active(conn: sqlite3.Connection) -> int:
        return conn.execute("SELECT COUNT(*) FROM sessions WHERE status = 'active'").fetchone()[0]

    @staticmethod
    def device_breakdown(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(
            """SELECT COALESCE(device_type, 'Unknown') AS device, COUNT(*) AS total
               FROM sessions GROUP BY device_type ORDER BY total DESC"""
        ).fetchall()

    @staticmethod
    def recent_with_username(conn: sqlite3.Connection, limit: int = 100) -> list[sqlite3.Row]:
        return conn.execute(
            """SELECT sessions.*, users.username FROM sessions
               JOIN users ON users.id = sessions.user_id
               ORDER BY sessions.id DESC LIMIT ?""",
            (limit,),
        ).fetchall()
