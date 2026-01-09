from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.matcher import match_resume_to_jd

router = APIRouter()


class ResumeInput(BaseModel):
    skills: List[str]
    total_yoe: float


class JDInput(BaseModel):
    job_id: str
    title: str
    company: str | None = None
    required_skills: List[str]
    preferred_skills: List[str]
    min_yoe: float | None
    keywords: List[str]


class MatchRequest(BaseModel):
    resume: ResumeInput
    jobs: List[JDInput]


@router.post("")
def match_jobs(req: MatchRequest):
    results = []

    for job in req.jobs:
        match_result = match_resume_to_jd(
            resume=req.resume.dict(),
            jd=job.dict()
        )

        results.append({
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            **match_result
        })

    # Sort by best overall match
    results.sort(key=lambda x: x["overall_match"], reverse=True)

    return {"results": results}

