from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)


# 检查用户是否存在
async def user_exists(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user: UserRequest):
    user.password = hash_password(user.password)
    user_info = User(**user.model_dump())
    db.add(user_info)
    await db.flush()
    await db.refresh(user_info)
    return UserInfoResponse.model_validate(user_info)


# 用户登录
async def login_endpoint(db: AsyncSession, user_info: UserRequest):
    # 检查用户名是否存在
    user = await user_exists(db, user_info.username)
    if user is None:
        return None

    # ✅ 验证密码（明文 vs 数据库密文）
    if not verify_password(user_info.password, user.password):
        return False

    return UserInfoResponse.model_validate(user)


# 根据 ID 查询用户
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    if user:
        return user
    return None


# 更新用户信息
async def update_profile(user: User, update_data: UserUpdateRequest):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    return UserInfoResponse.model_validate(user)


# 更新用户密码
async def reset_password(user: User, request_data: ChangePasswordRequest):
    if not verify_password(request_data.old_password, user.password):
        return False
    user.password = hash_password(request_data.new_password)

    return True
