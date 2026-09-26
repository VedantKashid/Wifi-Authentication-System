# WiFi Authentication System

A cybersecurity-focused WiFi / captive-portal authentication platform built
with **Flask** and **SQLite**, structured as an installable application
package with a factory pattern, blueprints, and a dedicated data-access
layer.

> This application implements the **authentication and monitoring layer**
> of a captive-portal deployment. Real network enforcement (blocking or
> allowing traffic) must be performed by an authorized gateway/access point;
> see [`network/README.md`](network/README.md) for the recommended
> architecture. Use only on a WiFi network you own or are explicitly
> authorized to administer.

---

## Features

- Dark, cybersecurity-styled captive-portal UI with animated background
- Modern login and registration flows with client-side password visibility
- Server-side password policy enforcement (length, case, digit)
- Secure password hashing (Werkzeug / PBKDF2)
- Brute-force protection with automatic temporary lockout and attempt logging
- Role-based access control (`user` / `admin`)
- Session lifecycle tracking (IP, device type, login/logout time)
- Admin dashboard: live stats, 7-day login activity, device breakdown,
  recent authentication events
- User management (enable/disable accounts, self-protection against
  disabling your own admin account)
- Full authentication + administrator audit logs
- Active session monitor
- Backward-compatible database migration for older schema versions
- Responsive, mobile-friendly layout

## Project structure

```
wifi-authentication-system/
├── app/                        # Application package
│   ├── __init__.py             # create_app() factory
│   ├── config.py               # Environment-driven configuration
│   ├── extensions.py           # DB connection lifecycle, schema init, seeding
│   ├── models/                 # Data-access layer (one module per table)
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── login_attempt.py
│   │   └── admin_log.py
│   ├── routes/                 # Blueprints (HTTP layer only)
│   │   ├── auth.py             # /, /register, /login, /logout
│   │   ├── portal.py           # /portal
│   │   └── admin.py            # /admin/*
│   ├── utils/
│   │   ├── decorators.py       # login_required, admin_required
│   │   └── validators.py       # input validation, device detection
│   ├── templates/               # Jinja2 templates
│   └── static/                  # CSS / JS
├── database/
│   └── schema.sql              # Single source of truth for the schema
├── network/
│   └── README.md               # Captive-portal / gateway integration notes
├── docs/
│   └── PROJECT_OVERVIEW.md     # Presentation notes and intro speech
├── tests/
│   └── test_auth.py
├── run.py                      # Development entry point
├── run.bat                     # One-click Windows setup + run
├── requirements.txt
├── .env.example
└── .gitignore
```

This mirrors the standard Flask "application factory + blueprints" layout,
so the codebase is easy to extend (new blueprint = new feature area),
easy to test (the factory can be created with different configs), and
keeps SQL isolated in `app/models/` instead of scattered across routes.

## Getting started

### 1. Create a virtual environment and install dependencies

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or simply double-click / run `run.bat` on Windows to do the above and
launch the app in one step.

### 2. Configure environment variables (optional)

```bash
cp .env.example .env
```

Edit `.env` to set a real `SECRET_KEY` and, optionally, override the
default admin credentials, session timeout, or lockout thresholds. All
settings have sensible defaults for local development.

### 3. Run

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

The database (`database/database.db`) and the default administrator
account are created automatically on first run.

### Demo administrator account

| Field    | Value          |
|----------|----------------|
| Username | `admin`        |
| Password | `Admin@12345`  |

**Change this password (or set `DEFAULT_ADMIN_PASSWORD` in `.env`) before
any real deployment.**

## Running tests

```bash
pip install pytest
pytest
```

`tests/test_auth.py` currently documents the manual verification checklist
used during development; see the file for the steps and for guidance on
extending it into automated `pytest` + Flask test-client cases.

## Security notes

- Passwords are hashed with Werkzeug's `generate_password_hash` /
  `check_password_hash` (PBKDF2) — plaintext passwords are never stored.
- Failed login attempts are rate-limited per username within a rolling
  window, with attempts logged for auditing.
- Sessions expire automatically after a configurable idle period.
- The WiFi signal indicators in the UI are presentation elements for the
  captive-portal experience; they do not measure real radio signal
  strength from the host machine.
- Do not copy firewall or captive-portal rules from the internet without
  reviewing and adapting them for your own lab environment.
