// ─────────────────────────────────────────────
// Tech0 Search — 型定義
// 対応仕様設計書: §2.4, §3.2
// ─────────────────────────────────────────────

/** 検索結果の1件 */
export type SearchResult = {
  id: number;
  title: string;
  url: string;
};

/** /api/search のレスポンス */
export type SearchResponse = {
  query: string;
  results: SearchResult[];
  total: number;
};

/** /api/search のエラーレスポンス */
export type SearchErrorResponse = {
  error: string;
};
