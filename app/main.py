import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import os

load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ClaimRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Claim Assistant is running"}

import json

@app.post("/analyze-claim")
def analyze_claim(request: ClaimRequest):
    logger.info(f"[NEW LOG] Incoming claim: {request.text}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Classify insurance claims into categories: vehicle, water_damage, or unknown. Respond ONLY in valid JSON with keys: category and reason."
                },
                {
                    "role": "user",
                    "content": request.text
                }
            ]
        )

        content = response.choices[0].message.content
        logger.info(f"AI raw response: {content}")

        parsed = json.loads(content)
        return parsed

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "error": "AI service failed",
            "details": str(e)
        }

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
    except:
        parsed = {"error": "Invalid JSON from AI", "raw": content}

    return parsed