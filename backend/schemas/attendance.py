from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateAttendanceRequest(BaseModel):
    subject_id: int
    student_id: int
    is_present: bool = True


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    subject_id: int
    student_id: int
    is_present: bool