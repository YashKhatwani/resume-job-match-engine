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
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    min_yoe: float | None = None
    keywords: List[str] = []
    education: List[str] = []
    qualifications: List[str] = []


class MatchRequest(BaseModel):
    resume_id: str
    skills: List[str]
    total_yoe: float
    roles: List[str] = []
    education: List[str] = []
    qualifications: List[str] = []
    job_descriptions: List[JDData]


@router.post("")
def match_jobs(req: MatchRequest):
    results = []

    for jd in req.job_descriptions:
        # Create resume dict from request
        resume = {
            "skills": req.skills,
            "total_yoe": req.total_yoe,
            "education": req.education,
            "qualifications": req.qualifications,
        }

        # Create JD dict with parsed data
        jd_dict = {
            "job_id": jd.jd_id,
            "title": jd.title,
            "company": jd.company or "Unknown",
            "text": jd.text,
            "required_skills": jd.required_skills,
            "preferred_skills": jd.preferred_skills,
            "min_yoe": jd.min_yoe,
            "keywords": jd.keywords,
            "education": jd.education,
            "qualifications": jd.qualifications,
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

