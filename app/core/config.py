from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = (
        "mysql+aiomysql://root:260325Cy@localhost:3306/news_app?charset=utf8mb4"
    )
    # 数据库连接池配置
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20

    # 应用配置
    DEBUG: bool = True
    # JWT 配置
    SECRET_KEY: str = "kid55m9"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS 配置
    allowed_origins: str = "http://localhost:5173"
    allow_credentials: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
