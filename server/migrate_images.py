"""更新数据库中的图片路径：从小程序本地路径改为后端 URL"""
import os
import sqlite3

BASE_URL = os.getenv("BASE_URL", "https://bgaide.cloud")

conn = sqlite3.connect("data/bgaide.db")
conn.row_factory = sqlite3.Row

# 更新 /static/ 开头的路径为后端完整 URL
conn.execute(
    "UPDATE games SET cover = ? || cover, thumb = ? || thumb WHERE cover LIKE '/static/%'",
    (BASE_URL, BASE_URL)
)
conn.commit()

# 验证结果
rows = conn.execute("SELECT id, cover, thumb FROM games").fetchall()
for r in rows:
    print(f"  {r['id']:20s} -> {r['cover'][:60]}")

conn.close()
print("\nDone!")
