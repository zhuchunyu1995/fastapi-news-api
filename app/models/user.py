import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.favorite import Favorite


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="分类ID"
    )
    username: Mapped[str] = mapped_column(
        String(50),  # ✅ 必须指定长度！50 是常见值
        index=True,  # 创建索引，加速查询
        unique=True,  # 唯一约束，不能重复
        nullable=False,  # 不能为空（NOT NULL）
        comment="用户ID",
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码（加密存储）",
    )

    nickname: Mapped[str | None] = mapped_column(
        String(50),
        comment="昵称",
        default=None,
    )
    avatar: Mapped[str | None] = mapped_column(
        String(255),
        comment="头像URL",
        default=None,
    )

    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, values_callable=lambda x: [e.value for e in x]),
        default=GenderEnum.UNKNOWN,
        comment="性别",
    )

    bio: Mapped[str | None] = mapped_column(
        String(500),
        comment="个人简介",
        default=None,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        comment="手机号",
        unique=True,
        default=None,
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now(), comment="更新时间"
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
