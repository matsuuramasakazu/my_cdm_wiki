# CDM LLM-Wiki コンテンツカタログ (`index.md`)

本カタログは、CDM LLM-Wiki 内のすべての有効な Wiki ページの一覧を提供します。各エントリには該当ページへの Markdown リンクと1行要約が含まれています。

---

## 1. 規定 & 管理 (Meta & Administration)

- **[CDM_INDEX.md](CDM_INDEX.md)**: CDM 総合ナビゲーションガイド・目次（一次ソースインデックスの直下移設版）。
- **[SCHEMA.md](SCHEMA.md)**: 運用規約、Frontmatter 規格、ディレクトリ分類体系、および LLM 運用ワークフロー。
- **[README.md](README.md)**: 総合ガイドおよび AI エージェント用ハーネス指示書。
- **[log.md](log.md)**: 情報取り込み、質問回答、整合性チェックの時系列操作ログ。

---

## 2. 取り込み済み一次ソース (`sources/`)

- **[cdm_index_source.md](sources/cdm_index_source.md)**: 一次ソース [CDM_INDEX.md](CDM_INDEX.md) およびリポジトリ全体構造の総合要約。
- **[official_external_sources.md](sources/official_external_sources.md)**: FINOS、ISDA、ICMA、ISLA、FpML、REGnosys (Rune DSL)、国際規制標準等の公式外部一次情報・リファレンスリンク集。

---

## 3. システムアーキテクチャ & 設定 (`overview/`)

- **[cdm_architecture.md](overview/cdm_architecture.md)**: CDM の全体構造、Rosetta (Rune) DSL ソース配置、および自動生成 Java クラスへの対応法則。

---

## 4. ドメイン概念 & ビジネスロジック (`concepts/`)

- **[product_modeling.md](concepts/product_modeling.md)**: 金利スワップ(IRS)、CDS、株式/オプション、コモディティ、スケジュール、決済条件、商品自動分類(Qualification)。
- **[event_lifecycle.md](concepts/event_lifecycle.md)**: 取引ライフサイクルイベント（Execution, Clearing, Novation, Allocation, Termination）およびポジション管理。
- **[fpml_ingestion.md](concepts/fpml_ingestion.md)**: FpML XML メッセージと CDM オブジェクトの相互変換・マッピング構造、IRS TradeState 対応表、および PartyReference (xsd:IDREF) 参照解決。
- **[legal_and_margin.md](concepts/legal_and_margin.md)**: ISDA/ICMA/ISLA マスターアグリーメント、CSA (担保契約)、Initial/Variation Margin 計算規則。
- **[observables_and_rates.md](concepts/observables_and_rates.md)**: 参照金利(FRO: SOFR, EURIBOR, TONA)、複利計算、日数計算(Day Count)。
- **[front_office_pricing_bounded_context.md](concepts/front_office_pricing_bounded_context.md)**: CDMをリファレンスとするフロントオフィス・プライシング業務の5つのBounded Context分割およびマイクロサービスアーキテクチャ設計。
- **[json_serialization_and_dialects.md](concepts/json_serialization_and_dialects.md)**: CDM JSON のシリアライゼーション仕様、@メタデータアノテーション構造、および用途・参照解決・DRR別の主要方言とJava/Python対応能力。

---

## 5. 主要エンティティ & データ型 (`entities/`)

- **[core_data_types.md](entities/core_data_types.md)**: Rosetta の主要型定義（`TradeState`, `BusinessEvent`, `Payout`, `LegalEntity`, `PriceQuantity`）のリファレンス。

---

## 6. 関数 & 自動判定 (`functions/`)

- **[qualification_and_calculation.md](functions/qualification_and_calculation.md)**: Rosetta 関数（`func`）、商品/イベント自動判定（`Qualify_`）、および計算ルーチンの解説。
