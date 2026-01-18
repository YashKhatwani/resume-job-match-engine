# app/api/ai.py
from fastapi import APIRouter
from app.schemas.ai import AISuggestionRequest
from app.services.groq_ai import get_ai_suggestions
from app.services.ai_prompt import build_groq_prompt

router = APIRouter(tags=["AI"])

@router.post("/suggestions")
def ai_suggestions(data: AISuggestionRequest):
    prompt = build_groq_prompt(data)
    suggestions = get_ai_suggestions(prompt)
    return {"suggestions": suggestions}
