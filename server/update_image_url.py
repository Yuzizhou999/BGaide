"""
批量更新数据库中游戏图片的 URL 前缀

用法：
  python update_image_url.py <新的基础地址>

示例：
  开发环境：python update_image_url.py http://localhost:8000
  生产环境：python update_image_url.py https://api.你的域名.com
  改回本地：python update_image_url.py ""
"""

import sqlite3
import sys

DB_PATH = "data/bgaide.db"

def main():
    if len(sys.argv) < 2:
        print("用法: python update_image_url.py <新的基础地址>")
        print("示例: python update_image_url.py https://api.example.com")
        return

    new_base = sys.argv[1].rstrip("/")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("SELECT id, cover, thumb FROM games").fetchall()

    updated = 0
    for r in rows:
        cover = r["cover"]
        thumb = r["thumb"]

        # 提取 /static/... 部分（去掉旧的 base URL）
        cover_path = _extract_path(cover)
        thumb_path = _extract_path(thumb)

        if cover_path:
            new_cover = f"{new_base}{cover_path}" if new_base else cover_path
            new_thumb = f"{new_base}{thumb_path}" if new_base else thumb_path

            conn.execute(
                "UPDATE games SET cover = ?, thumb = ? WHERE id = ?",
                (new_cover, new_thumb, r["id"])
            )
            print(f"  [OK] {r['id']:20s} -> {new_cover}")
            updated += 1
        else:
            print(f"  [--] {r['id']:20s} -> (外部链接，跳过)")

    conn.commit()
    conn.close()
    print(f"\n完成！更新了 {updated} 个游戏的图片地址")


def _extract_path(url):
    """从完整 URL 中提取 /static/... 路径部分"""
    if "/static/" in url:
        idx = url.index("/static/")
        return url[idx:]
    return None


if __name__ == "__main__":
    main()
