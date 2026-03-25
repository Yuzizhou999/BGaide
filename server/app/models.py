"""Pydantic 响应模型"""

from pydantic import BaseModel


# ── 游戏列表项 ──
class GameItem(BaseModel):
    id: str
    name: str
    nameEn: str = ""
    gameType: str | None = None
    cover: str = ""
    thumb: str = ""
    players: list[int]        # [min, max]
    duration: list[int]       # [min, max]
    difficulty: str = "中等"
    bggScore: float = 0
    tags: list[str] = []
    hot: bool = False
    recommended: bool = False
    visible: bool = True
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
    gameType: str | None = None
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
    visible: bool = True
    description: str = ""


class RulesCreate(BaseModel):
    components: list[str] = []
    setup: list[str] = []
    winCondition: str = ""
    turnFlow: list[str] = []


# ── 用户反馈 ──
class FeedbackCreate(BaseModel):
    type: str  # correct / wish
    content: str


class FeedbackItem(BaseModel):
    id: int
    type: str
    content: str
    createdAt: int


class PaginatedFeedbacks(BaseModel):
    total: int
    page: int
    pageSize: int
    data: list[FeedbackItem]


# ── 收藏 ──
class CollectionSyncPayload(BaseModel):
    visitorId: str
    gameId: str
    collected: bool


class CollectionSyncResult(BaseModel):
    visitorId: str
    gameId: str
    collected: bool


class CollectionListResponse(BaseModel):
    visitorId: str
    gameIds: list[str]


# ── 推荐位配置 ──
class RecommendConfigPayload(BaseModel):
    gameIds: list[str] = []


class RecommendConfigResponse(BaseModel):
    gameIds: list[str]
    data: list[GameItem]
