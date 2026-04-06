# 國泰 AI 主廚 · Cathay Culinary Experience

> 基於國泰航空餐飲服務的 Hackathon 示範專案。結合 **Django REST Framework** + **Vue 3** + **DashScope (Qwen Plus)** + **AR 展示**，為乘客打造沉浸式餐飲體驗。

---

## ✨ 核心功能

- **🤖 AI 主廚對話**：透過 DashScope Qwen Plus 提供食材搭配、文化故事、營養建議與烹飪技法解答
- **📱 互動式菜單**：Vue 3 + Element Plus 打造餐食/飲品分區、過敏原標籤、詳細營養資訊與文化敘事
- **📊 用餐反饋系統**：支援口味/口感/分量評分、剩餐原因紀錄、照片上傳與里程積分發放
- **🥽 AR 虛擬展示**：整合 Kivicube AR 場景，提供沉浸式菜品 3D 體驗（含工具欄操作與多語言提示）
- **🌐 三語言切換**：完整支援繁體中文（香港）、簡體中文、英文介面切換
- **🔗 CX 整合橋接**：預留與國泰預點餐系統、Lifestyle 商城的橋接介面
- **📚 API 文件**：drf-spectacular 自動產生完整 Swagger 文件

---

## 🏗️ 技術架構

```text
前端 (Vue 3 SPA)
    ↓ axios
    ↓ Vite proxy (:5173)
後端 (Django REST :8000)
    ↓
    ├─ DashScope SDK (Qwen Plus AI)
    ├─ SQLite/MySQL Database
    └─ Kivicube AR 場景整合
```

**前端技術棧**

- Vue 3 (Composition API) + Vue Router + Pinia
- Element Plus UI 框架
- Vue I18n (三語言支援)
- Axios (HTTP 客戶端)
- Vite (開發與構建工具)

**後端技術棧**

- Django 5.0+ + Django REST Framework
- SimpleJWT (身份認證)
- drf-spectacular (API 文件)
- DashScope / LangChain (AI 對話)
- Pillow (圖片處理)
- django-cors-headers (跨域支援)

---

## 🗂️ 專案結構

```text
CathyHackathon/
├─ backend/                    # Django 後端服務
│  ├─ core/                    # 專案設定、URL 路由、CORS 配置
│  ├─ ai_chef/                 # AI 主廚聊天 API (DashScope 整合)
│  ├─ menu/                    # 菜品、配料、過敏原、FAQ 資料 API
│  ├─ chat/                    # 聊天 Session 與訊息模型
│  ├─ surveys/                 # 問卷、剩餐紀錄、積分、週期性回饋
│  ├─ integrations/            # 對外系統橋接（CX 預點餐等）
│  ├─ fixtures/                # 初始資料 (dish_menu.json, drink_menu.json 等)
│  ├─ manage.py
│  ├─ requirements.txt
│  └─ db.sqlite3               # 預設資料庫（開發用）
│
└─ frontend/                   # Vue 3 前端應用
   ├─ src/
   │  ├─ pages/                # 頁面元件
   │  │  ├─ Home.vue           # 首頁 (功能導覽)
   │  │  ├─ Menu.vue           # 菜單列表
   │  │  ├─ DishDetail.vue     # 菜品詳情 (文化故事、營養資訊)
   │  │  ├─ AIChef.vue         # AI 主廚對話頁
   │  │  ├─ ArView.vue         # AR 虛擬展示頁
   │  │  ├─ Survey.vue         # 用餐反饋問卷
   │  │  ├─ MyFeedback.vue     # 我的反饋紀錄
   │  │  ├─ Preselect.vue      # 生活精品商城導流
   │  │  └─ Auth.vue           # 登入/註冊頁
   │  │
   │  ├─ components/           # 可重用元件
   │  │  ├─ AppHeader.vue      # 頂部導航欄
   │  │  ├─ AppFooter.vue      # 底部資訊
   │  │  ├─ ChefChatPanel.vue  # AI 聊天面板
   │  │  ├─ DishCard.vue       # 菜品卡片
   │  │  └─ LanguageSwitcher.vue # 語言切換器
   │  │
   │  ├─ api/
   │  │  └─ http.js            # Axios 實例與攔截器
   │  │
   │  ├─ i18n/                 # 多語言文案
   │  │  ├─ en.json            # 英文
   │  │  ├─ zh.json            # 簡體中文
   │  │  └─zh-HK.json          # 繁體中文（香港）
   │  │   
   │  │
   │  ├─ router/
   │  │  └─ index.js           # 路由配置
   │  │
   │  ├─ styles/
   │  │  └─ theme.css          # 全域樣式與 Cathay 配色
   │  │
   │  ├─ utils/
   │  │  └─ chinese.js         # 簡繁轉換工具
   │  │
   │  ├─ App.vue               # 根元件
   │  └─ main.js               # 入口檔案 (i18n、router、pinia 初始化)
   │
   ├─ vite.config.js           # Vite 配置 (proxy 設定)
   ├─ package.json
   └─ index.html
```

