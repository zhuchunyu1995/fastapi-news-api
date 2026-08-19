from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import DbSession
from app.core.deps import get_current_user
from app.core.response import success_response
from app.crud import favorite
from app.models.user import User
from app.schemas.favorite import FavoriteStatusResponse, GetFavoriteStatusRequest

router = APIRouter(prefix="/api/favorite", tags=["favorites"])


@router.get("/check")
async def get_favorite_status(
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
):
    is_favorite = await favorite.get_favorite_status(
        db, user_id=user.id, news_id=news_id
    )
    return success_response(
        message="获取收藏状态成功",
        data=FavoriteStatusResponse.model_validate({"isFavorite": is_favorite}),
    )


@router.post("/add")
async def favorite_news(
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
    request_body: GetFavoriteStatusRequest,
):
    data = await favorite.favorite_news(
        db, user_id=user.id, news_id=request_body.news_id
    )
    return success_response(
        message="收藏文章成功",
        data=data,
    )


@router.delete("/remove")
async def remove_favorite(
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
):
    is_removed = await favorite.remove_favorite(db, user_id=user.id, news_id=news_id)
    if is_removed is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="取消收藏失败",
        )
    return success_response(
        message="取消收藏成功",
    )
