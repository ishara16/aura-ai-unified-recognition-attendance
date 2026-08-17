from src.database.db import create_subject, get_teacher_subjects


def create_teacher_subject(
    subject_code: str,
    name: str,
    section: str,
    teacher_id: int
):
    return create_subject(
        subject_code,
        name,
        section,
        teacher_id
    )


def get_subjects_for_teacher(teacher_id: int):
    return get_teacher_subjects(teacher_id)