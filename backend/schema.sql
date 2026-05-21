-- ─────────────────────────────────────────────
-- schema.sql — テーブル定義
-- 対応仕様設計書: §4.2
--
-- 【使い方】
--   SQLite（ローカル開発）:
--     python3 seed_data.py  → 自動でスキーマ作成＋サンプルデータ投入
--
--   MySQL（Azure DB for MySQL）:
--     mysql -h <ホスト> -u <ユーザー> -p tech0search < schema_mysql.sql
-- ─────────────────────────────────────────────


-- ════════════════════════════════════════════
-- SQLite 用スキーマ（ローカル開発）
-- ════════════════════════════════════════════

-- pages テーブル（必須）
-- 対応仕様設計書: §4.2 pagesテーブル
CREATE TABLE IF NOT EXISTS pages (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    title      TEXT     NOT NULL,
    url        TEXT     NOT NULL UNIQUE,
    body       TEXT,
    created_at TEXT     DEFAULT (datetime('now', 'localtime'))
);

-- search_logs テーブル（発展課題）
-- 検索クエリと件数を記録する（FR-006）
CREATE TABLE IF NOT EXISTS search_logs (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    query         TEXT     NOT NULL,
    results_count INTEGER  DEFAULT 0,
    searched_at   TEXT     DEFAULT (datetime('now', 'localtime'))
);


-- ════════════════════════════════════════════
-- MySQL 用スキーマ（Azure DB for MySQL）
-- ※ SQLite との主な違いをコメントで明示
-- ════════════════════════════════════════════

-- ★ SQLite との違い①: AUTO_INCREMENT（スペースなし）
-- ★ SQLite との違い②: VARCHAR(N) で長さ指定が必須
-- ★ SQLite との違い③: LONGTEXT で本文の長さ制限を回避
-- ★ SQLite との違い④: ENGINE, CHARSET, COLLATE の指定

-- CREATE TABLE IF NOT EXISTS pages (
--     id         INT          AUTO_INCREMENT PRIMARY KEY,
--     title      VARCHAR(500) NOT NULL,
--     url        VARCHAR(2000) NOT NULL UNIQUE,
--     body       LONGTEXT,
--     created_at DATETIME     DEFAULT CURRENT_TIMESTAMP
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
--
-- CREATE TABLE IF NOT EXISTS search_logs (
--     id            INT          AUTO_INCREMENT PRIMARY KEY,
--     query         VARCHAR(500) NOT NULL,
--     results_count INT          DEFAULT 0,
--     searched_at   DATETIME     DEFAULT CURRENT_TIMESTAMP
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
