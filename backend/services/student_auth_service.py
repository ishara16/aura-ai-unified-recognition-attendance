from backend.database.supabase import supabase


def get_student_by_id(student_id: int):
    response = (
        supabase
        .table("students")
        .select("student_id, name")
        .eq("student_id", student_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]