from datetime import datetime, timedelta, timezone

from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from core.config import settings

# 创建加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 加密密码
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 生成 JWT
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 验证 JWT
def verify_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        return int(user_id) if user_id else None
    except JWTError:
        return None
