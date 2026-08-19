from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import DbSession
from app.core.deps import get_current_user
from app.core.response import success_response
from app.core.security import create_access_token
from app.crud import user as user_crud
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserAuthResponse,
    UserInfoResponse,
    UserRequest,
    UserUpdateRequest,
)

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(
    db: DbSession,
    user_info: UserRequest,
):
    # 检查用户名是否存在
    exists = await user_crud.user_exists(db, user_info.username)
    if exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    # 注册用户
    user = await user_crud.create_user(db, user_info)

    # token 生成
    token = create_access_token(user.id)

    data = UserAuthResponse.model_validate({"token": token, "user_info": user})
    return success_response(data=data, message="注册成功")


@router.post("/login")
async def login(
    db: DbSession,
    user_info: UserRequest,
):
    user = await user_crud.login_endpoint(db, user_info)
    if user is None or user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = create_access_token(user.id)
    data = UserAuthResponse.model_validate({"token": token, "user_info": user})
    return success_response(data=data, message="登录成功")


@router.get("/info")
async def get_user_info(
    user: Annotated[User, Depends(get_current_user)],
):
    return success_response(
        data=UserInfoResponse.model_validate(user), message="获取用户信息成功"
    )


@router.put("/update")
async def update_user_info(
    update_data: UserUpdateRequest,
    user: Annotated[User, Depends(get_current_user)],
):
    data = await user_crud.update_profile(user, update_data)
    return success_response(data=data, message="更新用户信息成功")


@router.put("/password")
async def change_password(
    request_data: ChangePasswordRequest,
    user: Annotated[User, Depends(get_current_user)],
):
    is_old_password_valid = await user_crud.reset_password(user, request_data)
    if is_old_password_valid is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误",
        )
    return success_response(message="密码修改成功")
