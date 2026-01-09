from fastapi import APIRouter, UploadFile, File
import uuid

router = APIRouter()

@router.post("/parse")
def parse_resume(file: UploadFile = File(...)):
    resume_id = str(uuid.uuid4())

    # TODO: extract text + skills + yoe
    return {
        "resume_id": resume_id,
        "skills": ["react", "spring boot"],
        "total_yoe": 2.5,
        "roles": ["software engineer"]
    }