---

## ⚙️ 快速開始

### 1. 先決條件

- Python 3.11+
- Node.js 18+ / npm 9+
- DashScope 帳號與 API Key
- （可選）MySQL 8.0+，預設使用 SQLite

### 2. 後端安裝與啟動

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 設定環境變數
export DASHSCOPE_API_KEY="your-dashscope-api-key"
export DJANGO_SECRET_KEY="your-secret-key-here"
export DEBUG=1

# 初始化資料庫
python manage.py migrate

# 載入範例資料
python manage.py loaddata fixtures/dish_menu.json
python manage.py loaddata fixtures/dish2_menu.json
python manage.py loaddata fixtures/drink_menu.json
python manage.py loaddata fixtures/drink2_menu.json

# 啟動開發伺服器
python manage.py runserver
```

後端服務啟動後：

- API 根路徑：`http://127.0.0.1:8000/api/`
- Swagger 文件：`http://127.0.0.1:8000/api/docs/`
- 媒體檔案：`http://127.0.0.1:8000/media/`

### 3. 前端安裝與啟動

```bash
cd frontend
npm install
npm run dev
```

前端服務啟動後：

- 應用首頁：`http://127.0.0.1:5173`
- Vite 已配置 proxy，自動將 `/api` 與 `/media` 請求轉發至後端

### 4. 功能驗收

- **AI 主廚體驗**：`http://127.0.0.1:5173/chef`
- **菜單瀏覽**：`http://127.0.0.1:5173/menu`
- **菜品詳情**：`http://127.0.0.1:5173/dish/:id`
- **AR 展示**：`http://127.0.0.1:5173/ar` (需 HTTPS 或 localhost)
- **用餐反饋**：`http://127.0.0.1:5173/survey`
- **反饋紀錄**：`http://127.0.0.1:5173/my-feedback`
- **生活精品**：`http://127.0.0.1:5173/preselect`

---

## 🔑 環境變數

| 變數 | 說明 | 預設值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | DashScope AI 服務認證金鑰（必填） | 無 |
| `DJANGO_SECRET_KEY` | Django 加密簽章金鑰 | 開發用預設值 |
| `DEBUG` | 開啟 Django 除錯模式 | `0` (生產) |
| `ALLOWED_HOSTS` | 允許的主機名稱列表 | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | 前端跨域來源白名單 | `http://127.0.0.1:5173` |
| `DATABASE_URL` | 資料庫連線字串（可選） | SQLite |

---

