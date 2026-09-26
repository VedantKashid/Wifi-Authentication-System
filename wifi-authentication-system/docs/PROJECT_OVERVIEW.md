# Project Overview — WiFi Authentication System

## 1. Title

**WiFi Authentication System** — A Secure Captive-Portal Authentication
Platform for Managed WiFi Networks

## 2. Problem statement

Open or loosely-managed WiFi networks (in campuses, offices, cafés, and
labs) make it hard to know *who* is on the network, *when* they connected,
and *whether* repeated failed logins indicate an attack in progress.
Most small deployments either skip authentication entirely or rely on a
single shared password, which gives administrators no visibility and no
way to revoke access per user.

## 3. Objective

To design and build a web-based captive-portal authentication layer that:

- Verifies user identity before granting network access
- Detects and throttles brute-force login attempts automatically
- Gives administrators a real-time dashboard of users, sessions, and
  authentication activity
- Keeps a full, queryable audit trail of logins and admin actions

## 4. Technology stack

| Layer            | Technology                                |
|-------------------|-------------------------------------------|
| Backend framework | Python, Flask (application factory + blueprints) |
| Database          | SQLite                                    |
| Auth & hashing    | Werkzeug security (PBKDF2 password hashing) |
| Frontend          | Jinja2 templates, HTML5, CSS3, vanilla JS |
| Deployment target | Gunicorn (WSGI), behind a network gateway |

## 5. System architecture

```
WiFi client → Access point / gateway → Captive portal redirect
           → Flask application (this project) → SQLite
```

The Flask application owns **authentication and monitoring only**.
Actual network-level enforcement (allowing/blocking client traffic) is the
responsibility of an authorized gateway or access point (e.g. hostapd +
dnsmasq + firewall rules) — see `network/README.md` for the full
integration architecture. This separation of concerns keeps the web
application portable and testable independent of any specific network
hardware.

Within the application itself:

- **`app/routes/`** — three blueprints (`auth`, `portal`, `admin`) handle
  HTTP requests and delegate all data access to the model layer.
- **`app/models/`** — one module per database table (`User`, `Session`,
  `LoginAttempt`, `AdminLog`), so every query is written once, in one
  place, and easy to review for correctness and security.
- **`app/utils/`** — shared cross-cutting concerns: access-control
  decorators (`login_required`, `admin_required`) and input validation.
- **`app/extensions.py`** — owns the SQLite connection lifecycle and
  schema initialization, including a backward-compatible migration path
  for databases created by earlier versions of the schema.

## 6. Key features delivered

- Registration with server-side username/email/password policy validation
- Secure login with PBKDF2 password hashing (no plaintext storage)
- Automatic temporary lockout after repeated failed attempts within a
  rolling time window, with every attempt logged
- Role-based access control separating regular users from administrators
- Session tracking: IP address, detected device type, login/logout time
- Admin dashboard with live counts, a 7-day login activity trend, a
  device-type breakdown, and a feed of recent authentication events
- User management screen to enable/disable accounts, with a safeguard
  against an admin disabling their own account
- Dedicated authentication log and admin action audit log screens
- Active session monitor across all connected users

## 7. Possible future extensions

- Replace polling-based session status with WebSocket-driven live updates
- Integrate directly with `hostapd`/RADIUS for real network-level
  enforcement instead of a standalone captive-portal simulation
- Add email or TOTP-based multi-factor authentication
- Externalize configuration further with a proper secrets manager for
  production deployments

---

## 8. Introduction speech (for viva / project presentation)

*Suggested delivery time: ~90 seconds. Adjust names/timelines to fit your
actual submission.*

> Good [morning/afternoon] everyone. My project is called the **WiFi
> Authentication System** — a secure, web-based captive-portal platform
> that controls and monitors who connects to a WiFi network.
>
> The motivation behind this project is simple: most small WiFi
> deployments either have no real authentication at all, or rely on a
> single shared password that gives administrators zero visibility into
> who is actually using the network. I wanted to build something that
> solves both problems — proper per-user authentication, and a real-time
> view into network activity — the way a security team would expect in a
> managed environment.
>
> The system is built with **Python and Flask** on the backend, using
> **SQLite** for data storage, and a custom dark, cybersecurity-themed
> interface on the frontend. Every user goes through a secure registration
> and login flow, where passwords are never stored in plaintext — they're
> hashed using industry-standard PBKDF2 hashing. The login system also
> includes **brute-force protection**: after a set number of failed
> attempts within a short window, that account is automatically locked out
> temporarily, and every attempt — successful or not — is logged for
> auditing.
>
> On top of the authentication layer, I built a complete **admin
> dashboard** that gives administrators live statistics: total and active
> users, a seven-day login activity trend, a breakdown of connected
> devices by type, and a feed of recent authentication events. Admins can
> also enable or disable user accounts, monitor active sessions in
> real time, and review a full audit log of both login attempts and
> administrative actions.
>
> Architecturally, the project is organized the way a production Flask
> application would be — using an **application factory pattern** with
> **blueprints** separating authentication, the user portal, and the admin
> area, and a dedicated **model layer** that isolates all database queries
> from the request-handling code. This makes the codebase easy to test,
> extend, and audit — which matters a lot for anything touching network
> security.
>
> It's important to be clear about scope: this application handles the
> **authentication and monitoring layer** of a captive portal. Actual
> network-level enforcement — physically allowing or blocking a device's
> traffic — is the job of an authorized gateway or access point, and I've
> documented that integration architecture separately so the project is
> honest about what it does and doesn't claim to do.
>
> To summarize: this project demonstrates a full, security-conscious
> authentication system — from password policy and hashing, to
> brute-force defense, to real-time administrative monitoring — built on
> a clean, maintainable architecture. Thank you, and I'm happy to walk
> through a live demo or answer any questions.

### Shorter 30-second version (for time-constrained slots)

> My project is a **WiFi Authentication System** — a secure captive-portal
> platform built with Flask and SQLite that authenticates users before
> granting network access. It includes secure password hashing,
> brute-force lockout protection, role-based access control, and a
> real-time admin dashboard showing active sessions, login trends, and a
> full audit log. The goal was to bring proper, auditable authentication
> to WiFi deployments that would otherwise rely on a single shared
> password with no visibility for administrators.
