"use client";

// ─────────────────────────────────────────────
// SearchBox コンポーネント
// 対応仕様設計書: §2.4
//   - state: query (string)
//   - state: loading (boolean)
//   - event: onSearch() → 親にクエリを渡す
// ─────────────────────────────────────────────

type Props = {
  onSearch: (query: string) => void;
  loading: boolean;
};

export default function SearchBox({ onSearch, loading }: Props) {
  return (
    <div className="search-box">
      <input
        id="search-input"
        type="text"
        placeholder="キーワードを入力..."
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            onSearch((e.target as HTMLInputElement).value.trim());
          }
        }}
      />
      <button
        onClick={() => {
          const input = document.getElementById("search-input") as HTMLInputElement;
          onSearch(input.value.trim());
        }}
        disabled={loading}
      >
        {loading ? "検索中..." : "検索"}
      </button>
    </div>
  );
}
