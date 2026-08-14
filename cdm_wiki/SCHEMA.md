# CDM LLM-Wiki スキーマ & 運用ガイドライン (`SCHEMA.md`)

本ドキュメントは、`cdm_workspace/cdm_wiki/` に配置された FINOS Common Domain Model (CDM) LLM-Wiki の構造、分類体系、ファイル規約、および運用ワークフローを規定します。

---

## 1. 3層アーキテクチャ

1. **Raw Sources (一次情報・不可変)**:
   - ルートパス: `../common-domain-model/`
   - 一次ナビゲーションガイド: `../common-domain-model/` 内のすべての探索は [CDM_INDEX.md](CDM_INDEX.md) に従って行わなければならない。
   - エージェントは Wiki 操作時に `../common-domain-model/` 内のファイルを直接変更してはならない。

2. **The Wiki (持続的・蓄積型ナレッジ)**:
   - ルートパス: `./` (`cdm_workspace/cdm_wiki/`)
   - LLM エージェントが維持・管理する構造化された Markdown ファイル群。
   - サブディレクトリ（`sources/`, `overview/`, `concepts/`, `entities/`, `functions/`）に整理・格納される。

3. **The Schema (本規定)**:
   - 配置場所: `SCHEMA.md`
   - LLM エージェントが Wiki を更新・維持する標準作業手順書（SOP）。

---

## 2. ディレクトリ分類体系 & ファイル命名規則

```
cdm_wiki/
├── CDM_INDEX.md                    # 総合ナビゲーションガイド・目次
├── SCHEMA.md                       # Wiki 規約・構造定義・ワークフロー（本書）
├── README.md                       # 概要・利用ガイドおよびエージェント通知
├── index.md                        # コンテンツカタログ（リンクと1行要約）
├── log.md                          # 時系列操作ログ
├── sources/                        # 取り込み済み一次情報の要約
│   └── cdm_index_source.md
├── overview/                       # 全体アーキテクチャ・フレームワーク解説
│   └── cdm_architecture.md
├── concepts/                       # ドメイン概念・ライフサイクル規則
│   ├── product_modeling.md
│   ├── event_lifecycle.md
│   ├── fpml_ingestion.md
│   ├── legal_and_margin.md
│   └── observables_and_rates.md
├── entities/                       # 主要 Rosetta データ型・型定義リファレンス
│   └── core_data_types.md
└── functions/                      # 計算ロジック・適格性判定・マッピング関数
    └── qualification_and_calculation.md
```

- **ファイル命名規約**: `snake_case.md`（小文字＋アンダースコア）を使用（例: `product_modeling.md`）。
- **YAML Frontmatter 規約**: すべての Wiki ページは先頭に以下のメタデータを記述しなければならない：
  ```yaml
  ---
  title: "ページタイトル"
  category: "concepts" # sources | overview | concepts | entities | functions
  sources:
    - "CDM_INDEX.md"
  last_updated: "2026-08-09"
  tags: [cdm, rosetta, derivatives]
  ---
  ```
- **ハイパーリンク規約**:
  - **ローカル相対リンク**: 相対パスを使用した Markdown リンク（例: `[product-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)`）を記述する。
  - **外部 URL 接続確認（絶対ルール）**: 外部 URL（`https://...`）を掲載する際は、必ず事前に HTTP リクエスト等で疎通確認（200 OK）を行い、有効性が確認された URL のみを掲載しなければならない。リンター `validate_wiki.py` にて自動検証される。

---

## 3. 主要運用ワークフロー

### 3.1 Ingest ワークフロー（一次情報取り込み）
新しいソースドキュメントやコードベースを取り込む手順：
1. **ソース確認**: [CDM_INDEX.md](CDM_INDEX.md) を参照し、対象の `.rosetta` ファイルや Java モジュールを特定・確認する。
2. **ソース要約ページの作成**: `sources/<source_name>.md` に要約ページを作成する。
3. **知識の統合・更新**: 既存の `entities/`, `concepts/`, `overview/` ページを更新し、新しい概念があればページを新設する。関連ページ間の相互リンクを確実に更新する。
4. **インデックス更新**: [index.md](index.md) に新設ページを追加し、1行要約を記述する。
5. **ログ追記**: [log.md](log.md) に以下のフォーマットで操作記録を追記する：
   `## [YYYY-MM-DD] ingest | <ソースのタイトル>`

### 3.2 Query ワークフロー（検索・回答・知識還元）
ユーザーからの質問に回答する手順：
1. **インデックス参照**: [index.md](index.md) を読み、関連する Wiki ページを特定する。
2. **詳細確認**: 関連する Wiki ページ（必要に応じて一次情報ファイル）を読み込む。
3. **回答合成**: 根拠を明示しながら回答を作成する。
4. **自動Wiki還元義務**: 質問への回答を通じて得られた新しい知見・マッピング・構造の比較分析は、ユーザーへ回答を出力するのと同時に、必ず `cdm_wiki/`（`concepts/` や `entities/` 等）へ即座に反映・保存しなければならない。
5. **カタログ・ログ更新**: 新規作成・更新したページを [index.md](index.md) に反映し、[log.md](log.md) に以下のフォーマットで追記する：
   `## [YYYY-MM-DD] query | <質問の件名>`

### 3.3 Lint ワークフロー（整合性・健全性チェック）
定期的に Wiki の品質を自動監査する手順：
1. **自動バリデータの実行**:
   ```bash
   python ../.agents/skills/cdm-wiki-manager/scripts/validate_wiki.py
   ```
2. **検証項目**:
   - **リンク切れチェック**: `index.md` や各ページの相対リンクが実在するか自動検証。
   - **孤立ページ検出**: `index.md` に登録されていないコンテンツページがないか検出。
   - **Frontmatter 検証**: 必須キー（`title`, `category`, `sources`, `last_updated`, `tags`）および親ディレクトリとのカテゴリ一致を検証。
   - **フォーマット検証**: `log.md` のアクション・日付形式の整合性を検証。
3. **ログ追記**: チェック結果を [log.md](log.md) に追記する：
   `## [YYYY-MM-DD] lint | Checked N pages, zero errors`
