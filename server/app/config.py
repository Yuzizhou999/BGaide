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

# CORS 允许的来源（可通过环境变量覆盖）
# 例如：CORS_ORIGINS="https://bgaide.cloud,http://localhost:5173"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "https://bgaide.cloud,http://localhost:5173").split(",")
    if origin.strip()
]
