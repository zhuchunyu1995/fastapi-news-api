from fastapi import APIRouter, HTTPException, Query, status

from app.core.dependencies import DbSession
from app.core.response import success_response
from app.crud import news
from app.schemas.news import NewsDetailResponse, NewsListData

router = APIRouter(prefix="/api/news", tags=["news"])


# 获取新闻分类列表
@router.get("/categories")
async def get_categories(
    db: DbSession,
    skip: int = 0,
    limit: int = 100,
):
    result = await news.get_category(db, skip, limit)
    return success_response(data=result)


# 获取新闻列表
@router.get("/list")
async def get_news_list(
    db: DbSession,
    category_id: int = Query(..., description="新闻分类ID", alias="categoryId"),
    page: int = Query(..., description="页码", alias="page"),
    page_size: int = Query(
        default=10, ge=5, le=20, description="每页数量", alias="pageSize"
    ),
):
    skip = (page - 1) * page_size
    result = await news.get_news_list(db, category_id, skip=skip, limit=page_size)
    total: int = await news.get_news_count(db, category_id)
    has_more = (skip + len(result)) < total
    data = NewsListData.model_validate(
        {"list": result, "total": total, "hasMore": has_more}
    )
    return success_response(data=data)


# 获取新闻详情
@router.get("/detail")
async def get_news_detail(
    db: DbSession,
    id: int = Query(..., description="新闻ID"),
):
    result = await news.get_news_detail(db, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="新闻不存在或已被删除",
        )

    relatedNews = await news.get_related_news(db, id, result.category_id)

    affected = await news.increment_views(db, result.id)
    if not affected:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="新闻不存在或已被删除",
        )
    keys = [
        "id",
        "title",
        "content",
        "image",
        "author",
        "publish_time",
        "category_id",
        "views",
    ]
    data_obj = {k: getattr(result, k) for k in keys}
    data_obj["related_news"] = relatedNews

    data = NewsDetailResponse.model_validate(data_obj)
    return success_response(data=data)
