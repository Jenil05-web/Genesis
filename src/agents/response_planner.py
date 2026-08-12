from openai import OpenAI

from src.config import settings
from src.rag.search_knowledge_base import search_protocols
from src.tools.maps_tool import geocode
from src.tools.weather_tool import get_weather
from src.utils.helpers import safe_parse_json, normalise_severity
import logging
logger = logging.getLogger("genesis")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PLAN_PROMPT = """You are a disaster response planner. Using ONLY the protocol context below,
draft a 3-phase response plan for this situation. If the context doesn't cover
something, say so instead of inventing it.

Situation: {situation}
Alert info: {alert_info}
Image findings: {image_findings}
Current weather: {weather_info}

Protocol context:
{context}

Return ONLY JSON matching this schema:
{{
  "immediate": "string",
  "short_term": "string",
  "recovery": "string",
  "grounded": true or false
}}"""

def make_response_plan(situation: str, disaster_type: str, alert_info: str = "",
                        image_findings: str = "", location_hint: str = None,
                        previous_issues: list = None) -> dict:
    """Retrieves relevant protocols + real weather, then drafts a grounded 3-phase plan."""
    context_chunks = search_protocols(situation, disaster_type=disaster_type)
    context_text = "\n\n".join(context_chunks)

    weather_info = "unavailable"
    if location_hint:
        geo = geocode(location_hint)
        if geo["found"]:
            weather = get_weather(geo["lat"], geo["lon"])
            weather_info = f"{weather['temperature_c']}°C, {weather['precipitation_mm']}mm precipitation, {weather['wind_speed_kmh']}km/h wind"

    feedback_note = ""
    if previous_issues:
        feedback_note = f"\n\nIMPORTANT: A previous version of this plan had these issues — fix them: {previous_issues}"

    prompt = PLAN_PROMPT.format(
        situation=situation,
        alert_info=alert_info or "none provided",
        image_findings=image_findings or "none provided",
        weather_info=weather_info,
        context=context_text,
    ) + feedback_note

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        response_format = {"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],

    )

    plan = safe_parse_json(response.choices[0].message.content, fallback={"immediate": "", "short_term": "", "recovery": "", "grounded": False})
    plan["used_context"] = context_chunks
    # Normalise any severity the planner echoes back so downstream consumers get a canonical value
    if "severity" in plan:
        plan["severity"] = normalise_severity(plan["severity"])
    logger.info("make_response_plan: grounded=%s context_chunks=%d", plan.get("grounded"), len(context_chunks))
    return plan



