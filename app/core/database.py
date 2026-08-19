from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings

# 创建异步引擎
async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发时打印SQL，生产环境建议设为False
    pool_size=settings.POOL_SIZE,  # 设置连接池活跃连接数
    max_overflow=settings.MAX_OVERFLOW,  # 设置连接池最大连接数
)
