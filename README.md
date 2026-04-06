# 国泰 AI 主厨 · Cathay Culinary Experience

> 基于国泰航空餐饮服务的 Hackathon 示范项目。结合 **Django REST Framework** + **Vue 3** + **DashScope (Qwen Plus)** + **AR 展示**，为乘客打造沉浸式餐饮体验。

---

## ✨ 核心功能

- **🤖 AI 主厨对话**：通过 DashScope Qwen Plus 提供食材搭配、文化故事、营养建议与烹饪技法解答
- **📱 互动式菜单**：Vue 3 + Element Plus 打造餐食/饮品分区、过敏原标签、详细营养信息与文化叙事
- **📊 用餐反馈系统**：支持口味/口感/分量评分、剩餐原因记录、照片上传与里程积分发放
- **🥽 AR 虚拟展示**：整合 Kivicube AR 场景，提供沉浸式菜品 3D 体验（含工具栏操作与多语言提示）
- **🔐 会员认证系统**：支持邮箱/手机号注册登录（OTP 验证码）、JWT 鉴权、自动 Token 刷新、注册奖励积分与里程
- **🌐 三语言切换**：完整支持繁体中文（香港）、简体中文、英文界面切换
- **🔗 CX 整合桥接**：预留与国泰预点餐系统、Lifestyle 商城的桥接接口
- **📚 API 文档**：drf-spectacular 自动生成完整 Swagger 文档

---

## 🏗️ 技术架构

```text
前端 (Vue 3 SPA)
    ↓ axios
    ↓ Vite proxy (:5173)
后端 (Django REST :8000)
    ↓
    ├─ DashScope SDK (Qwen Plus AI)
    ├─ SQLite/MySQL Database
    └─ Kivicube AR 场景整合
```

**前端技术栈**

- Vue 3 (Composition API) + Vue Router + Pinia
- Element Plus UI 框架
- Vue I18n (三语言支持)
- Axios (HTTP 客户端)
- Vite (开发与构建工具)

**后端技术栈**

- Django 5.0+ + Django REST Framework
- SimpleJWT (身份认证)
- drf-spectacular (API 文档)
- DashScope / LangChain (AI 对话)
- Pillow (图片处理)
- django-cors-headers (跨域支持)

---

## 🗂️ 项目结构

```text
CathyHackathon/
├─ backend/                    # Django 后端服务
│  ├─ core/                    # 项目设置、URL 路由、CORS 配置
│  ├─ accounts/                # 用户认证模块（注册/登录/OTP/JWT/会员信息）
│  ├─ ai_chef/                 # AI 主厨聊天 API (DashScope 整合)
│  ├─ menu/                    # 菜品、配料、过敏原、FAQ 数据 API
│  ├─ chat/                    # 聊天 Session 与消息模型
│  ├─ surveys/                 # 问卷、剩餐记录、积分、周期性反馈
│  ├─ integrations/            # 对外系统桥接（CX 预点餐等）
│  ├─ fixtures/                # 初始数据 (dish_menu.json, drink_menu.json 等)
│  ├─ tests/                   # 后端测试脚本集合
│  ├─ dish.py                  # 菜品数据辅助脚本
│  ├─ install_relay.py         # 中继服务安装脚本
│  ├─ test_ai_chat.py          # AI 对话功能测试脚本
│  ├─ manage.py
│  ├─ requirements.txt
│  └─ db.sqlite3               # 默认数据库（开发用）
│
└─ frontend/                   # Vue 3 前端应用
   ├─ src/
   │  ├─ pages/                # 页面组件
   │  │  ├─ Home.vue           # 首页 (功能导览)
   │  │  ├─ Menu.vue           # 菜单列表
   │  │  ├─ DishDetail.vue     # 菜品详情 (文化故事、营养信息)
   │  │  ├─ AIChef.vue         # AI 主厨对话页
   │  │  ├─ ArView.vue         # AR 虚拟展示页
   │  │  ├─ Survey.vue         # 用餐反馈问卷
   │  │  ├─ MyFeedback.vue     # 我的反馈记录
   │  │  ├─ Preselect.vue      # 生活精品商城导流
   │  │  └─ Auth.vue           # 登录/注册页（支持 OTP 验证）
   │  │
   │  ├─ components/           # 可复用组件
   │  │  ├─ AppHeader.vue      # 顶部导航栏
   │  │  ├─ AppFooter.vue      # 底部信息
   │  │  ├─ ChefChatPanel.vue  # AI 聊天面板
   │  │  ├─ DishCard.vue       # 菜品卡片
   │  │  ├─ MemberFlightCard.vue # 会员航班卡片
   │  │  └─ LanguageSwitcher.vue # 语言切换器
   │  │
   │  ├─ stores/               # Pinia 状态管理
   │  │  ├─ auth.js            # 认证 Store（JWT 管理、Token 自动刷新、注册奖励）
   │  │  └─ index.js           # Store 入口
   │  │
   │  ├─ api/
   │  │  └─ http.js            # Axios 实例与拦截器
   │  │
   │  ├─ i18n/                 # 多语言文案
   │  │  ├─ en.json            # 英文
   │  │  ├─ zh.json            # 简体中文
   │  │  ├─ zh-HK.json         # 繁体中文（香港）
   │  │  └─ check_i18n.py      # 多语言文案一致性检查脚本
   │  │
   │  ├─ router/
   │  │  └─ index.js           # 路由配置
   │  │
   │  ├─ styles/
   │  │  └─ theme.css          # 全局样式与 Cathay 配色
   │  │
   │  ├─ utils/
   │  │  └─ chinese.js         # 简繁转换工具
   │  │
   │  ├─ App.vue               # 根组件
   │  └─ main.js               # 入口文件 (i18n、router、pinia 初始化)
   │
   ├─ vite.config.js           # Vite 配置 (proxy 设置)
   ├─ package.json
   └─ index.html
```

