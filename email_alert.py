import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "rgshettymys@gmail.com"
SENDER_PASSWORD = "Model@123"
RECIPIENT_EMAIL = "deakshanth.shetty@gmail.com"


def send_email_alert(payload):
    subject = f"[{payload['risk_level']}] GDPR Update – Action Required"

    body = f"""
GDPR Regulatory Update Detected

Article: {payload['article']}
Risk Level: {payload['risk_level']}

What changed:
{payload['change_summary']}

Why this applies:
""" + "\n".join(f"- {r}" for r in payload["reasoning"]) + f"""

Recommended action:
{payload['recommended_action']}

Source:
{payload['source']}

Confidence:
{payload['confidence'] * 100:.0f}%
"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
