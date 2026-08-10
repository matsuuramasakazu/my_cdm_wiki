# CDM LLM-Wiki 時系列操作ログ (`log.md`)

本ファイルは、CDM LLM-Wiki に対して行われたすべての操作（取り込み、質問回答、メンテナンス）を時系列順に記録するログです。CLI ツール等（例: `grep "^## \[" log.md`）でパースしやすいよう統一フォーマットを使用しています。

---

## [2026-08-09] setup | CDM LLM-Wiki 環境の初期化
- `SCHEMA.md` を作成し、3層アーキテクチャ、分類体系、YAML Frontmatter 規格、LLM 運用手順を定義。
- `.agents/AGENTS.md` に Antigravity IDE ハーネスを設定（Wiki 操作時の `README.md`/`SCHEMA.md` 参照義務、ソース探索時の `CDM_INDEX.md` 参照義務）。
- `README.md`, `index.md`, `log.md` の初期作成。

## [2026-08-09] ingest | CDM_INDEX.md および初期ドメイン構造の取り込み
- 一次情報 `../common-domain-model/CDM_INDEX.md` をインジェスト。
- 以下の初期 Wiki ページ群を生成：
  - `sources/cdm_index_source.md`
  - `overview/cdm_architecture.md`
  - `concepts/product_modeling.md`
  - `concepts/event_lifecycle.md`
  - `concepts/fpml_ingestion.md`
  - `concepts/legal_and_margin.md`
  - `concepts/observables_and_rates.md`
  - `entities/core_data_types.md`
  - `functions/qualification_and_calculation.md`
- すべてのページを `index.md` カタログに登録。

## [2026-08-10] refactor | CDM_INDEX.md の配置場所変更
- `common-domain-model/CDM_INDEX.md` を `cdm_wiki/CDM_INDEX.md` 直下に移設。
- `CDM_INDEX.md` 内部の相対パス（Rosetta/Javaソースへの参照）を `../common-domain-model/` 経由に修正。
- 移設ファイルを参照する全 Wiki ページ (`SCHEMA.md`, `README.md`, `index.md`, 各サブディレクトリドキュメント) の相対パス参照を `CDM_INDEX.md` / `../CDM_INDEX.md` に更新。

## [2026-08-10] query | FpML ↔ CDM 相互変換機能および金利スワップ TradeState マッピング知見の反映
- `concepts/fpml_ingestion.md` を更新し、CDM に標準組み込みの FpML Ingestion 機能と、標準非提供の Export/Projection 仕様（カスタム実装が必要である旨）および金利スワップ (IRS) の `TradeState` ↔ FpML ノード対応表を記録・保存。
- `index.md` の該当ページ要約文を更新。
- 事実誤認（CDM 標準での Export サポート）に関する Wiki 記述の訂正を実施。


