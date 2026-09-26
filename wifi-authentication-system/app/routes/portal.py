"""The authenticated captive-portal landing page shown after login."""

from flask import Blueprint, render_template

from app.extensions import get_db
from app.models.session import Session
from app.utils.decorators import login_required

portal_bp = Blueprint("portal", __name__)


@portal_bp.route("/portal")
@login_required
def portal():
    conn = get_db()
    active_sessions = Session.count_active(conn)
    return render_template("portal/portal.html", active_sessions=active_sessions)
