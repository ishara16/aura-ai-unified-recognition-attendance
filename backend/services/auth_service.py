from src.database.db import teacher_login


def authenticate_teacher(username: str, password: str):
    return teacher_login(username, password)