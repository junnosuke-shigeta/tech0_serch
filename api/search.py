# ─────────────────────────────────────────────
# search.py — 検索ロジック
# 対応仕様設計書: §3.2 GET /api/search
#
# Must  : タイトルの LIKE 検索（FR-004: 関連度順）
# 発展  : 本文（body）も含めた全文検索
# ─────────────────────────────────────────────

from database import get_connection


def search_pages(keyword: str, include_body: bool = False) -> list[dict]:
    """
    キーワードでページを検索して返す。

    Args:
        keyword:      検索キーワード
        include_body: True にすると本文（body）も検索対象に含める（発展課題）

    Returns:
        [{"id": 1, "title": "...", "url": "..."}, ...]
        関連度順（タイトル一致を上位に）でソートされる（FR-004）
    """
    conn = get_connection()

    try:
        # ── Must: タイトル検索 ──────────────────────────
        # SQLite と MySQL で LIKE の動作がほぼ同じなので共通クエリが使える。
        # ただし MySQL の場合は照合順序（utf8mb4_unicode_ci）に依存する。
        if include_body:
            # 発展: タイトル OR 本文を検索
            sql = """
                SELECT id, title, url,
                    CASE WHEN title LIKE ? THEN 2 ELSE 1 END AS score
                FROM pages
                WHERE title LIKE ? OR body LIKE ?
                ORDER BY score DESC, id ASC
            """
            params = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        else:
            # Must: タイトルのみ検索（FR-004: 完全一致を上位に）
            sql = """
                SELECT id, title, url,
                    CASE
                        WHEN title = ?        THEN 3
                        WHEN title LIKE ?     THEN 2
                        ELSE 1
                    END AS score
                FROM pages
                WHERE title LIKE ?
                ORDER BY score DESC, id ASC
            """
            exact  = keyword
            prefix = f"{keyword}%"
            like   = f"%{keyword}%"
            params = (exact, prefix, like)

        # ── SQLite / MySQL 共通の実行方法 ───────────────
        # SQLite:  ? プレースホルダー、fetchall() → sqlite3.Row
        # MySQL:   %s プレースホルダー、fetchall() → dict
        #
        # 両方に対応するため MySQL 接続時は ? → %s に置換する
        import os
        if os.environ.get("USE_MYSQL", "false").lower() == "true":
            sql = sql.replace("?", "%s")

        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        # sqlite3.Row は dict に変換しておく（JSON シリアライズのため）
        results = []
        for row in rows:
            if isinstance(row, dict):
                results.append({"id": row["id"], "title": row["title"], "url": row["url"]})
            else:
                results.append({"id": row["id"], "title": row["title"], "url": row["url"]})

        return results

    finally:
        conn.close()
