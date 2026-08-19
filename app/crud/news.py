from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import Category, News
from app.schemas.news import CategoryResponse, NewsDetailResponse, NewsItemResponse


# 获取新闻分类列表
async def get_category(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    data = [CategoryResponse.model_validate(tag) for tag in result.scalars().all()]
    return data


# 获取新闻列表
async def get_news_list(db: AsyncSession, category_id, skip: int = 0, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    data = [NewsItemResponse.model_validate(news) for news in result.scalars().all()]
    return data


# 获取新闻分类下的新闻数量
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


# 获取新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    data = NewsDetailResponse.model_validate(result.scalar_one_or_none())
    return data


# 获取相关新闻
async def get_related_news(
    db: AsyncSession, news_id: int, category_id: int, limit: int = 5
):
    stmt = (
        select(News)
        .where(News.id != news_id, News.category_id == category_id)
        .order_by(News.category_id.desc(), News.publish_time.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    data = [NewsItemResponse.model_validate(news) for news in result.scalars().all()]
    return data


# 增加新闻点击量
async def increment_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    affected = await db.execute(stmt)
    rowcount = getattr(affected, "rowcount", 0)
    return rowcount > 0
