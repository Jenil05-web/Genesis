import json
from openai import OpenAI

from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

TRIAGE_PROMPT = """Classify this message for disaster response. Return ONLY JSON matching this schema:

{
  "is_actionable_sos": boolean,
  "disaster_type": "flood" | "fire" | "earthquake" | "storm" | "other" | "none",
  "severity": "low" | "medium" | "high" | "critical",
  "location_hint": string or null,
  "reason": "one short sentence"
}

Message: "{text}"
"""


def check_alert(text: str) -> dict:
    """Classifies one message as SOS or not, with disaster type and severity."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": TRIAGE_PROMPT.replace("{text}", text)}],
    )
    return json.loads(response.choices[0].message.content)