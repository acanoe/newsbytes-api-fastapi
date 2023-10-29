from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(user_id: int, expire_minutes: int = 60 * 24) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = {"exp": expire, "sub": user_id}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)
