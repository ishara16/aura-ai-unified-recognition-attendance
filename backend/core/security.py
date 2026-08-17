from datetime import datetime, timedelta, timezone

from jose import jwt

from backend.config import settings

from fastapi import HTTPException
from jose import JWTError, jwt

def create_access_token(teacher_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(teacher_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        teacher_id = payload.get("sub")

        if teacher_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return int(teacher_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )