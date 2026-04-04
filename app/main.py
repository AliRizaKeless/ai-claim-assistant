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

    try:
        parsed = json.loads(content)
    except:
        parsed = {"error": "Invalid JSON from AI", "raw": content}

    return parsed