from src.database.db import teacher_login
from backend.core.security import create_access_token


def authenticate_teacher(username: str, password: str):
    teacher = teacher_login(username, password)

    if not teacher:
        return None

    access_token = create_access_token(
        teacher["teacher_id"],
        "teacher"
    )

    return {
        "teacher": teacher,
        "access_token": access_token
    }