---

## ⚙️ 快速开始

### 1. 先决条件

- Python 3.11+
- Node.js 18+ / npm 9+
- DashScope 账号与 API Key
- （可选）MySQL 8.0+，默认使用 SQLite

### 2. 后端安装与启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 设置环境变量
export DASHSCOPE_API_KEY="your-dashscope-api-key"
export DJANGO_SECRET_KEY="your-secret-key-here"
export DEBUG=1

# 初始化数据库
python manage.py migrate

# 加载示例数据
python manage.py loaddata fixtures/dish_menu.json
python manage.py loaddata fixtures/dish2_menu.json
python manage.py loaddata fixtures/drink_menu.json
python manage.py loaddata fixtures/drink2_menu.json

# 启动开发服务器
python manage.py runserver
```

后端服务启动后：

- API 根路径：`http://127.0.0.1:8000/api/`
- Swagger 文档：`http://127.0.0.1:8000/api/docs/`
- 媒体文件：`http://127.0.0.1:8000/media/`

### 3. 前端安装与启动

```bash
cd frontend
npm install
npm run dev
```

前端服务启动后：

- 应用首页：`http://127.0.0.1:5173`
- Vite 已配置 proxy，自动将 `/api` 与 `/media` 请求转发至后端

### 4. 功能验收

- **AI 主厨体验**：`http://127.0.0.1:5173/chef`
- **菜单浏览**：`http://127.0.0.1:5173/menu`
- **菜品详情**：`http://127.0.0.1:5173/dish/:id`
- **AR 展示**：`http://127.0.0.1:5173/ar` (需 HTTPS 或 localhost)
- **用餐反馈**：`http://127.0.0.1:5173/survey`
- **反馈记录**：`http://127.0.0.1:5173/my-feedback`
- **生活精品**：`http://127.0.0.1:5173/preselect`

---

## 🔑 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | DashScope AI 服务认证密钥（必填） | 无 |
| `DJANGO_SECRET_KEY` | Django 加密签章密钥 | 开发用默认值 |
| `DEBUG` | 开启 Django 调试模式 | `0` (生产) |
| `ALLOWED_HOSTS` | 允许的主机名称列表 | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | 前端跨域来源白名单 | `http://127.0.0.1:5173` |
| `DATABASE_URL` | 数据库连接字符串（可选） | SQLite |

---

## 📡 API 快速参考

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register/` | POST | 用户注册（OTP 验证，返回 JWT + 奖励信息） |
| `/api/auth/login/` | POST | 用户登录（邮箱/手机号 + 密码，返回 JWT） |
| `/api/auth/refresh/` | POST | 刷新 Access Token |
| `/api/auth/me/` | GET | 获取当前登录用户信息（需认证） |
| `/api/auth/send-otp/` | POST | 发送 OTP 验证码（邮件或短信） |
| `/api/dishes/` | GET | 获取所有菜品列表（含过敏原、配料摘要） |
| `/api/dishes/<id>/` | GET | 获取单一菜品详细信息 |
| `/api/allergens/` | GET | 获取过敏原主数据 |
| `/api/ingredients/` | GET | 获取食材主数据 |
| `/api/chef/chat/` | POST | AI 主厨对话 `{"message": "..."}` |
| `/api/chat/` | POST | FAQ 聊天（需 `dish_id` + `question`） |
| `/api/survey/` | GET/POST/PUT/DELETE | 问卷提交、查询与更新 |
| `/api/leftover/` | POST | 上传菜品/剩餐照片（multipart/form-data） |
| `/api/periodic-feedback/` | POST | 提交周期性建议 |
| `/api/integrations/cx/choose-meal/` | POST | CX 系统桥接接口 |

**AI 主厨对话示例**

```bash
curl -X POST http://127.0.0.1:8000/api/chef/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"请推荐适合老人的汤品"}'
```

**提交用餐反馈示例**

```bash
curl -X POST http://127.0.0.1:8000/api/survey/ \
  -H "Content-Type: application/json" \
  -d '{
    "dish_id": 1,
    "rating": 5,
    "taste": "balanced",
    "texture": "balanced",
    "quantity": "just_right",
    "leftover_level": 0,
    "notes": "非常美味！"
  }'
