"use client";

// ─────────────────────────────────────────────
// Tech0 Search — メイン検索ページ
// 対応仕様設計書: §2.2, §2.3, §2.4
//
// データフロー（仕様設計書 §1.2）:
//   ユーザー入力
//   → handleSearch()
//   → fetch(NEXT_PUBLIC_API_URL/api/search?q=...)
//   → FastAPI → MySQL
//   → setResults() → 画面再描画
// ─────────────────────────────────────────────

import { useState } from "react";
import SearchBox from "./components/SearchBox";
import ResultCard from "./components/ResultCard";
import { SearchResult, SearchResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function SearchPage() {
  // ── State ──────────────────────────────────
  const [results, setResults] = useState<SearchResult[]>([]);
  const [total, setTotal]     = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState<string | null>(null);
  const [lastQuery, setLastQuery] = useState("");

  // ── Handler ────────────────────────────────
  const handleSearch = async (query: string) => {
    if (!query) return;

    setLoading(true);
    setError(null);
    setLastQuery(query);

    try {
      const res = await fetch(
        `${API_URL}/api/search?q=${encodeURIComponent(query)}`
      );

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error ?? `HTTP ${res.status}`);
      }

      const data: SearchResponse = await res.json();
      setResults(data.results);
      setTotal(data.total);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "予期しないエラーが発生しました");
      setResults([]);
      setTotal(null);
    } finally {
      setLoading(false);
    }
  };

  // ── Render ─────────────────────────────────
  return (
    <main>
      {/* ヘッダー */}
      <header>
        <h1>🔍 Tech0 Search</h1>
        <p>テクゼロン社 社内検索エンジン</p>
      </header>

      {/* 検索ボックス (FR-001) */}
      <section className="search-section">
        <SearchBox onSearch={handleSearch} loading={loading} />
      </section>

      {/* 検索結果 (FR-002, FR-003) */}
      <section className="results-section">
        {/* エラー表示 */}
        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}

        {/* 件数表示 */}
        {total !== null && !error && (
          <p className="results-count">
            「{lastQuery}」の検索結果: {total}件
          </p>
        )}

        {/* 結果一覧 (FR-002, FR-003) */}
        {results.length > 0 ? (
          <div className="result-list">
            {results.map((r) => (
              <ResultCard key={r.id} result={r} />
            ))}
          </div>
        ) : (
          total === 0 && (
            <div className="no-results">
              <p>「{lastQuery}」に一致するページは見つかりません</p>
              <p>別のキーワードで試してください</p>
            </div>
          )
        )}
      </section>
    </main>
  );
}
