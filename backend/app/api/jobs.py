from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from app.services.jd_parser import parse_jd

router = APIRouter(tags=["jobs"])

class JDInput(BaseModel):
    id: str
    text: str

class JobsRequest(BaseModel):
    jobs: list[JDInput]

@router.post("/parse")
def parse_jobs(req: JobsRequest):
    results = []

    for job in req.jobs:
        parsed = parse_jd(job.text)

        results.append({
            "id": job.id,
            "title": "Not specified",  # TODO: Add title extraction to jd_parser
            "company": "Not specified",  # TODO: Add company extraction to jd_parser
            "required_skills": parsed.get("required_skills", []),
            "preferred_skills": parsed.get("preferred_skills", []),
            "min_yoe": parsed.get("min_yoe"),
            "keywords": parsed.get("keywords", []),
            "education": parsed.get("education", []),
            "qualifications": parsed.get("qualifications", []),
            "raw_text": job.text
        })

    return {"jobs": results}