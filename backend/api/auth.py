from fastapi import APIRouter, HTTPException

from backend.schemas.auth import TeacherLoginRequest
from backend.services.auth_service import authenticate_teacher


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/teacher/login")
def teacher_login(request: TeacherLoginRequest):
    teacher = authenticate_teacher(
        request.username,
        request.password
    )

    if teacher is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    teacher.pop("password", None)

    return {
        "message": "Teacher login successful",
        "teacher": teacher
    }