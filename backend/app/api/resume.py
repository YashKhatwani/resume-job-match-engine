from fastapi import APIRouter, UploadFile, File
import uuid
from app.services.resume_parser import parse_resume as parse_resume_service

router = APIRouter()

@router.post("/parse")
def parse_resume(file: UploadFile = File(...)):
    """
    Parse a resume PDF file and extract:
    - Skills
    - Years of experience
    - Roles
    """
    resume_id = str(uuid.uuid4())

    try:
        # Log file info
        print(f"\n========== RESUME PARSE DEBUG ==========")
        print(f"File received: {file.filename}")
        print(f"Content-Type: {file.content_type}")
        print(f"Resume ID: {resume_id}")

        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            print(f"❌ Invalid file type: {file.filename}")
            return {"error": "Only PDF files are supported"}, 400

        print(f"✓ File type validation passed")

        # Parse the resume
        parsed_data = parse_resume_service(file.file)

        print(f"\n--- COMPLETE RESUME CONTENT ---")
        raw_text = parsed_data.get('raw_text', '')
        if raw_text:
            print(f"📄 Raw Text ({len(raw_text)} characters):")
            print("-" * 60)
            print(raw_text[:len(raw_text)])  # Print first 1000 characters
            
        
        print(f"\n--- Extracted Data ---")
        print(f"Skills ({len(parsed_data.get('skills', []))}):")
        print(f"  {parsed_data.get('skills', [])}")
        print(f"Total YOE: {parsed_data.get('total_yoe', 0)}")
        print(f"Roles ({len(parsed_data.get('roles', []))}):")
        print(f"  {parsed_data.get('roles', [])}")
        print(f"Education ({len(parsed_data.get('education', []))}):")
        print(f"  {parsed_data.get('education', [])}")
        print(f"Qualifications ({len(parsed_data.get('qualifications', []))}):")
        print(f"  {parsed_data.get('qualifications', [])}")
        print(f"========== END DEBUG ==========\n")

        return {
            "resume_id": resume_id,
            "skills": parsed_data.get("skills", []),
            "total_yoe": parsed_data.get("total_yoe", 0),
            "roles": parsed_data.get("roles", []),
            "education": parsed_data.get("education", []),
            "qualifications": parsed_data.get("qualifications", [])
        }
    except Exception as e:
        print(f"❌ Error parsing resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to parse resume: {str(e)}"}, 500