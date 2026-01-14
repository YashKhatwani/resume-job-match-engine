from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.matcher import match_resume_to_jd

router = APIRouter()


class JDData(BaseModel):
    jd_id: str
    title: str
    company: str | None = None
    text: str


class MatchRequest(BaseModel):
    resume_id: str
    skills: List[str]
    total_yoe: float
    roles: List[str] = []
    job_descriptions: List[JDData]


@router.post("")
def match_jobs(req: MatchRequest):
    results = []

    for jd in req.job_descriptions:
        # Create resume dict from request
        resume = {
            "skills": req.skills,
            "total_yoe": req.total_yoe,
        }

        # Create JD dict with parsed text
        jd_dict = {
            "job_id": jd.jd_id,
            "title": jd.title,
            "company": jd.company or "Unknown",
            "text": jd.text,
            "required_skills": [],  # Will be extracted by matcher if needed
            "preferred_skills": [],
            "min_yoe": None,
            "keywords": [],
        }

        match_result = match_resume_to_jd(
            resume=resume,
            jd=jd_dict
        )

        results.append({
            "job_id": jd.jd_id,
            "title": jd.title,
            "company": jd.company or "Unknown",
            **match_result
        })

    # Sort by best overall match
    results.sort(key=lambda x: x["overall_match"], reverse=True)

    return {"results": results}

