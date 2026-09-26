"""
Database wiring for the application.

The project uses plain SQLite (no ORM) so the schema stays transparent
and easy to inspect for a lab/demo environment. A single connection is
kept per request context via Flask's `g` object and closed automatically
when the request ends.
"""

import os
import sqlite3
from datetime import datetime

from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db() -> sqlite3.Connection:
    """Return the request-scoped SQLite connection, creating it if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exception=None) -> None:
    """Close the request-scoped connection, if one was opened."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app) -> None:
    """Create tables (if missing), migrate older databases, and seed the
    default administrator account. Safe to call on every startup."""
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)

    with app.app_context():
        conn = get_db()

        with open(app.config["SCHEMA_PATH"], "r", encoding="utf-8") as schema_file:
            conn.executescript(schema_file.read())

        # Backward-compatible migration for databases created by older
        # versions of this project that predate the device_type column.
        columns = {row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()}
        if "device_type" not in columns:
            conn.execute("ALTER TABLE sessions ADD COLUMN device_type TEXT DEFAULT 'Unknown'")

        _seed_default_admin(conn, app.config)
        conn.commit()


def _seed_default_admin(conn: sqlite3.Connection, config) -> None:
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?", (config["DEFAULT_ADMIN_USERNAME"],)
    ).fetchone()
    if existing:
        return

    now = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        """INSERT INTO users (username, email, password_hash, role, status, created_at)
           VALUES (?, ?, ?, 'admin', 'active', ?)""",
        (
            config["DEFAULT_ADMIN_USERNAME"],
            config["DEFAULT_ADMIN_EMAIL"],
            generate_password_hash(config["DEFAULT_ADMIN_PASSWORD"]),
            now,
        ),
    )


def init_app(app) -> None:
    """Register teardown handling with the Flask app."""
    app.teardown_appcontext(close_db)
