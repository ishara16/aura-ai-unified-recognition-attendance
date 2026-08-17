from fastapi import FastAPI

from backend.api.auth import router as auth_router

app = FastAPI(
    title="AURA API",
    description="AI Unified Recognition Attendance API",
    version="1.0.0"
)

app.include_router(auth_router)

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