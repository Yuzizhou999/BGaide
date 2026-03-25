"""用户相关 API 路由"""

import sqlite3
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import get_db
from ..models import (
    CollectionListResponse,
    CollectionSyncPayload,
    CollectionSyncResult,
    FeedbackCreate,
    FeedbackItem,
    PaginatedFeedbacks,
)

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/ping", summary="用户模块连通测试")
def ping():
    return {"message": "用户模块已就绪，待接入微信登录"}


@router.get("/collections", response_model=CollectionListResponse, summary="获取收藏列表")
def list_collections(
    visitorId: str = Query(..., min_length=1, description="访客标识"),
    db: sqlite3.Connection = Depends(get_db),
):
    """按 visitorId 获取收藏的游戏 ID 列表"""
    visitor_id = visitorId.strip()
    rows = db.execute(
        "SELECT game_id FROM user_collections WHERE visitor_id = ? ORDER BY created_at DESC",
        (visitor_id,),
    ).fetchall()
    return CollectionListResponse(visitorId=visitor_id, gameIds=[row["game_id"] for row in rows])


@router.post("/collections", response_model=CollectionSyncResult, summary="同步收藏状态")
def sync_collection(
    payload: CollectionSyncPayload,
    db: sqlite3.Connection = Depends(get_db),
):
    """将单条收藏状态同步到服务端（收藏/取消收藏）"""
    visitor_id = (payload.visitorId or "").strip()
    game_id = (payload.gameId or "").strip()
    if not visitor_id or not game_id:
        raise HTTPException(status_code=422, detail="visitorId 和 gameId 不能为空")

    if payload.collected:
        db.execute(
            """
            INSERT INTO user_collections (visitor_id, game_id, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(visitor_id, game_id) DO UPDATE SET created_at = excluded.created_at
            """,
            (visitor_id, game_id, int(time.time() * 1000)),
        )
    else:
        db.execute(
            "DELETE FROM user_collections WHERE visitor_id = ? AND game_id = ?",
            (visitor_id, game_id),
        )

    db.commit()
    return CollectionSyncResult(visitorId=visitor_id, gameId=game_id, collected=payload.collected)


@router.post("/feedback", response_model=FeedbackItem, status_code=201, summary="提交反馈")
def create_feedback(payload: FeedbackCreate, db: sqlite3.Connection = Depends(get_db)):
    """提交用户反馈（规则指正/心愿单）"""
    feedback_type = (payload.type or "").strip().lower()
    if feedback_type not in {"correct", "wish"}:
        raise HTTPException(status_code=422, detail="type 必须是 correct 或 wish")

    content = (payload.content or "").strip()
    if not content:
        raise HTTPException(status_code=422, detail="content 不能为空")

    # 限制长度，避免异常大文本
    content = content[:500]
    created_at = int(time.time() * 1000)

    cursor = db.execute(
        "INSERT INTO feedbacks (type, content, created_at) VALUES (?, ?, ?)",
        (feedback_type, content, created_at),
    )
    db.commit()

    return FeedbackItem(
        id=cursor.lastrowid,
        type=feedback_type,
        content=content,
        createdAt=created_at,
    )


@router.get("/feedback", response_model=PaginatedFeedbacks, summary="反馈列表")
def list_feedbacks(
    type: Optional[str] = Query(None, description="过滤类型：correct / wish"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(20, ge=1, le=100, description="每页数量"),
    db: sqlite3.Connection = Depends(get_db),
):
    """查询反馈列表（可按类型筛选）"""
    conditions = []
    params = []

    if type is not None:
        feedback_type = type.strip().lower()
        if feedback_type not in {"correct", "wish"}:
            raise HTTPException(status_code=422, detail="type 必须是 correct 或 wish")
        conditions.append("type = ?")
        params.append(feedback_type)

    where = " AND ".join(conditions) if conditions else "1=1"
    total = db.execute(f"SELECT COUNT(*) FROM feedbacks WHERE {where}", params).fetchone()[0]

    offset = (page - 1) * pageSize
    rows = db.execute(
        f"SELECT id, type, content, created_at FROM feedbacks WHERE {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        params + [pageSize, offset],
    ).fetchall()

    return PaginatedFeedbacks(
        total=total,
        page=page,
        pageSize=pageSize,
        data=[
            FeedbackItem(
                id=row["id"],
                type=row["type"],
                content=row["content"],
                createdAt=row["created_at"],
            )
            for row in rows
        ],
    )