## 📡 API 快速參考

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/dishes/` | GET | 取得所有菜品列表（含過敏原、配料摘要） |
| `/api/dishes/<id>/` | GET | 取得單一菜品詳細資訊 |
| `/api/allergens/` | GET | 取得過敏原主資料 |
| `/api/ingredients/` | GET | 取得食材主資料 |
| `/api/chef/chat/` | POST | AI 主廚對話 `{"message": "..."}` |
| `/api/chat/` | POST | FAQ 聊天（需 `dish_id` + `question`） |
| `/api/survey/` | GET/POST/PUT/DELETE | 問卷提交、查詢與更新 |
| `/api/leftover/` | POST | 上傳菜品/剩餐照片（multipart/form-data） |
| `/api/periodic-feedback/` | POST | 提交週期性建議 |
| `/api/integrations/cx/choose-meal/` | POST | CX 系統橋接介面 |

**AI 主廚對話範例**

```bash
curl -X POST http://127.0.0.1:8000/api/chef/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"請推薦適合長輩的湯品"}'
```

**提交用餐反饋範例**

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

## 🗃️ 專案資源

### 初始資料

- `backend/fixtures/dish_menu.json` - 主要菜品資料（八寶紅蟳飯等）
- `backend/fixtures/dish2_menu.json` - 補充菜品資料
- `backend/fixtures/drink_menu.json` - 飲品資料（鐵觀音茶、葡萄酒等）
- `backend/fixtures/drink2_menu.json` - 補充飲品資料

### 前端素材

- `frontend/src/assets/` - AI 主廚圖示、廚師照片、菜品示意圖
- `frontend/src/i18n/*.json` - 三語言翻譯文案資源

### 語言資源說明

- `zh-HK.json` - 繁體中文（香港）**當前使用版本**
- `zh-HK-clean.json` - 繁體中文（香港）備用/清理版（用於資料合併腳本）
- `zh.json` - 簡體中文
- `en.json` - 英文

---

## 🧪 測試與驗證

```bash
# 後端測試
cd backend
python manage.py test

# 測試 AI 對話功能
python test_ai_chat.py

# 前端構建測試
cd frontend
npm run build
npm run preview
```

---

## 🚀 部署建議

1. **資料庫升級**：切換至 MySQL / PostgreSQL，設定連線池 (`CONN_MAX_AGE=600`)
2. **安全性配置**：
   - 關閉 `DEBUG=0`
   - 設定 `ALLOWED_HOSTS`
   - 限制 `CORS_ALLOWED_ORIGINS`
   - 使用環境變數或 Secret Manager 管理敏感資訊
3. **靜態檔案**：執行 `python manage.py collectstatic`
4. **後端服務**：使用 Gunicorn / uWSGI + Nginx
5. **前端部署**：`npm run build` 後部署至 CDN 或靜態伺服器
6. **媒體儲存**：建議使用 AWS S3 / Azure Blob 等物件儲存服務

---

## 🧰 常見問題

**Q: DashScope API 回應格式變更怎麼辦？**

A: `AIChefChatView` 已實作備援邏輯，支援 `output.text` 與 `output.choices` 兩種格式。如仍失敗，請檢查回應日誌並更新解析邏輯。

**Q: 出現 CORS 錯誤**

A: 開發環境已允許所有來源。生產環境請在 `settings.py` 中設定 `CORS_ALLOWED_ORIGINS`。

**Q: SQLite 資料庫鎖定錯誤**

A: SQLite 不適合多執行緒/多程序環境，建議切換至 MySQL 或 PostgreSQL。

**Q: 媒體檔案無法顯示**

A: 確認 Vite proxy 配置正確，或在生產環境使用獨立物件儲存服務。

**Q: AR 功能無法使用**

A: AR 功能需要 HTTPS 環境或 localhost。檢查瀏覽器是否支援 WebGL 和攝影機權限。

**Q: 語言切換後部分文字未翻譯**

A: 檢查 `i18n/*.json` 是否包含對應的翻譯鍵值。確保所有語言檔案的鍵值結構一致。

---

## 📄 授權與聲明

本專案僅供 Hackathon 示範與學習用途，不代表國泰航空官方產品。

- 所有營養與健康資訊僅供參考，非專業醫療建議
- AI 生成內容可能存在錯誤，請謹慎參考
- 歡迎 Fork 並擴充功能（RAG、會員系統、支付整合等）

---

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request！

主要改進方向：

- 🔍 整合 RAG (Retrieval-Augmented Generation) 提升 AI 回答準確度
- 👤 完善會員系統與權限管理
- 💳 整合支付與積分兌換功能
- 📊 增加數據分析與報表功能
- 🌍 擴展更多語言支援
- ♿ 提升無障礙功能 (A11y)

---

## 📧 聯絡資訊

專案維護：CathyHackathon Team

技術支援：請透過 GitHub Issues 提問

---

**Built with ❤️ for Cathay Pacific Hackathon**
