"""Data-access models for the WiFi authentication system.

Each model is a thin, static wrapper around the SQLite tables defined in
`database/schema.sql`. Keeping the SQL here (instead of scattered across
route handlers) makes the query surface easy to review and audit.
"""
