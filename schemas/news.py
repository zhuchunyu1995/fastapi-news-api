from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryResponse(BaseModel):
    id: int
    name: str
    sort_order: int

    model_config = ConfigDict(from_attributes=True)


class NewsItemResponse(BaseModel):
    """单条新闻输出模型"""

    id: int
    publish_time: datetime
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    content: str
    image: str | None = None
    author: str | None = None
    category_id: int
    views: int

    model_config = ConfigDict(from_attributes=True)


class NewsListData(BaseModel):
    """新闻列表数据模型（嵌套在 data 里）"""

    list: list[NewsItemResponse]  # 新闻列表
    total: int  # 总条数
    hasMore: bool  # 是否还有更多


class NewsDetailResponse(BaseModel):
    """新闻详情输出模型"""

    id: int
    title: str
    content: str
    image: str | None = None
    author: str | None = None
    publish_time: datetime = Field(alias="publishTime")  # 前端用驼峰
    category_id: int = Field(alias="categoryId")  # 前端用驼峰
    views: int = 0
    related_news: list[NewsItemResponse] = Field(default=[], alias="relatedNews")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
