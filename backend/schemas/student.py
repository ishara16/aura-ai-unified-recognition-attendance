from pydantic import BaseModel


class StudentResponse(BaseModel):
    student_id: int
    name: str