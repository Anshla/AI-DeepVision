import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

import streamlit as st

log = logging.getLogger("email_alert")
logging.basicConfig(level=logging.INFO)


# ---------------- SECRET HELPER ----------------
def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)


def _get_config():
    smtp_server = get_secret("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(get_secret("SMTP_PORT", 587))

    sender = get_secret("EMAIL_SENDER")
    password = get_secret("EMAIL_PASSWORD")

    receivers_raw = get_secret("EMAIL_RECEIVERS", "")
    receivers = [r.strip() for r in receivers_raw.split(",") if r.strip()]

    return smtp_server, smtp_port, sender, password, receivers


# ---------------- MAIN FUNCTIONS ----------------
def send_email_alert(count: int, subject: str = None, message: str = None) -> bool:
    smtp_server, smtp_port, sender, password, receivers = _get_config()

    if not (sender and password and receivers):
        log.error("Email not sent: email secrets not configured")
        return False

    if subject is None:
        subject = "🚨 Crowd Alert Notification"

    if message is None:
        message = (
            f"⚠ Crowd Alert!\n\n"
            f"Detected crowd count: {count}\n\n"
            f"AI-DeepVision System"
        )

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        log.info("Alert email sent to: %s", receivers)
        return True

    except Exception as exc:
        log.exception("Failed to send alert email: %s", exc)
        return False


def send_test_email() -> bool:
    return send_email_alert(
        count=0,
        subject="AI-DeepVision Test Email",
        message=(
            "This is a test email from AI-DeepVision.\n\n"
            "If you received this, the SMTP configuration is working correctly."
        ),
    )


def is_email_configured() -> bool:
    _, _, sender, password, receivers = _get_config()
    return bool(sender and password and receivers)


def get_email_receivers() -> List[str]:
    _, _, _, _, receivers = _get_config()
    return receivers
