from pydantic import BaseModel


class StudentLoginRequest(BaseModel):
    student_id: int


class StudentResponse(BaseModel):
    student_id: int
    name: str


class StudentLoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    student: StudentResponse