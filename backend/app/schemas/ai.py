# app/schemas/ai.py
from pydantic import BaseModel
from typing import List

class AISuggestionRequest(BaseModel):
    missing_required: List[str]
    missing_preferred: List[str]
    experience_gap: float
    jd_keywords: List[str]
