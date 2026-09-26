"""
Application factory for the WiFi Authentication System.

Usage:
    from app import create_app
    app = create_app()
    app.run()
"""

from datetime import timedelta

from flask import Flask

from app.config import get_config
from app.extensions import init_app as init_extensions
from app.extensions import init_db


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        minutes=app.config["PERMANENT_SESSION_LIFETIME_MINUTES"]
    )

    init_extensions(app)
    init_db(app)

    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.portal import portal_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        return {"wifi_ssid": app.config["WIFI_SSID"]}

    return app
