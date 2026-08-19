from fastapi import FastAPI

from core.exception_handlers import register_exception_handlers
from core.middleware import register_cors
from routers import news, user

app = FastAPI()


# 注册异常处理函数
register_exception_handlers(app)


# 注册 CORS 中间件
register_cors(app)

# 注册路由
app.include_router(news.router)
app.include_router(user.router)
