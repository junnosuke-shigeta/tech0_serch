#!/usr/bin/env python3
# ─────────────────────────────────────────────
# seed_data.py — DB初期化＋サンプルデータ投入
#
# 【使い方】
#   python3 seed_data.py
#
# 実行すると:
#   1. tech0_search.db を作成（なければ）
#   2. pages テーブルを作成（なければ）
#   3. サンプルデータ30件を投入
# ─────────────────────────────────────────────

import sqlite3
import os

DB_PATH = os.environ.get("SQLITE_PATH", "tech0_search.db")

SAMPLE_PAGES = [
    # (title, url, body)
    ("DX推進の基礎",              "https://techzeron.example.com/dx-basics",       "デジタルトランスフォーメーション（DX）の基礎知識。業務プロセスのデジタル化から始める第一歩。"),
    ("DXリテラシー研修資料",      "https://techzeron.example.com/dx-training",     "全社員向けDXリテラシー研修の資料。データ活用・AI・クラウドの基本を学ぶ。"),
    ("社内ポータル利用ガイド",    "https://techzeron.example.com/portal-guide",    "社内ポータルの使い方。ドキュメント検索・申請・掲示板の操作方法。"),
    ("製造部門 業務マニュアル",   "https://techzeron.example.com/manuf-manual",    "製造ラインの標準作業手順書。品質管理・安全基準・設備点検の手順。"),
    ("営業支援ツール操作手順",    "https://techzeron.example.com/sales-tool",      "CRMシステムの操作手順。顧客情報の登録・商談管理・レポート出力。"),
    ("AI活用事例集",              "https://techzeron.example.com/ai-cases",        "社内AI活用プロジェクトの事例集。画像検査自動化・需要予測・チャットボット導入事例。"),
    ("クラウド移行ガイドライン",  "https://techzeron.example.com/cloud-guideline", "オンプレシステムのクラウド移行方針。Azure利用基準・セキュリティポリシー。"),
    ("情報セキュリティ規程",      "https://techzeron.example.com/security-policy", "情報資産の管理規程。機密情報の取り扱い・インシデント報告フロー。"),
    ("Python研修テキスト",        "https://techzeron.example.com/python-training", "社員向けPython入門研修テキスト。データ分析・自動化スクリプトの基礎。"),
    ("データ分析入門",            "https://techzeron.example.com/data-analysis",   "Excel・Pythonを使ったデータ分析手法。可視化・集計・予測モデルの基礎。"),
    ("財務報告書 2024年度",       "https://techzeron.example.com/finance-2024",    "2024年度の財務報告書。売上高・利益・設備投資・キャッシュフロー。"),
    ("人事制度ガイドブック",      "https://techzeron.example.com/hr-guide",        "評価制度・等級制度・給与体系・昇進基準の解説。"),
    ("テレワーク規程",            "https://techzeron.example.com/telework",        "在宅勤務・テレワークの申請手順・セキュリティルール・費用補助。"),
    ("新入社員オンボーディング",  "https://techzeron.example.com/onboarding",      "入社後最初の3ヶ月のガイド。社内システム登録・研修スケジュール・メンター制度。"),
    ("プロジェクト管理ガイド",    "https://techzeron.example.com/pj-guide",        "プロジェクト立案・WBS作成・進捗管理・リスク管理の手法。"),
    ("品質管理マニュアル",        "https://techzeron.example.com/quality",         "製品品質の管理基準。ISO認証・検査プロセス・不良品対応フロー。"),
    ("環境・SDGs取り組み",        "https://techzeron.example.com/sdgs",            "テクゼロン社のSDGsへの取り組み。CO2削減・廃棄物削減・再生可能エネルギー導入。"),
    ("技術開発ロードマップ",      "https://techzeron.example.com/tech-roadmap",    "次世代製品・技術の開発計画。R&D投資方針・特許戦略・産学連携。"),
    ("社内FAQ",                   "https://techzeron.example.com/faq",             "よくある質問集。給与・有給・福利厚生・社内手続き・IT機器申請。"),
    ("コンプライアンス研修",      "https://techzeron.example.com/compliance",      "法令遵守・ハラスメント防止・インサイダー取引規制の研修資料。"),
    ("購買・調達手続き",          "https://techzeron.example.com/procurement",     "物品購入・外注発注の申請フロー。見積もり取得・稟議書作成・契約手続き。"),
    ("IT機器申請ガイド",          "https://techzeron.example.com/it-request",      "PC・スマートフォン・周辺機器の申請・更新・廃棄の手続き。"),
    ("グローバル展開戦略",        "https://techzeron.example.com/global",          "海外市場への展開計画。アジア・欧米・新興国市場の事業戦略。"),
    ("社内イントラネット案内",    "https://techzeron.example.com/intranet",        "社内イントラネットの利用方法。メール・カレンダー・Teams・SharePoint。"),
    ("健康経営推進計画",          "https://techzeron.example.com/health",          "従業員の健康増進施策。健康診断・メンタルヘルス・ウォーキングイベント。"),
    ("生産性向上ツール集",        "https://techzeron.example.com/productivity",    "業務効率化ツールの一覧。RPA・AI・BI・コラボレーションツールの活用事例。"),
    ("知的財産管理規程",          "https://techzeron.example.com/ip",              "特許・商標・著作権の管理規程。発明届・外部開示審査・ライセンス管理。"),
    ("BCP（事業継続計画）",       "https://techzeron.example.com/bcp",             "災害・システム障害・パンデミック時の事業継続計画。緊急連絡網・復旧手順。"),
    ("社内研修カレンダー",        "https://techzeron.example.com/training-cal",    "年間の研修・セミナー・勉強会のスケジュール一覧。"),
    ("採用・面接ガイドライン",    "https://techzeron.example.com/recruitment",     "採用プロセス・面接評価基準・オファー提示の手順。"),
]


def init_db():
    """DBを初期化してサンプルデータを投入する"""
    print(f"📂 DB: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ── テーブル作成 ──
    cur.executescript(open("schema.sql", encoding="utf-8").read())
    print("✅ テーブル作成完了")

    # ── サンプルデータ投入 ──
    inserted = 0
    skipped  = 0
    for title, url, body in SAMPLE_PAGES:
        try:
            cur.execute(
                "INSERT INTO pages (title, url, body) VALUES (?, ?, ?)",
                (title, url, body),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            # UNIQUE 制約違反（URL重複）→ スキップ
            skipped += 1

    conn.commit()
    conn.close()

    print(f"✅ サンプルデータ投入: {inserted}件追加 / {skipped}件スキップ（重複）")
    print(f"✅ 完了！ '{DB_PATH}' に {inserted + skipped} 件のデータがあります")
    print()
    print("次のステップ:")
    print("  uvicorn main:app --reload")
    print("  → http://localhost:8000/docs でAPIを確認")


if __name__ == "__main__":
    init_db()
