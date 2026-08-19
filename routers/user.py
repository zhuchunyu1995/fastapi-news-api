from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.deps import get_current_user
from core.dependencies import get_db
from core.response import success_response
from core.security import create_access_token
from crud.user import create_user, login_endpoint, user_exists
from schemas.user import UserAuthResponse, UserInfoResponse, UserRequest

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_info: UserRequest,
):
    # 检查用户名是否存在
    exists = await user_exists(db, user_info.username)
    if exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    # 注册用户
    user = await create_user(db, user_info)

    # token 生成
    token = create_access_token(user.id)

    data = UserAuthResponse.model_validate({"token": token, "user_info": user})
    return success_response(data=data, message="注册成功")


@router.post("/login")
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_info: UserRequest,
):
    user = await login_endpoint(db, user_info)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    token = create_access_token(user.id)
    data = UserAuthResponse.model_validate({"token": token, "user_info": user})
    return success_response(data=data, message="登录成功")


@router.get("/info")
async def get_user_info(
    user: Annotated[UserInfoResponse, Depends(get_current_user)],
):
    return success_response(data=user, message="获取用户信息成功")
