from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.news import News
    from app.models.user import User


class Favorite(Base):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="收藏ID"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,  # ✅ 保留索引加速查询
        nullable=False,
        comment="用户ID",
    )

    news_id: Mapped[int] = mapped_column(
        ForeignKey("news.id", ondelete="CASCADE"),
        index=True,  # ✅ 索引，加速按新闻查询
        nullable=False,
        comment="新闻ID",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="uq_favorite_user_news"),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="favorites",
    )

    news: Mapped["News"] = relationship(
        "News",
        back_populates="favorites",
    )

    def __repr__(self):
        return f"Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})"
