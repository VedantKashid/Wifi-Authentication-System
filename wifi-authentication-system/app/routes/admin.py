"""Administrator dashboard, user management, session monitoring and
authentication/audit logs."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.extensions import get_db
from app.models.admin_log import AdminLog
from app.models.login_attempt import LoginAttempt
from app.models.session import Session
from app.models.user import User
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    conn = get_db()
    stats = {
        "users": User.count(conn),
        "active_users": User.count_active(conn),
        "successful_logins": LoginAttempt.count_successful(conn),
        "failed_logins": LoginAttempt.count_failed_or_blocked(conn),
        "active_sessions": Session.count_active(conn),
    }
    weekly = LoginAttempt.weekly_success_counts(conn, days=7)
    devices = Session.device_breakdown(conn)
    recent = LoginAttempt.recent(conn, limit=6)
    return render_template(
        "admin/dashboard.html", stats=stats, weekly=weekly, devices=devices, recent=recent
    )


@admin_bp.route("/users")
@admin_required
def users():
    conn = get_db()
    all_users = User.list_all(conn)
    return render_template("admin/users.html", users=all_users)


@admin_bp.post("/users/<int:user_id>/toggle")
@admin_required
def toggle_user(user_id):
    if user_id == session.get("user_id"):
        flash("You cannot disable your own admin account.", "danger")
        return redirect(url_for("admin.users"))

    conn = get_db()
    user = User.get_by_id(conn, user_id)
    new_status = User.toggle_status(conn, user_id)
    if new_status:
        AdminLog.record(
            conn,
            session["user_id"],
            f"{new_status.upper()} user {user['username']}",
            request.remote_addr or "unknown",
        )
        flash(f"User {user['username']} is now {new_status}.", "success")

    return redirect(url_for("admin.users"))


@admin_bp.route("/logs")
@admin_required
def logs():
    conn = get_db()
    login_logs = LoginAttempt.recent_log(conn, limit=100)
    admin_logs = AdminLog.recent(conn, limit=100)
    return render_template("admin/logs.html", login_logs=login_logs, admin_logs=admin_logs)


@admin_bp.route("/sessions")
@admin_required
def sessions():
    conn = get_db()
    all_sessions = Session.recent_with_username(conn, limit=100)
    return render_template("admin/sessions.html", sessions=all_sessions)
