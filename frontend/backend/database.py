# ─────────────────────────────────────────────
# database.py — DB接続の抽象化
# 対応仕様設計書: §4.1
#
# USE_MYSQL 環境変数で SQLite / Azure MySQL を切り替える
#   USE_MYSQL=false（デフォルト）→ SQLite（ローカル開発）
#   USE_MYSQL=true               → Azure DB for MySQL（本番）
#
# ★ここが「DBだけ変わってAPIは変わらない」設計のポイント★
# main.py は get_connection() を呼ぶだけで、
# 接続先がどちらでも同じコードが動く。
# ─────────────────────────────────────────────

import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()  # .env ファイルを読み込む

USE_MYSQL: bool = os.environ.get("USE_MYSQL", "false").lower() == "true"


def get_connection():
    """
    環境変数 USE_MYSQL の値に応じて接続先を切り替える。

    Returns:
        SQLite の場合: sqlite3.Connection（row_factory=sqlite3.Row）
        MySQL の場合:  pymysql.Connection（DictCursor）
    """
    if USE_MYSQL:
        return _get_mysql_connection()
    else:
        return _get_sqlite_connection()


def _get_sqlite_connection() -> sqlite3.Connection:
    """
    SQLite 接続（ローカル開発用）
    対応仕様設計書: §4.1 開発環境
    """
    db_path = os.environ.get("SQLITE_PATH", "tech0_search.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # カラム名でアクセスできるようにする
    return conn


def _get_mysql_connection():
    """
    Azure DB for MySQL 接続（本番用）
    対応仕様設計書: §4.1 本番環境
    必要な環境変数: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
    """
    try:
        import pymysql
    except ImportError:
        raise ImportError(
            "pymysql が見つかりません。'pip install pymysql' を実行してください。"
        )

    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise EnvironmentError(
            f"以下の環境変数が設定されていません: {', '.join(missing)}\n"
            f".env ファイルまたは環境変数を確認してください。"
        )

    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl_disabled": False},          # Azure MySQL は SSL 必須
        connect_timeout=10,
    )


def get_db_type() -> str:
    """現在の接続先を返す（デバッグ・ログ用）"""
    return "MySQL (Azure)" if USE_MYSQL else "SQLite (Local)"
