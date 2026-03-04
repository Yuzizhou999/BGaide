"""游戏相关 API 路由"""

import json
import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..models import (
    FAQItem, GameCreate, GameItem, PaginatedGames,
    QuickLearn, RulesCreate, RulesResponse,
)

router = APIRouter(prefix="/api/games", tags=["游戏"])


def _row_to_game(row: sqlite3.Row) -> GameItem:
    """将数据库行转换为 GameItem 模型"""
    return GameItem(
        id=row["id"],
        name=row["name"],
        nameEn=row["name_en"],
        cover=row["cover"],
        thumb=row["thumb"],
        players=[row["players_min"], row["players_max"]],
        duration=[row["duration_min"], row["duration_max"]],
        difficulty=row["difficulty"],
        bggScore=row["bgg_score"],
        tags=json.loads(row["tags"]),
        hot=bool(row["hot"]),
        recommended=bool(row["recommended"]),
        description=row["description"],
    )


@router.get("", response_model=PaginatedGames, summary="游戏列表")
def list_games(
    keyword: Optional[str] = Query(None, description="搜索关键词（匹配名称/英文名/别名）"),
    playerCount: Optional[int] = Query(None, description="支持的玩家人数"),
    durationMin: Optional[int] = Query(None, description="最短游戏时长（分钟）"),
    durationMax: Optional[int] = Query(None, description="最长游戏时长（分钟）"),
    difficulty: Optional[str] = Query(None, description="难度：简单/中等/困难"),
    hot: Optional[bool] = Query(None, description="是否热门"),
    recommended: Optional[bool] = Query(None, description="是否推荐"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(20, ge=1, le=100, description="每页数量"),
    db: sqlite3.Connection = Depends(get_db),
):
    """获取游戏列表，支持搜索、筛选和分页"""
    conditions = []
    params = []

    if keyword:
        kw = f"%{keyword}%"
        conditions.append(
            "(name LIKE ? OR name_en LIKE ? OR aliases LIKE ?)"
        )
        params.extend([kw, kw, kw])

    if playerCount is not None:
        conditions.append("players_min <= ? AND players_max >= ?")
        params.extend([playerCount, playerCount])

    if durationMin is not None:
        conditions.append("duration_max >= ?")
        params.append(durationMin)

    if durationMax is not None:
        conditions.append("duration_min <= ?")
        params.append(durationMax)

    if difficulty:
        conditions.append("difficulty = ?")
        params.append(difficulty)

    if hot is not None:
        conditions.append("hot = ?")
        params.append(1 if hot else 0)

    if recommended is not None:
        conditions.append("recommended = ?")
        params.append(1 if recommended else 0)

    where = " AND ".join(conditions) if conditions else "1=1"

    # 查询总数
    count_sql = f"SELECT COUNT(*) FROM games WHERE {where}"
    total = db.execute(count_sql, params).fetchone()[0]

    # 分页查询
    offset = (page - 1) * pageSize
    query_sql = f"SELECT * FROM games WHERE {where} ORDER BY bgg_score DESC LIMIT ? OFFSET ?"
    rows = db.execute(query_sql, params + [pageSize, offset]).fetchall()

    return PaginatedGames(
        total=total,
        page=page,
        pageSize=pageSize,
        data=[_row_to_game(row) for row in rows],
    )


@router.get("/{game_id}", response_model=GameItem, summary="游戏详情")
def get_game(game_id: str, db: sqlite3.Connection = Depends(get_db)):
    """获取单个游戏的详细信息"""
    row = db.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 不存在")
    return _row_to_game(row)


@router.get("/{game_id}/rules", response_model=RulesResponse, summary="游戏规则")
def get_rules(game_id: str, db: sqlite3.Connection = Depends(get_db)):
    """获取游戏的快速入门规则"""
    row = db.execute("SELECT * FROM rules WHERE game_id = ?", (game_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 的规则不存在")
    return RulesResponse(
        gameId=row["game_id"],
        quickLearn=QuickLearn(
            gameId=row["game_id"],
            components=json.loads(row["components"]),
            setup=json.loads(row["setup"]),
            winCondition=row["win_condition"],
            turnFlow=json.loads(row["turn_flow"]),
        ),
    )


@router.get("/{game_id}/faq", response_model=list[FAQItem], summary="游戏 FAQ")
def get_faq(game_id: str, db: sqlite3.Connection = Depends(get_db)):
    """获取游戏的常见问题"""
    rows = db.execute(
        "SELECT question, answer FROM faqs WHERE game_id = ? ORDER BY sort_order",
        (game_id,),
    ).fetchall()
    return [FAQItem(q=row["question"], a=row["answer"]) for row in rows]


# ══════════════════════════════════════════════
#  管理接口：增删改
# ══════════════════════════════════════════════

@router.post("", response_model=GameItem, status_code=201, summary="添加游戏",
             tags=["管理"])
def create_game(
    game: GameCreate,
    rules: RulesCreate | None = None,
    faq: list[FAQItem] | None = None,
    db: sqlite3.Connection = Depends(get_db),
):
    """添加一个新游戏，可同时传入规则和 FAQ"""
    # 检查 ID 是否已存在
    existing = db.execute("SELECT id FROM games WHERE id = ?", (game.id,)).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail=f"游戏 '{game.id}' 已存在")

    db.execute("""
        INSERT INTO games (id, name, name_en, aliases, cover, thumb,
            players_min, players_max, duration_min, duration_max,
            difficulty, bgg_score, tags, hot, recommended, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        game.id, game.name, game.nameEn,
        json.dumps(game.aliases, ensure_ascii=False),
        game.cover, game.thumb,
        game.players[0], game.players[1],
        game.duration[0], game.duration[1],
        game.difficulty, game.bggScore,
        json.dumps(game.tags, ensure_ascii=False),
        1 if game.hot else 0,
        1 if game.recommended else 0,
        game.description,
    ))

    # 同时插入规则（如果提供了）
    if rules:
        db.execute("""
            INSERT INTO rules (game_id, components, setup, win_condition, turn_flow)
            VALUES (?, ?, ?, ?, ?)
        """, (
            game.id,
            json.dumps(rules.components, ensure_ascii=False),
            json.dumps(rules.setup, ensure_ascii=False),
            rules.winCondition,
            json.dumps(rules.turnFlow, ensure_ascii=False),
        ))

    # 同时插入 FAQ（如果提供了）
    if faq:
        for idx, item in enumerate(faq):
            db.execute(
                "INSERT INTO faqs (game_id, question, answer, sort_order) VALUES (?, ?, ?, ?)",
                (game.id, item.q, item.a, idx),
            )

    db.commit()
    return _row_to_game(db.execute("SELECT * FROM games WHERE id = ?", (game.id,)).fetchone())


@router.put("/{game_id}", response_model=GameItem, summary="更新游戏", tags=["管理"])
def update_game(game_id: str, game: GameCreate, db: sqlite3.Connection = Depends(get_db)):
    """更新游戏基本信息"""
    existing = db.execute("SELECT id FROM games WHERE id = ?", (game_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 不存在")

    db.execute("""
        UPDATE games SET name=?, name_en=?, aliases=?, cover=?, thumb=?,
            players_min=?, players_max=?, duration_min=?, duration_max=?,
            difficulty=?, bgg_score=?, tags=?, hot=?, recommended=?, description=?
        WHERE id=?
    """, (
        game.name, game.nameEn,
        json.dumps(game.aliases, ensure_ascii=False),
        game.cover, game.thumb,
        game.players[0], game.players[1],
        game.duration[0], game.duration[1],
        game.difficulty, game.bggScore,
        json.dumps(game.tags, ensure_ascii=False),
        1 if game.hot else 0,
        1 if game.recommended else 0,
        game.description,
        game_id,
    ))
    db.commit()
    return _row_to_game(db.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone())


@router.delete("/{game_id}", summary="删除游戏", tags=["管理"])
def delete_game(game_id: str, db: sqlite3.Connection = Depends(get_db)):
    """删除游戏及其关联的规则和 FAQ"""
    existing = db.execute("SELECT id FROM games WHERE id = ?", (game_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 不存在")

    db.execute("DELETE FROM faqs WHERE game_id = ?", (game_id,))
    db.execute("DELETE FROM rules WHERE game_id = ?", (game_id,))
    db.execute("DELETE FROM games WHERE id = ?", (game_id,))
    db.commit()
    return {"message": f"游戏 '{game_id}' 已删除"}


@router.put("/{game_id}/rules", response_model=RulesResponse, summary="更新规则",
            tags=["管理"])
def update_rules(game_id: str, rules: RulesCreate, db: sqlite3.Connection = Depends(get_db)):
    """创建或更新游戏规则（覆盖式）"""
    existing = db.execute("SELECT id FROM games WHERE id = ?", (game_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 不存在")

    db.execute("DELETE FROM rules WHERE game_id = ?", (game_id,))
    db.execute("""
        INSERT INTO rules (game_id, components, setup, win_condition, turn_flow)
        VALUES (?, ?, ?, ?, ?)
    """, (
        game_id,
        json.dumps(rules.components, ensure_ascii=False),
        json.dumps(rules.setup, ensure_ascii=False),
        rules.winCondition,
        json.dumps(rules.turnFlow, ensure_ascii=False),
    ))
    db.commit()

    row = db.execute("SELECT * FROM rules WHERE game_id = ?", (game_id,)).fetchone()
    return RulesResponse(
        gameId=game_id,
        quickLearn=QuickLearn(
            gameId=game_id,
            components=json.loads(row["components"]),
            setup=json.loads(row["setup"]),
            winCondition=row["win_condition"],
            turnFlow=json.loads(row["turn_flow"]),
        ),
    )


@router.put("/{game_id}/faq", response_model=list[FAQItem], summary="更新FAQ",
            tags=["管理"])
def update_faq(game_id: str, faq: list[FAQItem], db: sqlite3.Connection = Depends(get_db)):
    """替换游戏的全部 FAQ（覆盖式）"""
    existing = db.execute("SELECT id FROM games WHERE id = ?", (game_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail=f"游戏 '{game_id}' 不存在")

    db.execute("DELETE FROM faqs WHERE game_id = ?", (game_id,))
    for idx, item in enumerate(faq):
        db.execute(
            "INSERT INTO faqs (game_id, question, answer, sort_order) VALUES (?, ?, ?, ?)",
            (game_id, item.q, item.a, idx),
        )
    db.commit()
    return faq
