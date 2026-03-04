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
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/games` | 游戏列表（支持搜索/筛选/分页） |
| GET | `/api/games/{id}` | 游戏详情 |
| GET | `/api/games/{id}/rules` | 游戏规则 |
| GET | `/api/games/{id}/faq` | 游戏 FAQ |
| GET | `/api/user/ping` | 用户模块连通测试 |

### 游戏列表参数

| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 搜索关键词 |
| playerCount | int | 玩家人数 |
| durationMin | int | 最短时长 |
| durationMax | int | 最长时长 |
| difficulty | string | 简单/中等/困难 |
| hot | bool | 是否热门 |
| recommended | bool | 是否推荐 |
| page | int | 页码（默认 1） |
| pageSize | int | 每页数量（默认 20） |

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

# 5. 配置 systemd 服务实现开机自启（见下方）
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
