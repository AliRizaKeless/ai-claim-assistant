import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import os

from app.schemas.claim_schema import ClaimRequest

from app.services.claim_service import normalize_category

load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from fastapi import FastAPI

app = FastAPI(
    title="AI Claim Assistant",
    description="API for classifying insurance claims using AI",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "AI Claim Assistant is running"}

import json

@app.post(
    "/analyze-claim",
    summary="Analyze insurance claim text",
    description="Takes a claim description and returns a structured category and reason using AI"
)
def analyze_claim(request: ClaimRequest):
    logger.info(f"[NEW LOG] Incoming claim: {request.text}")

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
                    "content": request.text
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

        if "category" not in parsed:
            parsed["category"] = "unknown"

        if "reason" not in parsed:
            parsed["reason"] = "No reason provided"

        if not isinstance(parsed["category"], str):
            parsed["category"] = "unknown"

        if not isinstance(parsed["reason"], str):
            parsed["reason"] = "Invalid reason format"
        return parsed

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

        return {
            "error": "Something went wrong. Please try again later."
    }
