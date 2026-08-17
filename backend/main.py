from fastapi import FastAPI

from backend.database.supabase import supabase

app = FastAPI(
    title="AURA API",
    description="AI Unified Recognition Attendance API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AURA API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }