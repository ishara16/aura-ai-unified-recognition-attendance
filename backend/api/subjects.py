from fastapi import APIRouter, Depends, HTTPException

from backend.core.dependencies import get_current_teacher
from backend.schemas.subject import CreateSubjectRequest, SubjectResponse
from backend.services.subject_service import (
    create_teacher_subject,
    get_subjects_for_teacher
)


router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"]
)


@router.post(
    "",
    response_model=SubjectResponse,
    status_code=201
)
def create_subject_endpoint(
    request: CreateSubjectRequest,
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    try:
        result = create_teacher_subject(
            request.subject_code,
            request.name,
            request.section,
            teacher_id
        )

        return result[0]

    except Exception as e:
        if "unique_teacher_subject" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Subject already exists for this teacher"
            )

        raise HTTPException(
            status_code=500,
            detail="Failed to create subject"
        )


@router.get("")
def get_subjects(
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    return get_subjects_for_teacher(teacher_id)