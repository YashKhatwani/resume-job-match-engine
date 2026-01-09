from fastapi import FastAPI
from app.api import resume, jobs, match

app = FastAPI(title="Resume Job Matcher")

app.include_router(resume.router, prefix="/resume")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(match.router, prefix="/match")

@app.get("/")
def read_root():    
    return {"message": "Welcome to the Resume Job Matcher API"}

@app.get("/health")
def health():
    return {"status": "ok"}
    
