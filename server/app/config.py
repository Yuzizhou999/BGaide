"""应用配置"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据库
DATABASE_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "bgaide.db"))

# JSON 数据源目录（仅首次初始化用）
DATA_DIR = BASE_DIR / "data"

# 服务器
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# CORS 允许的来源
CORS_ORIGINS = [
    "*",  # 开发阶段允许所有来源，生产环境应改为具体域名
]
