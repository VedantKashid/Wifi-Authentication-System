"""Login attempt / brute-force tracking queries."""

import sqlite3
from datetime import datetime, timedelta


class LoginAttempt:
    @staticmethod
    def record(conn: sqlite3.Connection, username: str, ip_address: str, status: str) -> None:
        conn.execute(
            "INSERT INTO login_attempts (username, ip_address, attempt_time, status) "
            "VALUES (?, ?, ?, ?)",
            (username, ip_address, datetime.now().isoformat(timespec="seconds"), status),
        )
        conn.commit()

    @staticmethod
    def recent_failed_count(conn: sqlite3.Connection, username: str, window_minutes: int) -> int:
        cutoff = (datetime.now() - timedelta(minutes=window_minutes)).isoformat(timespec="seconds")
        return conn.execute(
            """SELECT COUNT(*) AS count FROM login_attempts
               WHERE username = ? AND status = 'FAILED' AND attempt_time >= ?""",
            (username, cutoff),
        ).fetchone()["count"]

    @staticmethod
    def count_successful(conn: sqlite3.Connection) -> int:
        return conn.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE status='SUCCESS'"
        ).fetchone()[0]

    @staticmethod
    def count_failed_or_blocked(conn: sqlite3.Connection) -> int:
        return conn.execute(
            "SELECT COUNT(*) FROM login_attempts WHERE status IN ('FAILED','BLOCKED')"
        ).fetchone()[0]

    @staticmethod
    def weekly_success_counts(conn: sqlite3.Connection, days: int = 7) -> list[dict]:
        """Successful login counts for each of the last `days` days, oldest first."""
        weekly = []
        for i in range(days - 1, -1, -1):
            day = (datetime.now() - timedelta(days=i)).date()
            count = conn.execute(
                "SELECT COUNT(*) FROM login_attempts WHERE status='SUCCESS' AND date(attempt_time)=?",
                (day.isoformat(),),
            ).fetchone()[0]
            weekly.append({"label": day.strftime("%a"), "value": count})
        return weekly

    @staticmethod
    def recent(conn: sqlite3.Connection, limit: int = 6) -> list[sqlite3.Row]:
        return conn.execute(
            "SELECT * FROM login_attempts ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()

    @staticmethod
    def recent_log(conn: sqlite3.Connection, limit: int = 100) -> list[sqlite3.Row]:
        return conn.execute(
            "SELECT * FROM login_attempts ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
