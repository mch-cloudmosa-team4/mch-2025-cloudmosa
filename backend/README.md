
# CloudMosa Backend

A FastAPI-based backend server with modular architecture for the CloudMosa project.

## 快速開始

### Requirements
- Python 3.12 or above
- [uv](https://github.com/astral-sh/uv) package manager

### Install Dependencies

```bash
uv sync
```

### Start the Server

```bash
uv run fastapi dev main.py
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API 端點

- **根端點**: `http://127.0.0.1:8000/` - 基本 API 資訊
- **API 文檔**: `http://127.0.0.1:8000/docs` - 自動生成的 Swagger 文檔  
- **健康檢查**: `http://127.0.0.1:8000/api/v1/health` - 服務健康狀態
- **範例 CRUD**: `http://127.0.0.1:8000/api/v1/items` - 完整的 CRUD 操作範例

## 專案架構

### 目錄結構

```
backend/
├── main.py              # FastAPI 應用入口
├── app/
│   ├── config.py        # 配置管理
│   ├── dependencies.py  # 依賴注入
│   ├── models/          # 數據模型
│   ├── router/          # API 路由
│   ├── schemas/         # 請求/回應 Schema
│   ├── utils/           # 工具函數
│   └── crud/            # 數據庫操作 (預留)
```

### 架構特點

- **模組化設計**: 按功能分離不同模組
- **配置管理**: Pydantic Settings，支援環境變數
- **API 設計**: RESTful 風格，自動生成文檔
- **依賴注入**: FastAPI 原生系統，可重用組件
- **錯誤處理**: 全域異常處理，標準化回應

## 擴展建議

後續開發可以考慮添加：

- **資料庫整合**: SQLAlchemy/Tortoise ORM 
- **認證授權**: JWT Token、用戶管理
- **快取機制**: Redis 集成
- **測試框架**: pytest 測試配置  
- **部署配置**: Docker 容器化

## 技術棧

- **Framework**: FastAPI
- **Python**: 3.12+
- **Package Manager**: uv
- **Configuration**: Pydantic Settings

這個架構提供了堅實的基礎，可以根據需求進行擴展。
