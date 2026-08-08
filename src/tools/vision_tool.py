import base64
import json
from openai import OpenAI

from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

ANALYZE_PROMPT = """Analyze this image for disaster response purposes. Return ONLY JSON matching this schema:

{
  "flooded_zones": boolean,
  "blocked_roads": boolean,
  "collapsed_structures": boolean,
  "severity_estimate": "low" | "medium" | "high" | "critical",
  "notes": "one sentence summary"
}"""

def encode_image(image_path:str)-> str:
    """Reads a local image file and turns it into base64 text — OpenAI needs images this way unless it's already a public URL."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path_or_url:str)->dict:
    """Sends one image to GPT-4o-mini and returns structured disaster findings as dict"""    
    if image_path_or_url.startswith("http"):
        image_content = {"type": "image_url", "image_url": {"url": image_path_or_url}}
    else:
        encoded = encode_image(image_path_or_url)
        image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": ANALYZE_PROMPT},
                image_content
            ],
        }],
    )
    return json.loads(response.choices[0].message.content)



