from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import resume, jobs, match ,ai_suggestions as ai

app = FastAPI(title="Resume Job Match Engine")

# ✅ CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(resume.router, prefix="/resume")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(match.router, prefix="/match")
app.include_router(ai.router, prefix="/ai")

@app.get("/health")
def health():
    return {"status": "ok"}