```

```

---

## 🗃️ 项目资源

### 初始数据

- `backend/fixtures/dish_menu.json` - 主要菜品数据（八宝红蟳饭等）
- `backend/fixtures/dish2_menu.json` - 补充菜品数据
- `backend/fixtures/drink_menu.json` - 饮品数据（铁观音茶、葡萄酒等）
- `backend/fixtures/drink2_menu.json` - 补充饮品数据

### 前端素材

- `frontend/src/assets/` - AI 主厨图标、厨师照片、菜品示意图
- `frontend/src/i18n/*.json` - 三语言翻译文案资源

### 语言资源说明

- `zh-HK.json` - 繁体中文（香港）**当前使用版本**
- `zh.json` - 简体中文
- `en.json` - 英文
- `check_i18n.py` - 多语言文案一致性检查工具（验证各语言文件键值结构是否匹配）

---

## 🧪 测试与验证

```bash
# 后端测试
cd backend
python manage.py test

# 测试 AI 对话功能
python test_ai_chat.py

# 运行 tests/ 目录下的专项测试脚本（例如）
python tests/test_ai_chef_menu.py
python tests/test_delete_survey.py

# 前端构建测试
cd frontend
npm run build
npm run preview
```

---

## 🚀 部署建议

1. **数据库升级**：切换至 MySQL / PostgreSQL，设置连接池 (`CONN_MAX_AGE=600`)
2. **安全性配置**：
   - 关闭 `DEBUG=0`
   - 设置 `ALLOWED_HOSTS`
   - 限制 `CORS_ALLOWED_ORIGINS`
   - 使用环境变量或 Secret Manager 管理敏感信息
3. **静态文件**：执行 `python manage.py collectstatic`
4. **后端服务**：使用 Gunicorn / uWSGI + Nginx
5. **前端部署**：`npm run build` 后部署至 CDN 或静态服务器
6. **媒体存储**：建议使用 AWS S3 / Azure Blob 等对象存储服务

---

## 🧰 常见问题

**Q: DashScope API 响应格式变更怎么办？**

A: `AIChefChatView` 已实现备援逻辑，支持 `output.text` 与 `output.choices` 两种格式。如仍失败，请检查响应日志并更新解析逻辑。

**Q: 出现 CORS 错误**

A: 开发环境已允许所有来源。生产环境请在 `settings.py` 中设置 `CORS_ALLOWED_ORIGINS`。

**Q: SQLite 数据库锁定错误**

A: SQLite 不适合多线程/多进程环境，建议切换至 MySQL 或 PostgreSQL。

**Q: 媒体文件无法显示**

A: 确认 Vite proxy 配置正确，或在生产环境使用独立对象存储服务。

**Q: AR 功能无法使用**

A: AR 功能需要 HTTPS 环境或 localhost。检查浏览器是否支持 WebGL 和摄像头权限。

**Q: 语言切换后部分文字未翻译**

A: 检查 `i18n/*.json` 是否包含对应的翻译键值。确保所有语言文件的键值结构一致。

---

## 📄 授权与声明

本项目仅供 Hackathon 示范与学习用途，不代表国泰航空官方产品。

- 所有营养与健康信息仅供参考，非专业医疗建议
- AI 生成内容可能存在错误，请谨慎参考
- 欢迎 Fork 并扩充功能（RAG、会员系统、支付整合等）

---

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request！

主要改进方向：

- 🔍 整合 RAG (Retrieval-Augmented Generation) 提升 AI 回答准确度
- 👤 完善会员系统与权限管理
- 💳 整合支付与积分兑换功能
- 📊 增加数据分析与报表功能
- 🌍 扩展更多语言支持
- ♿ 提升无障碍功能 (A11y)

---

## 📧 联系信息

项目维护：CathyHackathon Team

技术支持：请通过 GitHub Issues 提问

---

**Built with ❤️ for Cathay Pacific Hackathon**
