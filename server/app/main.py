"""BGaide 后端 API 入口"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import config
from .database import init_db
from .routers import games, user

# 静态文件目录
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化数据库"""
    init_db()
    print(f"🚀 BGaide API 已启动 | http://{config.HOST}:{config.PORT}")
    print(f"📖 API 文档 | http://{config.HOST}:{config.PORT}/docs")
    yield


app = FastAPI(
    title="BGaide API",
    description="桌游助手后端 API — 规则查询百科与游玩辅助工具库",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(games.router)
app.include_router(user.router)

# 挂载静态文件（图片等）
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", tags=["健康检查"])
def root():
    return {"status": "ok", "app": "BGaide API", "version": "1.0.0"}

