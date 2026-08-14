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
## [2026-08-12] query | CDMに基づくフロントオフィスプライシング業務のBounded Context分割とマイクロサービス設計
- CDM をドメインリファレンスとして活用し、フロントオフィスのプライシング業務を 5 つの Bounded Context（Market Data, Indication & Quoting, Pricing & Risk, Trade Negotiation & Confirmation, Trade Capture & Booking）に分割。
- 各コンテキストにおける CDM オブジェクト（`PriceQuantity`, `TradableProduct`, `Payout`, `WorkflowStep`, `TradeState` 等）の役割・対応関係を定義。
- `index.md` カタログを更新。

## [2026-08-12] query | 約定条件 Solver（逆算・探索）処理のコンテキスト所属および PV 計算エンジン依存関係の追加
- `concepts/front_office_pricing_bounded_context.md` にサブセクション 2.6 を追加。
- 約定条件（Par Coupon, Strike 等）を解く Solver 処理の主要実行エンジンとしての位置付け（Pricing & Risk Valuation Context）と呼出元（Indication / Negotiation Context）の役割分担を定義。
- Solver 探索ループにおける PV 計算エンジンへのインメモリ・ローカル依存性を解説。

## [2026-08-14] query | FpML PartyReference (xsd:IDREF / ecore:reference) 属性仕様と CDM 参照解決構造の反映
- `concepts/fpml_ingestion.md` にセクション 5 を追加。
- XML スキーマにおける `xsd:ID` / `xsd:IDREF` の参照整合性保証、EMF ECore バインディング用 `ecore:reference` メタデータ、および CDM (`ReferenceWithMetaParty`) での `href` 解決構造を記録。
- `index.md` の要約を更新。

## [2026-08-14] setup | AI Agent ハーネスの最適化（Antigravity Skills 新設・自動リンター配備）
- Antigravity 2.0 Skills 機構を導入し、`.agents/skills/` 配下に以下を新設：
  - `cdm-wiki-manager`: Wiki ライフサイクル（Query還元, Ingest, Lint, Frontmatter規約）の自動管理スキル。
  - `cdm-wiki-manager/scripts/validate_wiki.py`: Wiki 整合性・壊れたリンク・Frontmatter・カタログ登録の自動検証リンター。
  - `cdm-navigator`: 140+ の Rosetta DSL / Java コードベース高速探索・逆引きスキル。
- `.agents/AGENTS.md` および `cdm_wiki/SCHEMA.md` のルール・手順書を洗練・同期。
- `validate_wiki.py` による自動整合性チェックを実施（Error: 0）。

## [2026-08-14] ingest | CDM 外部公式一次情報・標準規格リンク集の追加
- `sources/official_external_sources.md` を新規作成。
- FINOS CDM 公式ポータル、GitHub、Rune DSL ドキュメント、ISDA / ICMA / ISLA の 3 大業界団体リソース、FpML 仕様ライブラリ、および GLEIF / CPMI-IOSCO 等の関連国際規格の一次情報リンクを体系化。
- `index.md` カタログに登録。

## [2026-08-14] update | 外部 URL 事前接続確認の絶対ルール化およびリンター機能拡張
- `validate_wiki.py` に外部 URL の HTTP 接続性（200 OK）自動検証機能を実装。
- `sources/official_external_sources.md` 内の全 URL をテストし、確実に接続可能な正確な URL のみに精査・更新。
- `.agents/AGENTS.md`、`cdm_wiki/SCHEMA.md`、および `cdm-wiki-manager/SKILL.md` に「外部 URL 事前接続確認の義務（絶対ルール）」を明文化。
- 全件リンター監査を実行し合格（全 16 ファイル・156 リンク・外部 URL 19 件 Error: 0）。



