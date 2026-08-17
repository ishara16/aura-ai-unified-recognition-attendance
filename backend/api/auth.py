from fastapi import APIRouter, HTTPException , Depends

from backend.schemas.auth import TeacherLoginRequest
from backend.services.auth_service import authenticate_teacher
from backend.core.security import create_access_token

from backend.core.dependencies import get_current_teacher
from backend.database.supabase import supabase

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

    access_token = create_access_token(
        teacher["teacher_id"]
    )

    return {
        "message": "Teacher login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "teacher": teacher
    }

@router.get("/me")
def get_current_teacher_info(
    teacher_id: int = Depends(get_current_teacher)
):
    response = (
        supabase
        .table("teachers")
        .select("teacher_id, username, name")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return response.data[0]