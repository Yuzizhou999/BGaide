"""Pydantic 响应模型"""

from pydantic import BaseModel


# ── 游戏列表项 ──
class GameItem(BaseModel):
    id: str
    name: str
    nameEn: str = ""
    cover: str = ""
    thumb: str = ""
    players: list[int]        # [min, max]
    duration: list[int]       # [min, max]
    difficulty: str = "中等"
    bggScore: float = 0
    tags: list[str] = []
    hot: bool = False
    recommended: bool = False
    description: str = ""


# ── 游戏规则 ──
class QuickLearn(BaseModel):
    gameId: str
    components: list[str] = []
    setup: list[str] = []
    winCondition: str = ""
    turnFlow: list[str] = []


class RulesResponse(BaseModel):
    gameId: str
    quickLearn: QuickLearn


# ── FAQ ──
class FAQItem(BaseModel):
    q: str
    a: str


# ── 通用分页响应 ──
class PaginatedGames(BaseModel):
    total: int
    page: int
    pageSize: int
    data: list[GameItem]


# ── 管理接口：创建/更新请求体 ──
class GameCreate(BaseModel):
    id: str
    name: str
    nameEn: str = ""
    aliases: list[str] = []
    cover: str = ""
    thumb: str = ""
    players: list[int]        # [min, max]
    duration: list[int]       # [min, max]
    difficulty: str = "中等"
    bggScore: float = 0
    tags: list[str] = []
    hot: bool = False
    recommended: bool = False
    description: str = ""


class RulesCreate(BaseModel):
    components: list[str] = []
    setup: list[str] = []
    winCondition: str = ""
    turnFlow: list[str] = []
