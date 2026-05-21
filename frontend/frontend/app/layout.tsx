// ─────────────────────────────────────────────
// layout.tsx — ルートレイアウト
// ─────────────────────────────────────────────
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tech0 Search",
  description: "テクゼロン社 社内検索エンジン",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
