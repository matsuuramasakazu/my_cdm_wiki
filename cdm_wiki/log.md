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

## [2026-08-18] query | CDM JSON シリアライゼーション仕様と主要方言の整理・還元（CDM 7.x/6.x 準拠）
- `concepts/json_serialization_and_dialects.md` を作成・改訂。
- CDM の JSON 表現における 3 つの主要差異軸（メタデータ修飾 Qualified vs Unqualified、参照解決 Normalized vs Resolved、用途射影 Core Domain vs DRR/Projection）を体系化（不要な Legacy 2.x/3.x 記述を排除）。
- 現行メジャー `v7.x` / 直前メジャー `v6.x` を前提とした Java (`RuneJsonObjectMapper` / Jackson) および Python (`cdm-python` / Pydantic) のシリアライズ・デシリアライズ対応能力マトリクスと技術的根拠・公式一次情報リンク（FINOS, Rune, ISDA）を整備。
- Unqualified JSON のシステム間相互運用における 3 大アーキテクチャパターン（汎用 P2P 相互運用での Qualified 必須性、UI 配信 Consumer パターン、型確定 API/BFF Adapter パターン）を追記。
- JSON シリアライズにおける参照ポインタ表現体系（`@key` / `@key:external` / `@key:location` と `@ref` / `@ref:external` / `@ref:scoped` / `@ref:location`、および `ReferenceWithMeta<T>` の解決ライフサイクル）を追記。
- `globalKey`（`@key`）が主キーではなくコンテンツハッシュ（決定論的構造ハッシュ）である仕様特性と、同一ドキュメント内に重複 `globalKey`（`"globalKey": "0"` 等）が存在することの妥当性・仕様適合性を追記。
- 用途特化射影（Core Domain, Ingest中間形式, DRR）と 2 つの直交軸（Qualified/Unqualified × Normalized/Resolved）の明確な対応関係マッピング表を整理・追記。
- `index.md` カタログに登録。

## [2026-08-18] query | CDM 商品自動分類（Product Qualification）の階層判定アーキテクチャと具体例の整理・拡充
- `functions/qualification_and_calculation.md` を更新。
- ISDA Taxonomy v2 に準拠した 4 階層コンポーザブル判定体系（Asset Class → Base Product → Sub Product → Transaction Type）を整理。
- バニラ金利スワップ（IRS）、OISスワップ、通貨スワップ（Cross-Currency Swap）、為替NDF、スワップション、株式TRS等の具体的な Rosetta DSL 判定関数（`Qualify_`）および判定ルール・コード例を解説。
- 規制報告（Trade Reporting）自動化やシステム間相互運用における実務的メリットを体系化。

## [2026-08-19] query | Rosetta DSL の全 Type (759件) および Function (1,303件) のドメイン・機能別集計とカタログ化
- `rosetta-source/src/main/rosetta/` 配下の全 145 ファイルを網羅的に構文解析。
- `type`（759件）、`func`（1,303件）、`enum`（279件）のドメインプレフィックス別（`ingest-fpml`, `product`, `legaldocumentation`, `base`, `event`, `observable`, `margin-schedule`）およびビジネス機能別の集計・分類を実施。
- `overview/rosetta_dsl_inventory.md` を新規作成し、`index.md` カタログに登録。

## [2026-08-19] query | 手動作成 Java コード（42ファイル / 43クラス）の機能別分類とメトリクス化
- `rosetta-source/src/main/java/` 配下の手動実装 Java クラス（全 42 ファイル）を解析。
- ネイティブ関数実装（28件）、証券貸借・決済ワークフロー（5件）、自動分類判定エンジン（3件）、Guice DI & ランタイム設定（3件）、市場観測 & コードリスト（3件）の 5 大分類に体系化。
- `overview/rosetta_dsl_inventory.md` および `overview/cdm_architecture.md` を更新。

## [2026-08-19] query | プレーン金利スワップ（Vanilla IRS）の Trade 型構造 & クラス図の整理・還元
- `event-common-type.rosetta`, `product-template-type.rosetta`, `product-asset-type.rosetta`, `product-asset-floatingrate-type.rosetta` 等からプレーン金利スワップ（Fixed/Float IRS）の 4 階層型構造を抽出。
- `TradeState` $\rightarrow$ `Trade` (`TradableProduct`) $\rightarrow$ `EconomicTerms` $\rightarrow$ `InterestRatePayout`（Fixed/Floating）の詳細なクラス関連および属性定義を Mermaid クラス図として体系化。
- `concepts/vanilla_irs_trade_structure.md` を新規作成し、`index.md` カタログに登録。
