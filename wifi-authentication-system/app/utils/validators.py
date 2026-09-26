"""Input validation and lightweight request-parsing helpers."""

import re

USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_.-]{3,30}")
EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def valid_username(username: str) -> bool:
    return bool(re.fullmatch(USERNAME_PATTERN, username))


def valid_email(email: str) -> bool:
    return bool(re.fullmatch(EMAIL_PATTERN, email))


def valid_password(password: str) -> bool:
    """Require 8+ characters with at least one uppercase, one lowercase
    and one digit."""
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password) is not None
        and re.search(r"[a-z]", password) is not None
        and re.search(r"\d", password) is not None
    )


def detect_device(user_agent: str) -> str:
    ua = (user_agent or "").lower()
    if "android" in ua:
        return "Android"
    if "iphone" in ua or "ipad" in ua or "ios" in ua:
        return "iOS"
    if "windows" in ua:
        return "Windows"
    if "macintosh" in ua or "mac os" in ua:
        return "macOS"
    if "linux" in ua:
        return "Linux"
    return "Unknown"
