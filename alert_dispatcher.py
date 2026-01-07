from email_alert import send_email_alert
from slack_alert import send_slack_alert
from audit import log_event


def dispatch_alert(payload, impact):
    if not impact.applies:
        return

    if impact.risk_level == "LOW":
        return

    if impact.confidence < 0.6:
        log_event("ALERT_SKIPPED_LOW_CONFIDENCE", payload)
        return

    send_email_alert(payload)
    send_slack_alert(payload)

    log_event("ALERT_SENT", payload)
