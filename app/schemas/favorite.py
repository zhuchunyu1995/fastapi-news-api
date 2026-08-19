from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# 获取收藏状态请求模型
class GetFavoriteStatusRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# 获取收藏状态响应模型
class FavoriteStatusResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite", description="是否收藏")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# 收藏文章响应模型
class FavoriteResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId", description="用户ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    created_at: datetime = Field(..., alias="createTime", description="收藏时间")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
