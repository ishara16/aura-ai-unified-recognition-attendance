from fastapi import APIRouter, Depends, HTTPException

from backend.core.dependencies import get_current_teacher
from backend.schemas.student import StudentResponse
from backend.services.student_service import (
    get_all_students,
    get_student_by_id,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)


@router.get(
    "",
    response_model=list[StudentResponse]
)
def get_students(
    current_teacher: dict = Depends(get_current_teacher)
):
    return get_all_students()


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    current_teacher: dict = Depends(get_current_teacher)
):
    student = get_student_by_id(student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student