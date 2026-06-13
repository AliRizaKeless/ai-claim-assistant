from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.session import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.database import create_tables

from dotenv import load_dotenv
import os

from app.schemas.claim_schema import ClaimRequest

from app.services.claim_service import analyze_claim_with_ai, save_claim

load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from fastapi import FastAPI, Depends

app = FastAPI(
    title="AI Claim Assistant",
    description="API for classifying insurance claims using AI",
    version="1.0.0"
)

create_tables()

@app.get("/")
def read_root():
    return {"message": "AI Claim Assistant is running"}

import json

@app.post(
    "/analyze-claim",
    summary="Analyze insurance claim text",
    description="Takes a claim description and returns a structured category and reason using AI"
)
def analyze_claim(request: ClaimRequest, db: Session = Depends(get_db)):
    logger.info(f"[NEW LOG] Incoming claim: {request.text}")

    result = analyze_claim_with_ai(request.text)

    claim = save_claim(
        db=db,
        claim_text=request.text,
        category=result["category"],
        reason=result["reason"]
    )

    return {
        "id": claim.id,
        "category": claim.category,
        "reason": claim.reason
    }