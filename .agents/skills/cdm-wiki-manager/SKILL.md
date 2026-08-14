---
name: cdm-wiki-manager
description: >-
  FINOS Common Domain Model (CDM) LLM-Wiki のライフサイクル操作（Query回答時の自動ナレッジ還元、Ingest一次ソース取り込み、Lint整合性監査、Frontmatter検証、index.md/log.md更新）を実行する際に使用するスキル。
---

# CDM LLM-Wiki Manager スキル

本スキルは、`cdm_wiki/` 内に蓄積される FINOS CDM に関する持続的ナレッジベース（Karpathy 式 LLM-Wiki）を管理・維持・監査するための標準作業手順書（SOP）です。

---

## 🎯 主要ワークフロー

### 1. Query ワークフロー（質問回答 & 自動ナレッジ還元）
ユーザーからの質問に回答する際、新しい知見やマッピング関係が得られた場合は**回答の出力と同時に Wiki へ即座に反映**します。

1. **ナレッジ参照**:
   - [index.md](../../../cdm_wiki/index.md) を読み、既存の関連ページを特定する。
   - 該当する Wiki ページや一次ソース（`common-domain-model/`）を確認する。
2. **回答作成 & 還元内容の決定**:
   - 質問に対する回答を構成する。
   - 回答に含まれる新しい概念・構造・マッピング知見（例: FpML ↔ CDM 対応、Bounded Context 定義、型関係）を Wiki に還元する方針を決める。
3. **Wiki ページの作成または更新**:
   - 既存ページ（例: `concepts/`, `entities/`, `functions/`）へセクション追記、または新規ページを作成。
   - YAML Frontmatter（`last_updated`、`tags`、`sources`）を適切に更新。
4. **カタログ & ログの更新**:
   - 新規ページを作成した場合は [index.md](../../../cdm_wiki/index.md) にリンクと1行要約を追記。
   - [log.md](../../../cdm_wiki/log.md) に以下のフォーマットで履歴を追記：
     ```markdown
     ## [YYYY-MM-DD] query | <質問の件名または還元の概要>
     - <実施内容の箇条書き>
     ```
5. **整合性バリデーション実行**:
   - スクリプト [validate_wiki.py](./scripts/validate_wiki.py) を実行してエラーがないことを確認。

---

### 2. Ingest ワークフロー（一次ソース取り込み）
新しいドキュメントや Rosetta DSL ソースを取り込む手順：

1. **一次ソース確認**:
   - [CDM_INDEX.md](../../../cdm_wiki/CDM_INDEX.md) を参照し、対象の `.rosetta` や Java モジュールを特定。
2. **ソース要約ページの作成**:
   - `cdm_wiki/sources/<source_name>.md` を作成。
   - Frontmatter テンプレートに従ってメタデータを付与。
3. **概念・型の統合**:
   - `concepts/` や `entities/` に新しい定義・知見を反映。
4. **index.md / log.md 更新 & バリデーション**:
   - [index.md](../../../cdm_wiki/index.md) に追加し、[log.md](../../../cdm_wiki/log.md) に `## [YYYY-MM-DD] ingest | <タイトル>` を記録。
   - `python .agents/skills/cdm-wiki-manager/scripts/validate_wiki.py` を実行。

---

### 3. Lint / 監査ワークフロー（健全性チェック）
Wiki の品質・整合性を維持するための自動監査手順：

1. **バリデータスクリプトの実行**:
   ```bash
   python .agents/skills/cdm-wiki-manager/scripts/validate_wiki.py
   ```
2. **検証項目**:
   - 全コンテンツページの YAML Frontmatter 妥当性（必須キー、有効なカテゴリ名、日付形式）。
   - すべての Markdown 相対リンクの実在性（Wiki 内リンクおよび CDM ソース参照リンク）。
   - [index.md](../../../cdm_wiki/index.md) の登録漏れ（孤立ページ）および壊れたリンク。
   - [log.md](../../../cdm_wiki/log.md) のエントリ形式およびアクション種別。
3. **ログ記録**:
   - 監査結果を [log.md](../../../cdm_wiki/log.md) に追記（`## [YYYY-MM-DD] lint | Checked N pages, zero errors`）。

---

## 📋 ページ作成・編集規約

### YAML Frontmatter 規格
すべてのコンテンツページ（`sources/`, `overview/`, `concepts/`, `entities/`, `functions/`）はファイルの先頭に以下を含める必要があります：

```yaml
---
title: "ページタイトル"
category: "concepts" # sources | overview | concepts | entities | functions のいずれか（親ディレクトリと一致）
sources:
  - "../CDM_INDEX.md"
last_updated: "YYYY-MM-DD"
tags: [cdm, rosetta, derivatives, tag_name]
---
```

### ハイパーリンク規格
- 必ず Markdown 相対リンクを使用します（例: `[TradeState](../entities/core_data_types.md)` または `[product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)`）。
- アンカー付きリンクもサポートされます（例: `[決済条件](../concepts/product_modeling.md#2-決済条件)`）。

---

## 🚫 不可変性の原則
- `common-domain-model/` ディレクトリ配下のソースコードおよび DSL ファイルは**一次情報（Raw Source）**であり、Wiki 操作や質問回答においてエージェントが直接編集してはなりません。
