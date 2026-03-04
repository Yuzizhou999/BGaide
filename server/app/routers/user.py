"""用户相关 API 路由（预留）

后续接入微信小程序登录后实现以下功能：
- POST /api/user/login       微信登录（code 换 openid）
- GET  /api/user/collections  获取收藏列表
- POST /api/user/collections/:gameId  添加/取消收藏
- GET  /api/user/history      获取浏览历史
- POST /api/user/history      记录浏览
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/ping", summary="用户模块连通测试")
def ping():
    return {"message": "用户模块已就绪，待接入微信登录"}
