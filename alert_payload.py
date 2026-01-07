def build_alert_payload(change, impact):
    return {
        "article": "GDPR Article 32",
        "change_summary": change["summary"],
        "change_type": change["change_type"],
        "risk_level": impact.risk_level,
        "recommended_action": impact.recommended_action,
        "reasoning": impact.reasoning,
        "confidence": impact.confidence,
        "source": "https://gdpr-info.eu/art-32-gdpr/"
    }
