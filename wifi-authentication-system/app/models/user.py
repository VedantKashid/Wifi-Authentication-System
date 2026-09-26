"""User account queries."""

import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash


class User:
    @staticmethod
    def create(conn: sqlite3.Connection, username: str, email: str, password: str) -> None:
        """Insert a new standard user. Raises sqlite3.IntegrityError on a
        duplicate username or email so the caller can show a friendly error."""
        conn.execute(
            """INSERT INTO users (username, email, password_hash, role, status, created_at)
               VALUES (?, ?, ?, 'user', 'active', ?)""",
            (
                username,
                email,
                generate_password_hash(password),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()

    @staticmethod
    def get_by_username(conn: sqlite3.Connection, username: str) -> sqlite3.Row | None:
        return conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    @staticmethod
    def list_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(
            """SELECT id, username, email, role, status, created_at, last_login
               FROM users ORDER BY id DESC"""
        ).fetchall()

    @staticmethod
    def update_last_login(conn: sqlite3.Connection, user_id: int, when: str) -> None:
        conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (when, user_id))

    @staticmethod
    def toggle_status(conn: sqlite3.Connection, user_id: int) -> str | None:
        """Flip a user's status between active/disabled. Returns the new
        status, or None if the user does not exist."""
        user = conn.execute(
            "SELECT username, status FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None
        new_status = "disabled" if user["status"] == "active" else "active"
        conn.execute("UPDATE users SET status = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
        return new_status

    @staticmethod
    def count(conn: sqlite3.Connection) -> int:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    @staticmethod
    def count_active(conn: sqlite3.Connection) -> int:
        return conn.execute("SELECT COUNT(*) FROM users WHERE status='active'").fetchone()[0]
