# FINOS Common Domain Model (CDM) LLM-Wiki

`cdm_workspace/cdm_wiki/` へようこそ。

本 Wiki は、[FINOS Common Domain Model (CDM)](CDM_INDEX.md) に関する知識を蓄積・維持するための AI 管理型ナレッジベースです。[Andre Karpathy 氏の LLM Wiki 構想](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) に基づいて構築されています。

---

## 🤖 重要: AI エージェント向け指示事項（Antigravity IDE ハーネス）

> [!IMPORTANT]
> 本ワークスペースで Wiki 操作（ソース取り込み、質問回答、または整合性チェック）を行う際：
> 1. **Wiki 規約**: Wiki の構造、Frontmatter 規格、運用フローについては、必ず [SCHEMA.md](SCHEMA.md) を事前に確認してください。
> 2. **ソースコード探索**: `../common-domain-model/` 内のソースコードや Rosetta DSL ファイルを探索する際は、必ず [CDM_INDEX.md](CDM_INDEX.md) を一次ナビゲーションインデックスとして利用してください。
> 3. **メンテナンスルール**: ページの作成・更新を行った際は、必ず [index.md](index.md) を更新し、[log.md](log.md) に操作履歴を追記してください。

---

## 🗺️ ナビゲーション

- **[CDM_INDEX.md](CDM_INDEX.md)**: FINOS CDM 総合ナビゲーションガイド・目次。
- **[index.md](index.md)**: すべてのページをカテゴリ別に整理したカタログ（直接リンクと1行要約）。
- **[log.md](log.md)**: 情報取り込み、質問回答、整合性チェックの時系列ログ。
- **[SCHEMA.md](SCHEMA.md)**: Wiki の分類定義、フォーマット規格、運用手順書。

### ナレッジカテゴリ構成

| サブディレクトリ | 内容 | 主要エントリページ |
|---|---|---|
| **`sources/`** | 取り込み済み一次ソースの要約 | [cdm_index_source.md](sources/cdm_index_source.md) |
| **`overview/`** | システム全体アーキテクチャ・Rosetta DSL ↔ Java 対応法則 | [cdm_architecture.md](overview/cdm_architecture.md) |
| **`concepts/`** | デリバティブ商品モデル、ライフサイクル、法的契約、FpML・金利 | [product_modeling.md](concepts/product_modeling.md), [event_lifecycle.md](concepts/event_lifecycle.md) |
| **`entities/`** | 主要 Rosetta データ型・インターフェースのリファレンス | [core_data_types.md](entities/core_data_types.md) |
| **`functions/`** | Rosetta 関数（`func`）、適格性判定・計算ロジック | [qualification_and_calculation.md](functions/qualification_and_calculation.md) |

---

## 💡 人間（ユーザー）の活用方法

1. **閲覧・検索**: [index.md](index.md) から特定のドメインやトピックのページを探して閲覧します。
2. **質問**: AI エージェントに CDM の商品構造やイベント、コード設計に関する質問を投げかけます。エージェントは Wiki を参照して回答を作成し、得られた新しい知見を Wiki に還元します。
3. **新規ソースの取り込み**: 新しい文書やコードパスを指示し、エージェントに Wiki への取り込み（Ingest）を命じます。
