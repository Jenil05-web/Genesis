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

from src.tools.gdelt_tool import fetch_news
from src.tools.dataset_tool import load_sample_messages


def check_incoming(source: str = "dataset", query: str = "flood disaster", limit: int = 5) -> list[dict]:
    """Pulls messages from the given source, classifies each one, returns results."""
    if source == "gdelt":
        messages = fetch_news(query, limit=limit)
    else:
        messages = load_sample_messages(limit)

    results = []
    for msg in messages:
        classification = check_alert(msg["text"])
        results.append({**msg, **classification})
    return results



def check_alert(text: str) -> dict:
    """Classifies one message as SOS or not, with disaster type and severity."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": TRIAGE_PROMPT.replace("{text}", text)}],
    )
    return json.loads(response.choices[0].message.content)