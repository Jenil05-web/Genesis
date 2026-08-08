import json
from openai import OpenAI

from src.config import settings
from src.rag.search_knowledge_base import search_protocols

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PLAN_PROMPT= """You are a disaster response planner. Using ONLY the protocol context below,
draft a 3-phase response plan for this situation. If the context doesn't cover
something, say so instead of inventing it.

Situation: {situation}
Alert info: {alert_info}
Image findings: {image_findings}

Protocol context:
{context}

Return ONLY JSON matching this schema:
{{
  "immediate": "string",
  "short_term": "string",
  "recovery": "string",
  "grounded": true or false
}}"""

def make_response_plan(situation:str, disaster_type:str, alert_info:str = "", image_findings:str = "")->dict:
    """Retrieves relevant protocols, then asks the LLM to draft a grounded 3-phase plan."""

    context_chunks = search_protocols(situation, disaster_type=disaster_type)
    context_text = "\n\n".join(context_chunks)

    prompt = PLAN_PROMPT.format(
        situation = situation,
        alert_info = alert_info  or "none provided",
        image_findings=image_findings or "none provided",
        context=context_text,
    )

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        response_format = {"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],

    )

    plan = json.loads(response.choices[0].message.content)
    plan["used_context"] = context_chunks
    return plan



