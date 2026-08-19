from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserInfoBase(BaseModel):
    """用户信息基类（用于请求/数据库）"""

    nickname: str | None = Field(None, max_length=20, description="昵称")
    avatar: str | None = Field(None, max_length=255, description="头像URL")
    gender: str | None = Field(None, max_length=10, description="性别")
    bio: str | None = Field(None, max_length=500, description="个人简介")
    phone: str | None = Field(None, max_length=11, description="手机号")

    model_config = ConfigDict(from_attributes=True)


class UserRequest(UserInfoBase):
    """注册请求（包含密码）"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserInfoResponse(BaseModel):
    """用户信息响应（不包含密码）"""

    id: int
    username: str
    nickname: str | None = None
    avatar: str | None = None
    gender: str | None = None
    bio: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserAuthResponse(BaseModel):
    """登录响应数据"""

    token: str = Field(description="用户访问令牌")
    user_info: UserInfoResponse = Field(..., description="用户信息", alias="userInfo")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class UserTokenResponse(BaseModel):
    """用户令牌响应数据"""

    user_id: int
    token: str
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
