# ─────────────────────────────────────────────
# main.py — FastAPI アプリケーション
# 対応仕様設計書: §3.1, §3.2, §3.3
#
# 起動コマンド（ローカル開発）:
#   uvicorn main:app --reload
#
# 確認:
#   http://localhost:8000/docs        → Swagger UI
#   http://localhost:8000/api/search?q=DX → 検索テスト
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

# ── CORS 設定（仕様設計書 §3.3）────────────────
# Next.js（フロントエンド）からのリクエストを許可する。
# 開発: http://localhost:3000
# 本番: Azure Static Web Apps の URL
#
# CORS_ORIGINS 環境変数でカンマ区切りに複数指定可能。
_raw_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:3000",          # デフォルト: ローカル開発
)
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
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
    キーワード検索エンドポイント（仕様設計書 §3.2）

    - Must  : q でタイトルを LIKE 検索
    - 発展  : full=true で本文（body）も検索
    - 結果  : 関連度順（FR-004）

    Returns:
        200: {"query": str, "results": [...], "total": int}
        400: {"error": "q parameter is required"}
        500: {"error": "Internal server error: ..."}
    """
    # バリデーション（仕様設計書 §3.2 エラー(400)）
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
        # 本番では詳細エラーを返さない方が良いが、学習目的のため表示する
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"},
        )
