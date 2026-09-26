"""Public-facing authentication routes: welcome/captive page, registration,
login (with brute-force protection) and logout."""

from datetime import datetime

import sqlite3
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.extensions import get_db
from app.models.login_attempt import LoginAttempt
from app.models.session import Session
from app.models.user import User
from app.utils.validators import detect_device, valid_email, valid_password, valid_username

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("portal.portal"))
    return render_template("portal/welcome.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not valid_username(username):
            flash(
                "Username must be 3–30 characters and use letters, numbers, dot, "
                "underscore or hyphen.",
                "danger",
            )
            return render_template("auth/register.html")
        if not valid_email(email):
            flash("Enter a valid email address.", "danger")
            return render_template("auth/register.html")
        if not valid_password(password):
            flash("Password must be 8+ characters with uppercase, lowercase and a number.", "danger")
            return render_template("auth/register.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        conn = get_db()
        try:
            User.create(conn, username, email, password)
            flash("Account created securely. Authenticate to join the WiFi portal.", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "danger")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip = request.remote_addr or "unknown"

        conn = get_db()
        user = User.get_by_username(conn, username)
        failed_count = LoginAttempt.recent_failed_count(
            conn, username, current_app.config["LOCKOUT_WINDOW_MINUTES"]
        )

        if failed_count >= current_app.config["MAX_FAILED_ATTEMPTS"]:
            LoginAttempt.record(conn, username, ip, "BLOCKED")
            flash("Security lock active: too many failed attempts. Try again later.", "danger")
            return render_template("auth/login.html", blocked=True)

        if not user or user["status"] != "active" or not check_password_hash(user["password_hash"], password):
            LoginAttempt.record(conn, username, ip, "FAILED")
            flash("Invalid credentials. Authentication attempt recorded.", "danger")
            return render_template("auth/login.html")

        now = datetime.now().isoformat(timespec="seconds")
        device = detect_device(request.headers.get("User-Agent"))
        LoginAttempt.record(conn, username, ip, "SUCCESS")
        User.update_last_login(conn, user["id"], now)
        Session.create(conn, user["id"], ip, device)
        conn.commit()

        session.clear()
        session.permanent = True
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["device_type"] = device
        return redirect(url_for("portal.portal"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    user_id = session.get("user_id")
    if user_id is not None:
        conn = get_db()
        Session.close_active_for_user(conn, user_id)
    session.clear()
    flash("Secure session terminated.", "success")
    return redirect(url_for("auth.index"))
