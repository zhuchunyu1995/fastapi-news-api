from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """响应模型"""

    code: int = Field(description="状态码")
    message: str = Field(description="消息")
    data: T | None = Field(default=None, description="数据")


def success_response(
    data: T | None = None, message: str = "success", code=200
) -> Response[T]:
    return Response(
        code=code,
        message=message,
        data=data,
    )
