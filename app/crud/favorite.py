from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteResponse


# 获取收藏状态
async def get_favorite_status(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    is_favorite = await db.execute(stmt)
    return is_favorite.scalar_one_or_none() is not None


# 收藏文章
async def favorite_news(
    db: AsyncSession, user_id: int, news_id: int
) -> FavoriteResponse:
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.flush()
    await db.refresh(favorite)
    return FavoriteResponse.model_validate(favorite)


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    rowcount = getattr(result, "rowcount", 0)
    return rowcount > 0
