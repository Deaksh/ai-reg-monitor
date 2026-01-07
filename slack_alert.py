import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

def send_slack_alert(payload):
    message = {
        "text": f"""
🚨 *GDPR Update Detected*

*Risk:* {payload['risk_level']}
*Article:* {payload['article']}

*Change:*
{payload['change_summary']}

*Recommended Action:*
{payload['recommended_action']}

*Confidence:* {payload['confidence'] * 100:.0f}%
<{payload['source']}|View source>
"""
    }

    requests.post(SLACK_WEBHOOK_URL, json=message, timeout=5)
