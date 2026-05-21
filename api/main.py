# ─────────────────────────────────────────────
# main.py — FastAPI アプリケーション（完全版）
# Azure Functions Flex Consumption + Next.js 対応
# ─────────────────────────────────────────────

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import get_db_type
from search import search_pages

load_dotenv()

# ── FastAPI インスタンス ─────────────────────
app = FastAPI(
    title="Tech0 Search API",
    description="テクゼロン社 社内検索エンジン — バックエンドAPI",
    version="1.0.0",
)

# ── CORS 設定（Flex Consumption では必須）───────
_raw_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:3000",  # デフォルト: ローカル開発
)
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],      # ← OPTIONS を含めて全許可
    allow_headers=["*"],
)

# ── エンドポイント ───────────────────────────

@app.get("/")
def root():
    """ヘルスチェック用"""
    return {
        "service": "Tech0 Search API",
        "status": "ok",
        "db": get_db_type(),
    }


@app.get("/api/search")
def search(
    q: str = Query(default="", description="検索キーワード"),
    full: bool = Query(default=False, description="True にすると本文も検索（発展課題）"),
):
    """
    キーワード検索エンドポイント
    """
    if not q.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "q parameter is required"},
        )

    try:
        results = search_pages(keyword=q.strip(), include_body=full)
        return {
            "query":   q.strip(),
            "results": results,
            "total":   len(results),
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"},
        )
