// ─────────────────────────────────────────────
// ResultCard コンポーネント
// 対応仕様設計書: §2.4
//   props: id, title, url
// ─────────────────────────────────────────────

import { SearchResult } from "@/types";

type Props = {
  result: SearchResult;
};

export default function ResultCard({ result }: Props) {
  return (
    <div className="result-card">
      <a href={result.url} target="_blank" rel="noopener noreferrer">
        {result.title}
      </a>
      <p className="result-url">{result.url}</p>
    </div>
  );
}
