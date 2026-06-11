import json
import os
import logging
from openai import OpenAI


logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_category(category: str) -> str:
    category = category.lower().strip().replace(" ", "_")

    if any(word in category for word in ["vehicle", "car", "auto"]):
        return "vehicle"
    elif any(word in category for word in ["water", "flood", "flooding", "leak"]):
        return "water_damage"
    elif any(word in category for word in ["fire", "burn", "smoke"]):
        return "fire_damage"
    else:
        return "unknown"

def analyze_claim_with_ai(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an insurance claim classifier. Always respond ONLY in valid JSON format with exactly these keys: category and reason. Do not add markdown, explanations, or extra text."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        content = response.choices[0].message.content
        logger.info(f"AI raw response: {content}")

        try:
            parsed = json.loads(content)
        except Exception as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            return {
                "category": "unknown",
                "reason": "AI response could not be parsed"
            }

        if not isinstance(parsed, dict):
            return {
                "category": "unknown",
                "reason": "Invalid AI response format"
            }

        parsed["category"] = normalize_category(parsed.get("category", ""))

        if "reason" not in parsed or not isinstance(parsed["reason"], str):
            parsed["reason"] = "No valid reason provided"

        return parsed

    except Exception as e:
        logger.error(f"AI service failed: {str(e)}")
        return {
            "category": "unknown",
            "reason": "AI service failed"
        }