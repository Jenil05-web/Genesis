import json
from openai import OpenAI

from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

CHECK_PROMPT = """You are auditing a disaster response plan for hallucination.
The plan may reference details from the SITUATION (given facts) or the CONTEXT (retrieved protocols).
Mark it as failed only if the plan states specific facts, numbers, or actions
that are NOT supported by either the situation or the context.

SITUATION:
{situation}

CONTEXT:
{context}

PLAN:
Immediate: {immediate}
Short-term: {short_term}
Recovery: {recovery}

Return ONLY JSON:
{{
  "passed": boolean,
  "issues": ["list of specific unsupported claims found, empty if none"]
}}"""


def check_plan(plan: dict, situation:str) -> dict:
    """Independently checks if a plan's claims are actually supported by its own context."""
    context_text = "\n\n".join(plan.get("used_context", []))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": CHECK_PROMPT.format(
                situation = situation,
                context=context_text,
                immediate=plan.get("immediate", ""),
                short_term=plan.get("short_term", ""),
                recovery=plan.get("recovery", ""),
            ),
        }],
    )
    return json.loads(response.choices[0].message.content)