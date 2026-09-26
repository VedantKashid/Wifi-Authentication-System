"""
Application configuration.

Settings are read from environment variables so that secrets and
per-deployment values (secret key, WiFi SSID, database location) never
need to be hard-coded into source control. See `.env.example` for the
variables this project understands.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    WIFI_SSID = os.environ.get("WIFI_SSID", "SecureNet-WiFi")

    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "database.db")
    )
    SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

    PERMANENT_SESSION_LIFETIME_MINUTES = int(
        os.environ.get("SESSION_TIMEOUT_MINUTES", "30")
    )

    # Brute-force protection
    MAX_FAILED_ATTEMPTS = int(os.environ.get("MAX_FAILED_ATTEMPTS", "5"))
    LOCKOUT_WINDOW_MINUTES = int(os.environ.get("LOCKOUT_WINDOW_MINUTES", "10"))

    # Seeded administrator account (created on first run if it doesn't exist)
    DEFAULT_ADMIN_USERNAME = os.environ.get("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@example.com")
    DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "Admin@12345")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(name: str | None = None):
    name = name or os.environ.get("FLASK_ENV", "default")
    return CONFIG_MAP.get(name, DevelopmentConfig)
