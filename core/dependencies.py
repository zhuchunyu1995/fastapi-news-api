from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.database import async_engine

# 创建了一个工厂，每次调用它就能得到一个数据库会话（类似一个"临时工作区"）
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,  # 不自动把变更发送到数据库
)


# 异步生成器，产出 AsyncSession
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # 每次请求时生成一个会话  从池子借连接
    async with AsyncSessionLocal() as session:
        try:
            # 把会话交给路由
            yield session
            # 提交事务成功
            await session.commit()
        except Exception:
            # 或 rollback（失败）
            await session.rollback()
            raise
        finally:
            # 归还连接池子
            await session.close()
