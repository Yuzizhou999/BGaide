# BGaide 后端 API

桌游助手小程序的 FastAPI 后端服务。

## 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动开发服务器（自动热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 根路径：http://localhost:8000
- Swagger 文档：http://localhost:8000/api/docs
- ReDoc 文档：http://localhost:8000/api/redoc

生产环境访问：
- API 根路径：https://bgaide.cloud
- Swagger 文档：https://bgaide.cloud/api/docs
- ReDoc 文档：https://bgaide.cloud/api/redoc

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/games` | 游戏列表（支持搜索/筛选/分页） |
| GET | `/api/games/{id}` | 游戏详情 |
| GET | `/api/games/{id}/rules` | 游戏规则 |
| GET | `/api/games/{id}/faq` | 游戏 FAQ |
| GET | `/api/games/recommendations` | 获取推荐位配置（按顺序） |
| PUT | `/api/games/recommendations` | 更新推荐位配置（管理端） |
| GET | `/api/user/ping` | 用户模块连通测试 |
| GET | `/api/user/collections` | 获取收藏列表（visitorId） |
| POST | `/api/user/collections` | 同步单条收藏状态（收藏/取消） |
| POST | `/api/user/feedback` | 提交反馈（规则指正/心愿单） |
| GET | `/api/user/feedback` | 反馈列表（支持分页与类型筛选） |

### 游戏列表参数

| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 搜索关键词 |
| playerCount | int | 玩家人数 |
| durationMin | int | 最短时长 |
| durationMax | int | 最长时长 |
| gameType | string | 类型：德式/美式/毛线聚会 |
| difficulty | string | 简单/中等/困难 |
| hot | bool | 是否热门 |
| recommended | bool | 是否推荐 |
| includeHidden | bool | 是否包含下架游戏（默认 false） |
| shuffleSeed | string | 稳定随机种子（同一 seed 下分页顺序稳定） |
| page | int | 页码（默认 1） |
| pageSize | int | 每页数量（默认 20） |

### 推荐位后台配置

- 小程序推荐页会读取后端 `/api/games/recommendations`，不再在小程序端配置。
- 按 `gameIds` 顺序展示，最多 9 个；不传或传空数组表示回退为自动推荐策略。

示例：

```bash
curl -X PUT 'https://bgaide.cloud/api/games/recommendations' \
	-H 'Content-Type: application/json' \
	-d '{"gameIds": ["catan", "avalon", "werewolf", "codenames"]}'
```

读取当前配置：

```bash
curl 'https://bgaide.cloud/api/games/recommendations'
```

### 游戏可见性字段

- `visible`（bool）：是否在前台展示该游戏。
- 默认 `true`（上架）；设置为 `false` 后，`GET /api/games` 默认不会返回该游戏。

### 游戏类型字段

- `gameType`（string）：游戏类型，支持 `德式`、`美式`、`毛线聚会`。
- 老数据未填写该字段时为 `null`，不会影响现有展示和查询。

## 服务器部署（CentOS）

```bash
# 1. 安装 Python 3.11
yum install -y python3.11 python3.11-pip

# 2. 上传项目到服务器
scp -r server/ root@你的IP:/root/bgaide-server/

# 3. 在服务器上
cd /root/bgaide-server
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. 使用 Gunicorn 启动（生产环境）
pip install gunicorn
gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 5. （首次切域名时）更新图片 URL 前缀
python update_image_url.py https://bgaide.cloud

# 6. 配置 systemd 服务实现开机自启（见下方）
```

### systemd 服务配置

创建 `/etc/systemd/system/bgaide-api.service`：

```ini
[Unit]
Description=BGaide API
After=network.target

[Service]
User=root
WorkingDirectory=/root/bgaide-server
ExecStart=/root/bgaide-server/venv/bin/gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable bgaide-api
systemctl start bgaide-api
```
