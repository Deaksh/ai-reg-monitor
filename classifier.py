import json
from llm import llm
from schemas import ChangeClassification
from audit import log_event

PROMPT = """
You are a regulatory analyst.
Classify the regulatory change below.

Return ONLY valid JSON.

BEFORE:
{before}

AFTER:
{after}

Change types:
- NEW_OBLIGATION
- MODIFIED_OBLIGATION
- CLARIFICATION
- DEADLINE_CHANGE
- NO_IMPACT

Required JSON format:
{{
  "change_type": "...",
  "summary": "...",
  "confidence": 0.0
}}
"""


def classify_change(before: str, after: str) -> ChangeClassification:
    response = llm.invoke(PROMPT.format(before=before, after=after))

    raw = response.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        log_event("CLASSIFICATION_PARSE_ERROR", {"raw": raw})
        # Safe fallback
        return ChangeClassification(
            change_type="NO_IMPACT",
            summary="Unable to parse classification output",
            confidence=0.0
        )

    # 🔒 HARDEN AGAINST PARTIAL OUTPUTS
    change_type = data.get("change_type", "NO_IMPACT")

    summary = data.get(
        "summary",
        "No material regulatory impact detected"
        if change_type == "NO_IMPACT"
        else "Regulatory change detected"
    )

    confidence = data.get(
        "confidence",
        0.5 if change_type != "NO_IMPACT" else 0.9
    )

    return ChangeClassification(
        change_type=change_type,
        summary=summary,
        confidence=confidence
    )
