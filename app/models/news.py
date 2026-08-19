from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now(), comment="更新时间"
    )


class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="分类ID"
    )
    name: Mapped[str] = mapped_column(
        String(50),  # ✅ 必须指定长度！50 是常见值
        index=True,  # 创建索引，加速查询
        unique=True,  # 唯一约束，不能重复
        nullable=False,  # 不能为空（NOT NULL）
        comment="分类名称",
    )
    sort_order: Mapped[int] = mapped_column(
        default=0, nullable=False, comment="排序顺序"
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, sort_order={self.sort_order})"


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="新闻ID"
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, default="", comment="新闻标题"
    )

    description: Mapped[str] = mapped_column(
        String(500), nullable=True, default=None, comment="新闻描述"
    )

    content: Mapped[str] = mapped_column(
        Text, nullable=False, default="", comment="新闻内容"
    )

    image: Mapped[str] = mapped_column(
        String(255), nullable=True, default=None, comment="封面图片URL"
    )

    author: Mapped[str] = mapped_column(
        String(50), nullable=True, default=None, comment="作者"
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "news_category.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
        comment="分类ID",
    )

    views: Mapped[int] = mapped_column(nullable=False, default=0, comment="浏览量")

    publish_time: Mapped[datetime] = mapped_column(
        index=True,
        default=datetime.now,
        server_default=func.now(),
        comment="发布时间",
    )
