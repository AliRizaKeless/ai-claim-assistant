from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ClaimRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Claim Assistant is running"}

@app.post("/analyze-claim")
def analyze_claim(request: ClaimRequest):
    text = request.text.lower()

    if "car" in text or "bil" in text:
        category = "vehicle"
    elif "water" in text or "su" in text:
        category = "water_damage"
    else:
        category = "unknown"

    return {
        "category": category,
        "message": "This is a basic analysis"
    }