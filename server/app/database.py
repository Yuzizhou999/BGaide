"""SQLite 数据库初始化与数据导入"""

import json
import sqlite3
from pathlib import Path

from . import config


def get_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    conn = sqlite3.connect(config.DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 返回字典风格的行
    conn.execute("PRAGMA journal_mode=WAL")  # 提升并发读性能
    return conn


def get_db():
    """FastAPI 依赖注入：每个请求获取一个数据库连接，请求结束后关闭"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """建表 + 导入初始数据（幂等操作，已有数据则跳过）"""
    conn = get_connection()
    try:
        _create_tables(conn)
        _migrate_schema(conn)
        _seed_data(conn)
    finally:
        conn.close()


def _create_tables(conn: sqlite3.Connection):
    """创建数据表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS games (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            name_en     TEXT NOT NULL DEFAULT '',
            game_type   TEXT,
            aliases     TEXT NOT NULL DEFAULT '[]',   -- JSON 数组
            cover       TEXT NOT NULL DEFAULT '',
            thumb       TEXT NOT NULL DEFAULT '',
            players_min INTEGER NOT NULL DEFAULT 1,
            players_max INTEGER NOT NULL DEFAULT 4,
            duration_min INTEGER NOT NULL DEFAULT 0,
            duration_max INTEGER NOT NULL DEFAULT 0,
            difficulty  TEXT NOT NULL DEFAULT '中等',
            bgg_score   REAL NOT NULL DEFAULT 0,
            tags        TEXT NOT NULL DEFAULT '[]',   -- JSON 数组
            hot         INTEGER NOT NULL DEFAULT 0,   -- 0/1
            recommended INTEGER NOT NULL DEFAULT 0,   -- 0/1
            is_visible  INTEGER NOT NULL DEFAULT 1,   -- 0/1 是否展示
            description TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS rules (
            game_id     TEXT PRIMARY KEY,
            components  TEXT NOT NULL DEFAULT '[]',   -- JSON 数组
            setup       TEXT NOT NULL DEFAULT '[]',   -- JSON 数组
            win_condition TEXT NOT NULL DEFAULT '',
            turn_flow   TEXT NOT NULL DEFAULT '[]',   -- JSON 数组
            FOREIGN KEY (game_id) REFERENCES games(id)
        );

        CREATE TABLE IF NOT EXISTS faqs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id     TEXT NOT NULL,
            question    TEXT NOT NULL,
            answer      TEXT NOT NULL,
            sort_order  INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES games(id)
        );

        CREATE INDEX IF NOT EXISTS idx_faqs_game_id ON faqs(game_id);

        CREATE TABLE IF NOT EXISTS feedbacks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            type        TEXT NOT NULL CHECK (type IN ('correct', 'wish')),
            content     TEXT NOT NULL,
            created_at  INTEGER NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_feedbacks_type_created_at
            ON feedbacks(type, created_at DESC);

        CREATE TABLE IF NOT EXISTS user_collections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id  TEXT NOT NULL,
            game_id     TEXT NOT NULL,
            created_at  INTEGER NOT NULL,
            UNIQUE(visitor_id, game_id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        );

        CREATE INDEX IF NOT EXISTS idx_user_collections_visitor_id
            ON user_collections(visitor_id, created_at DESC);

        CREATE TABLE IF NOT EXISTS recommendations (
            slot        INTEGER PRIMARY KEY,
            game_id     TEXT NOT NULL,
            updated_at  INTEGER NOT NULL,
            UNIQUE(game_id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        );

        CREATE INDEX IF NOT EXISTS idx_recommendations_updated_at
            ON recommendations(updated_at DESC);
    """)


def _migrate_schema(conn: sqlite3.Connection):
    """对已有数据库执行轻量结构迁移"""
    columns = {
        row["name"] for row in conn.execute("PRAGMA table_info(games)").fetchall()
    }
    if "game_type" not in columns:
        conn.execute("ALTER TABLE games ADD COLUMN game_type TEXT")
    if "is_visible" not in columns:
        conn.execute("ALTER TABLE games ADD COLUMN is_visible INTEGER NOT NULL DEFAULT 1")
        conn.commit()


def _seed_data(conn: sqlite3.Connection):
    """从 JSON 文件导入初始数据（仅在表为空时导入）"""
    cursor = conn.execute("SELECT COUNT(*) FROM games")
    if cursor.fetchone()[0] > 0:
        return  # 已有数据，跳过

    data_dir = config.DATA_DIR

    # 导入游戏数据
    games_file = data_dir / "games.json"
    if games_file.exists():
        games = json.loads(games_file.read_text(encoding="utf-8"))
        for g in games:
            conn.execute("""
                INSERT INTO games (id, name, name_en, game_type, aliases, cover, thumb,
                    players_min, players_max, duration_min, duration_max,
                    difficulty, bgg_score, tags, hot, recommended, is_visible, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                g["id"], g["name"], g.get("nameEn", ""),
                g.get("gameType") or None,
                json.dumps(g.get("aliases", []), ensure_ascii=False),
                g.get("cover", ""), g.get("thumb", ""),
                g["players"][0], g["players"][1],
                g["duration"][0], g["duration"][1],
                g.get("difficulty", "中等"), g.get("bggScore", 0),
                json.dumps(g.get("tags", []), ensure_ascii=False),
                1 if g.get("hot") else 0,
                1 if g.get("recommended") else 0,
                1 if g.get("visible", True) else 0,
                g.get("description", ""),
            ))

    # 导入规则数据
    rules_file = data_dir / "rules.json"
    if rules_file.exists():
        rules = json.loads(rules_file.read_text(encoding="utf-8"))
        for game_id, rule in rules.items():
            ql = rule.get("quickLearn", {})
            conn.execute("""
                INSERT INTO rules (game_id, components, setup, win_condition, turn_flow)
                VALUES (?, ?, ?, ?, ?)
            """, (
                game_id,
                json.dumps(ql.get("components", []), ensure_ascii=False),
                json.dumps(ql.get("setup", []), ensure_ascii=False),
                ql.get("winCondition", ""),
                json.dumps(ql.get("turnFlow", []), ensure_ascii=False),
            ))

    # 导入 FAQ 数据
    faq_file = data_dir / "faq.json"
    if faq_file.exists():
        faqs = json.loads(faq_file.read_text(encoding="utf-8"))
        for game_id, items in faqs.items():
            for idx, item in enumerate(items):
                conn.execute("""
                    INSERT INTO faqs (game_id, question, answer, sort_order)
                    VALUES (?, ?, ?, ?)
                """, (game_id, item["q"], item["a"], idx))

    conn.commit()
    print(f"✅ 初始数据导入完成")
