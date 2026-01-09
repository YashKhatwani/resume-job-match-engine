from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from app.services.jd_parser import parse_jd

router = APIRouter()

class JobInput(BaseModel):
    title: str
    company: str | None = None
    jd_text: str

class JobsRequest(BaseModel):
    jobs: list[JobInput]

@router.post("/parse")
def parse_jobs(req: JobsRequest):
    results = []

    for job in req.jobs:
        parsed = parse_jd(job.jd_text)

        results.append({
            "job_id": str(uuid.uuid4()),
            "title": job.title,
            "company": job.company,
            **parsed
        })

    return {"jobs": results}
