import json
import re
from pydantic import BaseModel
from llm import llm
from company_profile import COMPANY_PROFILE


class ImpactAssessment(BaseModel):
    applies: bool
    risk_level: str            # NONE | LOW | MEDIUM | HIGH
    recommended_action: str
    reasoning: list[str]
    confidence: float


PROMPT = """
You are an AI compliance assistant.
Do NOT provide legal advice.

Regulatory change:
{change}

Company profile:
{company}

Return ONLY valid JSON.
No markdown.

JSON format:
{{
  "applies": true,
  "risk_level": "NONE | LOW | MEDIUM | HIGH",
  "recommended_action": "...",
  "reasoning": ["..."],
  "confidence": 0.0
}}
"""


def _extract_json(text: str) -> str:
    """Extract first valid JSON object from LLM output."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in LLM output:\n{text}")
    return match.group(0)


def assess_impact(change: dict) -> ImpactAssessment:
    response = llm.invoke(
        PROMPT.format(
            change=json.dumps(change, indent=2),
            company=COMPANY_PROFILE
        )
    )

    clean_json = _extract_json(response.content)
    return ImpactAssessment.model_validate_json(clean_json)
