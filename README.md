# Tech0 Search — サンプルコード

PROJECT ZERO / Step3-1 — マイクロサービス版 社内検索エンジン

```
frontend/   Next.js (TypeScript)  ← UIレイヤー
backend/    FastAPI   (Python)    ← APIレイヤー
```

## 全体アーキテクチャ

```
ブラウザ → Next.js → FastAPI → SQLite（開発）
                            → Azure DB for MySQL（本番）
```

## クイックスタート

**リリース手順書** を参照してください。
ステップごとの手順・コード解説・よくあるエラーが記載されています。
