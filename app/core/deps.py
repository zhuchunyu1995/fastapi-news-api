from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import verify_token
from app.crud.user import get_user_by_id
from app.schemas.user import UserInfoResponse


# 获取当前登录用户
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    authorization: Annotated[
        str, Header(..., alias="Authorization", description="Authorization token")
    ],
) -> UserInfoResponse:

    # 1. 验证 Header 格式
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证格式错误，请使用: Bearer <token>",
        )

    # 2. 提取 token
    token = authorization.replace("Bearer ", "")

    # 3. 验证 JWT
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌无效或过期",
        )

    # 4. 查询用户
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    # 5. 返回用户信息
    return UserInfoResponse.model_validate(user)
