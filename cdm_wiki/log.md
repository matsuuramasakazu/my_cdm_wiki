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

## [2026-08-19] query | 元本スケジュール定義クラス（NonNegativeQuantitySchedule, DatedValue, PrincipalPayments）の体系化
- 想定元本スケジュール（Amortizing/Step Notional）、元本交換スケジュール（PrincipalPayments）、為替連動リセット（FxLinkedNotionalSchedule）の型構造を特定。
- `concepts/vanilla_irs_trade_structure.md` にセクション 3 を追加し、クラス図と属性対応表を追記。

## [2026-08-19] query | 取引ライフサイクルイベント（BusinessEvent）のデータ構造 & 関数型状態遷移の体系化
- `event-common-type.rosetta`, `event-workflow-type.rosetta`, `event-common-func.rosetta`, `event-qualification-func.rosetta` を分析。
- `BusinessEvent` の Before/After 状態遷移モデル、13 種類の最小単位操作（`PrimitiveInstruction`）、および Novation/Allocation/Execution の具象フローを整理。
- `concepts/event_lifecycle.md` を大幅に拡充し、`index.md` カタログを更新。

## [2026-08-21] query | CDM バージョニング体系（SemVer）と後方互換性保証範囲の整理・還元
- FINOS CDM の Semantic Versioning 2.0.0 仕様（`MAJOR.MINOR.PATCH` および `-DEV` プレリリース）を体系化。
- メジャーバージョン（破壊的変更: 削除/改名/型変更/必須化/条件厳格化）およびマイナーバージョン（後方互換機能追加: オプショナル属性/新規型/新規関数/Enum値追加）のインクリメント基準を定義。
- 同一メジャーバージョン内における後方互換性の保証範囲（過去データの 100% 妥当性保証、Java/API ソース・バイナリ互換性）および前方互換性・Enum網羅性チェック等の留意点を整理。
- `overview/versioning_and_compatibility.md` を新規作成し、`index.md` カタログに登録。

## [2026-08-24] query | CDM バージョニング・互換性ドキュメントへの公式一次情報引用の具体化・追記
- `overview/versioning_and_compatibility.md` に、FINOS CDM 公式ドキュメント（Versioning, Change Control Guidelines, Maintenance and Release, Major Release Scheduling Guidelines）からの英語原文引用および具体的セクション参照を追記。
- 破壊的変更（Prohibited changes: 構造変更/削除/改名/制約厳格化/DSL式無効化/公開API変更）と許容変更（Allowed changes: 制約緩和/テストパック追加/文書更新/オプショナル要素追加）の公式定義を原文引用とともに整理。
- PR 分類（Bug fix / Enhancement / Technical）およびリリースビルド（Major / Minor / Patch / Dev）ごとの承認者要件マトリクス（Maintainer, CRWG, SWG, TAWG）を公式ドキュメントから引用・体系化。
- `sources/official_external_sources.md` および `index.md` に公式ガバナンス・バージョニングドキュメントへのリンクを反映。

## [2026-09-16] query | TradableProduct における product と tradeLot の分離構造 & 元本参照解決の解説
- `TradableProduct` における `product` (`NonTransferableProduct`) と `tradeLot` (`TradeLot`) の関心事の分離設計思想（商品条項定義 vs 約定ロット経済条件）を解明。
- `tradeLot` 内の `quantity` に名目元本実額（Notional Amount）が直接保持される仕組みと、`@ref:scoped` によるポインタ参照解決メカニズムを整理。
- `principalPayment` の `principalAmount` が元本交換の実金額（`Money` 型の実額）であることを DSL および FpML Ingestion コード（`MapPrincipalPayment`）から実証。
- `concepts/tradable_product_and_tradelot.md` を作成し、`index.md`、`vanilla_irs_trade_structure.md`、`log.md` を更新。

## [2026-09-16] query | EconomicTerms と CalculationPeriodDates における effectiveDate / terminationDate の使い分けと解決ロジック
- `EconomicTerms`（契約全体レベル：CDS, Repo, GMSLA等）と `CalculationPeriodDates`（個別レグレベル：IRS, CCS等の利息ストリーム）における日付階層とスコープの違いを解明。
- 金利スワップにおいてレグ側に日付が配置される実務的理由（通貨別カレンダー休日の非対称性、スタブ期間の独立性、変形スワップ）および FpML Ingestion でのマッピング差異を整理。
- CDM 証拠金計算ロジック（`margin-schedule-func.rosetta` の `AuxiliarEffectiveDate` / `AuxiliarTerminationDate`）における `min` / `max` 集約による日付解決仕様を体系化。
- `concepts/contract_dates_modeling.md` を新規作成し、`index.md`、`vanilla_irs_trade_structure.md`、`log.md` を更新。

## [2026-09-17] query | WorkflowStep 構造と FpML ライフサイクル変換サンプル (Execution Advice) の解説
- `fpml-5-13-processes-execution-advice` フォルダ内の CDM JSON 出力サンプル全18件を網羅的に分析。
- CDM における `WorkflowStep` の役割（外部メッセージとビジネスイベントの分離、`proposedEvent` vs `businessEvent` vs `rejected`、Lineage管理）を体系化。
- 取引ライフサイクル（新規約定 `ContractFormation`、一部契約更改 `Novation` (`split`)、中途解約 `quantityChange` (value=0 で全部解約)、条件変更 `ContractTermsAmendment`）における Primitive 操作と `before` 状態の組み合わせモデルを解説。
- FpML メッセージの訂正（`action: "Correct"`）と取消（`executionAdviceRetracted`）の CDM での追跡手法、およびコモディティ現物レグ・ESMA EMIR REFIT 規制分類（ISO 4914 UPI, SWAP タクソノミー）を整理。
- `concepts/workflow_step_and_lifecycle_samples.md` を新規作成し、`index.md` および `log.md` を更新。
- ワークフロー JSON デシリアライズ後の状態遷移実行メカニズム（`Create_AcceptedWorkflowStepFromInstruction`, `Create_BusinessEvent`, `Create_TradeState` による `after: TradeState` 生成）、Validation、Qualification、キャッシュフロー試算、DRR 規制報告連携、Java/Python 実装アプローチを体系化して追記。

## [2026-09-20] update | 一次ソース最新版（CDM 7.0.0 → 7.4.0 / 7.x.x）への Wiki 全面整合性同期
- 一次ソース `common-domain-model/rosetta-source/src` の 7.0.0 から 7.4.0（7.x.x ブランチ `efe1cb15c`）への更新に伴う整合性調査を実施。
- `overview/rosetta_dsl_inventory.md` の定義メトリクスを最新化：Type 759→780型（+21型）、Function 1,303→1,323関数（+20関数）、Enum 279→280列挙型（+1型）。ドメイン別・機能別分類内訳を更新。
- `overview/versioning_and_compatibility.md` に CDM 7.x 系（7.0.0〜7.4.0 安定本番版、7.x.x 開発ブランチ）のリリース状況と位置づけを追記。
- `concepts/event_lifecycle.md` にリセット処理の Instruction Composition 機構（Reset Step 2〜6: `event-instructioncomposition-reset-*`）の段階的合成設計を追記。
- `concepts/contract_dates_modeling.md` に CDM 7.x で追加された営業日調整・日付シフト関数群（`base-datetime-func`）および `CalculationPeriodImpl.java` の拡張を反映。
- `concepts/fpml_ingestion.md` に FpML `executionNotification` 取込マッピングおよび当事者識別子スキーム拡張を追記。
- `concepts/observables_and_rates.md` に参照金利観測種別判定ロジック（`DetermineObservationType` 等）を追記。
- `CDM_INDEX.md`、`sources/cdm_index_source.md`、`index.md` のナビゲーションおよびカタログ要約を最新状態に同期。

## [2026-09-20] query | Java版CDMライブラリ パッケージ作成のための前提環境調査・検証
- Java版CDMライブラリ（`cdm-java`）のビルド・パッケージングに必要な基盤要件（JDK 21制約、Maven 3.9+、Java 8互換バイトコード出力）を特定。
- コード生成基盤を支えるテクノロジー・プロダクト群（Rune / Rosetta DSL 10.13.0, rosetta.code-gen 12.19.0, Eclipse Xtext 2.38.0, rune-fpml 3.8.0）を整理。
- 機能分類別の依存プロダクト群（Guice 6.0.0, OpenGamma Strata 1.7.0, Jackson 2.18.10, Saxon-HE 10.6, jsoup 1.23.2, Guava 33.3.1-jre）を体系化。
- 実機環境で全5段階の動的検証を実施：バージョン確認、Maven Enforcer Plugin 制約チェック、プロパティ値評価、`rune-maven-plugin` による Rosetta DSL からの Java コード自動生成（6,300+クラス）、`mvn package` による JAR パッケージ生成（25.5MB `cdm-java-0.0.0.master-SNAPSHOT.jar`）。ハルシネーションを完全に排除した検証エビデンスを実証。
- `overview/java_cdm_build_and_packaging.md` を新規作成。コード生成基盤パイプライン図と解説の 1 対 1 対応、接続確認済み公式 GitHub URL（42件）、直接参照プロダクト一覧への詳細情報集約、および推移的依存ライブラリ（親プロダクト別カテゴリ分類）の表形式一覧化を実施。
- `index.md` および `log.md` を更新し、`validate_wiki.py` による整合性バリデーション（エラー0件）を確認。

## [2026-09-20] query | Python版CDMライブラリ パッケージ作成のための前提環境調査・検証
- Python版CDMライブラリ（`finos-cdm`）のコード生成・ビルド・パッケージングに必要な前提基盤要件（Java 21, Python 3.11+, Maven 3.9+, Git 2.x）を特定。
- コード生成基盤テクノロジー（Rune Python Generator `finos/rune-python-generator:10.13.0.0`, Rosetta DSL `10.13.0`, `rune-fpml:3.8.0`）を整理。
- ビルド・パッケージングツール（`pip`, `venv`, `wheel`, `setuptools>=77.0.3`, `build`, `twine`）および実行時依存（`pydantic>=2.10.3`, `rune.runtime>=2.2.0,<3.0.0`）、推移的依存（`annotated-types`, `pydantic-core`, `typing-extensions`, `typing-inspection`, `python-dateutil`, `tzdata`, `six`）、テスト依存（`pytest`, `pluggy`, `iniconfig`, `packaging`, `colorama`, `pygments`）を全列挙し、公式GitHubリポジトリ（全件HTTP 200疎通確認済）とともに体系化。
- 実機環境で全6段階の動的検証を実施：ローカル基盤ツールバージョン確認、DSLバージョンおよびジェネレータJAR取得確認、FpML依存確認、`PythonCodeGeneratorCLI` による Python コード生成実行（1,728ファイル出力）、`pyproject.toml` 依存解析、一時仮想環境での wheel パッケージビルド（`finos_cdm-0.0.0-py3-none-any.whl` 2.03MB生成）、インストールおよび `pytest` によるインポートテスト（`TradeState` のインポート確認 1 passed in 9.18s）。ハルシネーションを完全に排除した検証エビデンスを実証。
- `overview/python_cdm_build_and_packaging.md` を新規作成し、`index.md`、`log.md` を更新。
- `python-10.13.0.0.jar` の内部 META-INF メタデータ（`jar -tf`）および `rune-python-generator` リポジトリの `pom.xml` / `mvn dependency:tree` 解析を実施。ジェネレータが直接依存する10プロダクト（`rune-lang`, `rune-runtime`, `emf.codegen.ecore`, `guice`, `commons-cli`, `commons-io`, `jgrapht-core`, `slf4j-api`, `logback-classic`, `log4j-over-slf4j`）および推移的依存（Eclipse Xtext 2.44.0, Guava 33.6.0, Jackson 2.18.10 等）を機能カテゴリ別に体系化して `overview/python_cdm_build_and_packaging.md` に追記。`validate_wiki.py` による整合性バリデーション（全68件外部URL疎通、エラー0件）を確認。

## [2026-09-24] query | Rune DSL から cdm-json-schema を生成する処理フローの一次ソース調査・実機検証
- 一次ソース（`common-domain-model/rosetta-source/pom.xml`, ルート `pom.xml`, `rune-config.yml`, `codefresh.yml`, `docs/download.md`, `website/scripts/`）を調査。
- 入力ソース事前集約（`maven-resources-plugin` による CDM + FpML DSL の集約）、JSON Schema 生成（`json-schema` プロファイル、`rune-maven-plugin`、`CDMRosettaSetup`、`default-cdm-generators`）、ZIP パッケージング & 配布（Codefresh CI/CD `DeployJsonSchema`）、および公式ポータルサイト反映（`download-schemas.js`）の一連の処理フローを特定。
- 実機検証を実施：`mvn generate-sources -P json-schema` を実行し、`src/generated/jsonschema/` に 1,142 件の `.schema.json` ファイルが生成されることを確認（BUILD SUCCESS, 所要時間 2分05秒）。
- `overview/json_schema_generation_and_packaging.md` を新規作成（実行エビデンス追記）し、`index.md` および `log.md` を更新。

## [2026-09-24] query | CVA計算に必要な担保・契約・顧客・ネッティング情報の一次ソースDSL調査
- CVA（信用評価調整）計算に必要な 4 大要素（担保情報、契約情報、顧客・相手方情報、ネッティング情報）の Rosetta DSL 定義を一次ソースより特定・調査。
- 担保情報: `Threshold`（格付連動/ゼロ転落）、`MinimumTransferAmount`、`CollateralValuationTreatment`（ヘアカット）、`CollateralPortfolio`、`CollateralBalance`。
- 契約情報: `Trade -> contractDetails: ContractDetails`、`LegalAgreement`、`MasterAgreement`、`governingLaw`。
- 顧客情報: `Party`（LEI）、`LegalEntity`、`RelatedParty`（Guarantor 代替判定）、`CreditNotation`（格付・PD推計）。
- ネッティング情報: クローズアウト・ネッティングセット（`MasterAgreement` の `automaticEarlyTermination`、`terminationCurrency`）、マージン・ネッティングセット（`CollateralPortfolio -> portfolioIdentifier`）、決済ネッティング（`StandardSettlementStyleEnum`）。
- `concepts/cva_calculation_data_modeling.md` を新規作成し、`index.md` および `log.md` を更新。

## [2026-09-24] query | CDM Java版ライブラリとPython版ライブラリの非対応（未実装）機能の網羅的調査
- 一次ソース（`common-domain-model`, `rune-python-generator`, `rune-python-runtime`）を横断調査。
- フル機能の基準実装である Java版（`cdm-java`）に対し、Python版（`finos-cdm` / `rune-python-generator`）において非対応・未実装となっている機能を4大分類で特定：
  1. Rosetta DSL構文・アノテーション: DRR構文（`report`, `reporting rule`, `eligibility rule`）、関数継承（`extends`, `super`）、`typeAlias` のドメイン型名喪失（Java Path による基底プリミティブ展開）および named `condition` 脱落、メタデータアノテーション（`[synonym]`, `[deprecated]`, `[rootType]`, `[qualification]`, `[projection]`）の無視。
  2. ネイティブ関数（Java Native Functions）: Java版 `CdmRuntimeModule` で提供される日付・時刻計算（`CalculationPeriods`, `AddDays`, `DateDifference` 等 11関数）、数値・丸め・ベクトル演算（`RoundToNearest`, `VectorOperation` 等 5関数）、外部データプロバイダー（`BusinessCenterHolidays`, `IndexValueObservation`）、コードリストロード（`LoadCodeList`）が、Python版では未実装スタブ（呼出時 `NotImplementedError`）であることを解明。
  3. 業務パイプライン・オーケストレーション: 商品・イベント自動分類エンジン（`QualifyProcessorStep`）、外部電文変換（FpML XML/FIX/ISO 20022 からの Ingest / Projection）、外部スキーム動的検証（`[metadata scheme]`）、オブジェクト走査ハッシュ計算・グローバルキー自動付与パイプラインの欠落。
  4. アーキテクチャ・パラダイム: 不変オブジェクト+Builder vs Pydantic v2モデル、XML/FpML非対応（JSON特化）。
- `overview/cdm_python_vs_java_feature_parity.md` を新規作成し、`index.md` および `log.md` を更新。

## [2026-09-25] query | CDM JSON フォーマットのバージョン 7.x.x と 6.x.x の差異調査
- FpML Ingest サンプル（`ird-ex01-vanilla-swap.json`）および `cdm-json-schema`（v6.28.1 vs v7.4.0）を実機比較。
- CDM 7.x における Rune JSON Standard（`@` 属性によるメタデータ表現、不要キー枝刈り、ポリモーフィズムのフラット化）と 6.x (Legacy JSON / RosettaObjectMapper) の根本的差異を解明。
- サンプルファイルにおける約44%の行数削減（560行→316行）、約43%の文字数削減（16.6KB→9.5KB）を実証。
- 配布 `cdm-json-schema`（Draft-04）が v7.4.0 でも依然として Legacy JSON 形式であり、Rune JSON サンプルと過渡期的な非同期状態にある重要な技術的留意点を特定。
- `concepts/json_serialization_and_dialects.md` を作成し、`index.md` および `log.md` を更新。

## [2026-09-30] query | Rune DSLによる独自のCDMモデル拡張ワークフロー調査の反映
- Rune DSL（旧Rosetta DSL）を用いた独自の型、関数、列挙型追加によるCDM拡張ワークフローを体系化。
- 外部下流プロジェクト（Downstream / In-house）での自社専用拡張と、FINOS CDM コミュニティ本体（Upstream）へのコントリビューション拡張の2大アプローチを対比。
- Rune DSL における名前空間分離（namespace）、型継承（extends）、型合成（composition）、列挙型拡張（enum extends）、ビジネス関数（func）の構文仕様を整理。
- 外部プロジェクトにおける共通プロジェクト構成と `rune-config.yml`（namespaceConfig による CDM の read-only 保護、generators.namespaces）を定義。
- 【Java版】`rune-maven-plugin`（generate ゴール）による `RosettaModelObject` / Builder パターンの自動生成パイプラインを網羅。
- 【Python版】`finos/rune-python-generator`（`PythonCodeGeneratorCLI` Fat JAR）による Pydantic v2 準拠の Python クラス群および `pyproject.toml` 自動生成、Wheel パッケージング（PEP 517）、`rune.runtime` 連携パイプラインを追記。
- Java版 vs Python版のコード生成・実行モデル分岐対比表（ジェネレータ、オブジェクトモデル、シリアライゼーション、ランタイム、制約）を作成。
- 一次情報ファイル（`rosetta-source/pom.xml`, `rune-config.yml`, `editing.md`, `namespace.md`, `design-principles.md`, `python_cdm_build_and_packaging.md`）および公式外部URL（全件 HTTP 200 OK 疎通確認済）を提示。
- Pythonプロジェクトにおける `rune-config.yml` の具体的役割（CI/CD名前空間保護、標準メタデータ宣言、共通仕様化ロードマップ）の解説を追記。
- `concepts/extending_cdm_with_rune_dsl.md` を更新し、`index.md` および `log.md` を同期。

## [2026-10-05] query | cdm-java 下流利用ワークスペースにおける Java 8 動作互換性の一次ソース検証
- `rosetta-source/pom.xml` の `<maven.compiler.release>8</maven.compiler.release>` および親 POM の `<java.enforced.version>[21,22)</java.enforced.version>` を一次ソースから比較検証。
- CDM 本体のビルド環境（アップストリーム）では DSL コード生成基盤（Xtext / Rune プラグイン）の制約により JDK 21 が必須（Enforced）である一方、配布パッケージ `cdm-java` は `javac --release 8` によりコンパイルされていることを解明。
- コミット `fffd1fe9`（PR #1877）の `RELEASE.md` における設計意図（「To provide a wider compatibility for CDM Java implementors, this release changes the Java version of the distributed CDM Java artefacts from version 11 to 8...」）を特定。
- 実際にビルドされた `cdm-java-0.0.0.master-SNAPSHOT.jar` および主要ランタイム依存関係（`rune-runtime`, `rune-common`, `strata-basics`, `guava`, `jackson-databind`, `Saxon-HE`, `jsoup`）を `javap` で実機検証し、全クラスが `major version: 52`（Java 8 バイトコード）かつ Java 8 標準 API 制約下で提供されていることを実証。
- 下流ワークスペースにおいて、JDK 8 を用いて Java 8 でコードを書き、Java 8 でビルド・実行可能であることを確認。
- `overview/java_cdm_build_and_packaging.md` に「2.1 CDM 利用側（Downstream Project）における Java 8 動作互換性」を追記し、`index.md` および `log.md` を更新。

## [2026-10-07] query | CDMにおけるIndex、通貨、都市、商品一覧のコード値定義調査と反映
- CDM における「Index」「通貨」「都市」「商品」のコード値定義構造を一次ソース（Rosetta DSL、FpML Genericode XML、同梱 JSON リソース、Java ランタイム実装）から網羅的に調査。
- 3層コード値管理アーキテクチャ（DSL静的Enum、FpML Coding Scheme動的コードリスト、モデル駆動Qualification自動判定）を解明：
  1. Index一覧: `observable-asset-type.rosetta` の型階層（`IndexBase` / `choice Index`）、`FloatingRateIndexEnum`（700+ FROコード）、動的スキーム `FloatingRateIndex: FpMLCodingScheme(domain: "floating-rate-index")`、および `floating-rate-index-3-10.json`。
  2. 通貨一覧: `base-staticdata-asset-common-enum.rosetta` の `ISOCurrencyCodeEnum`（ISO 4217準拠 180+通貨）および継承拡張 `CurrencyCodeEnum extends ISOCurrencyCodeEnum`（FpML nonISOCurrencyScheme 準拠の CNH 等 9通貨）。
  3. 都市一覧: `base-staticdata-codelist-type.rosetta` の `typeAlias BusinessCenter: FpMLCodingScheme(domain: "business-center")`、`base-datetime-type.rosetta` の `BusinessCenters`、および同梱 JSON リソース `business-center-9-3.json`（JPTO, USNY, GBLO 等 150+都市）。`LoadCodeList` / `ValidateFpMLCodingSchemeDomain` による実行時検証。
  4. 商品一覧: `base-staticdata-asset-common-type.rosetta` の `ProductTaxonomy`（`TaxonomySourceEnum`: ISDA, CFI, EMIR, CFTC 等、`AssetClassEnum`、`ProductIdTypeEnum`: ISIN, UPI 等）、同梱 JSON リソース（`product-taxonomy-4-0.json`, `product-type-simple-1-7.json`）、および `product-qualification-func.rosetta` によるモデル駆動の自動判定（Qualification）ロジック。
- 一次情報ソースファイルパス、行数、および事前 HTTP 接続テスト（全件 200 OK）済み外部仕様 URL を特定。
- `concepts/reference_data_and_codelists.md` を新規作成し、`index.md` および `log.md` を更新。

## [2026-10-07] query | CDM DSLからのJSON Schema生成仕様・対象スコープ・ジェネレータ実装リポジトリの調査反映
- CDM の Rosetta (Rune) DSL から JSON Schema を生成する仕様、生成スコープ、およびコード所在リポジトリを一次ソース・外部リポジトリから網羅的に調査。
- ジェネレータ実装コードの所在を特定：
  - コード本体は `REGnosys/rosetta-code-generators`（GitHub OSS）の `json-schema` モジュール（`com.regnosys.rosetta.code-generators:json-schema`）に存在。
  - 主要クラス: `JsonSchemaCodeGenerator.java`, `JsonSchemaTypeGenerator.xtend`, `JsonSchemaMetaFieldGenerator.xtend`, `JsonSchemaGeneratorHelper.xtend`, `JsonSchemaTranslator.xtend`。
  - セットアッププロバイダ: 同リポジトリの `default-cdm-generators` モジュール内の `CDMRosettaSetup.java` および `DefaultExternalGeneratorsProvider.java`。
  - ビルドプラグイン基盤: `finos/rune-dsl`（`org.finos.rune:rune-maven-plugin`）。
- JSON Schema 生成対象スコープの詳細仕様を解明：
  1. ネームスペーススコープ: `rune-config.yml`（`cdm.*`, `com.rosetta.model`）および `JsonSchemaCodeGenerator.java` の `isSupportedModel()` により制御。`cdm.*` の中核モデルおよび `com.rosetta.model` は生成対象。`fpml.*`（FpML外部モデル）、`*.ingest.*`（電文取込用型）、`*.mapping.*`（マッピング定義）は除外。
  2. DSL構文要素スコープ: `type`（データ型 / Data）、`enum`（列挙型 / RosettaEnumeration）、メタ属性付与に伴うメタ型・参照型（`FieldWithMeta...`, `ReferenceWithMeta...`, `MetaFields` 等）のみ生成。`func`（関数）、`rule`（マッピング）、`condition`/`choice`（動的制約）は対象外。
  3. 属性・多重度スコープ: 多重度 `1..1` のみ `required` 配列に反映。配列（複数多重度）は `minItems` / `maxItems` つき `array` 表現。生成スキーマ規格は Draft-04（`http://json-schema.org/draft-04/schema#`）。
## [2026-10-08] query | 通貨オプション単体およびシンセティックフォワード（複数受渡日）のCDM表現の調査と還元
- 通貨オプション（FX Option）単体の CDM モデリング構造（`OptionPayout`, `OptionStrike`, `ExerciseTerms`, `SettlementTerms`, `Qualify_ForeignExchange_VanillaOption`）を一次ソースから特定。
- ストリップ型シンセティックフォワード（複数確定受渡日）の 2 大表現アプローチ（単一 Trade 内複数 Payout 方式 vs TradePackage パッケージ取引方式）を比較整理。
- フラットレート（単一ストライク）および期日別ストライク（マルチフォワード: スワップポイント加味）のデータ構造、純粋先渡ストリップ（`SettlementPayout` 複数配置）との対比を解明。
- 3 段階の動的ライフサイクルイベント（`ExerciseInstruction` による権利行使、`TransferInstruction` による資金決済、`QuantityChange` による残高更新および TradeState 遷移）を体系化。
- `concepts/fx_products_and_synthetic_forward.md` を作成・拡充し、実機サンプル JSON 群（`fx-ex09-euro-opt.json`, `fx-ex10-amer-opt.json`, `fx-ex11-non-deliverable-option.json`, `fx-ex08-fx-swap.json`, `fx-ex26-fxswap-multiple-USIs.json`, `msg-ex54-execution-advice-trade-partial-termination-C11-00.json`）による要素レベルの裏どりエビデンス（Section 4）を追記同期。
- 為替スポット（FX Spot）および単体プレーン為替先渡（FX Forward）のモデリング仕様（`SettlementPayout` 統一構造、ISDA Taxonomy `ForeignExchange_Spot_Forward`、`Price.composite` による直物＋フォワードポイント合成、`fx-ex01-fx-spot.json` と `fx-ex03-fx-fwd.json` の実サンプル比較検証）を解明し、同ドキュメント（Section 1 & 5.1）に追記反映。
- バリアオプション（Barrier Option）およびアベレージオプション（Asian Option）を考慮した動的ライフサイクルイベントの体系的拡張（全 8 大イベント: `Observation`, `Reset`, `Trigger / Knock`, `Exercise`, `Expiration`, `Transfer`, `QuantityChange`, `ValuationUpdate`）を解明。
- Asian オプションにおける平均化確定（`ResetInstruction`, `TradeState.resetHistory`, `Create_Reset`, `Qualify_Reset`, `AsianOptionChoice` による `averagingFeature` と `averagingStrikeFeature` の排他制御）および実機サンプル（`fx-ex20-avg-rate-option-parametric.json`, `fx-ex22`）の要素対応を特定。
- バリアオプションにおけるノックアウト消滅・リベート支払（`Barrier.knockOut`, `ClosedStateEnum -> Terminated`, `FeaturePayment` $\to$ `Transfer`）、ノックイン活性化（`Barrier.knockIn`）、および実機サンプル（`fx-ex13-fx-dbl-barrier-option.json`）の要素対応を特定。
- `concepts/fx_products_and_synthetic_forward.md`（Section 4 & 5.6）に反映。

## [2026-10-08] query | バリアタッチおよびアベレージレートFixingのイベント表現サンプルJSON調査と実態検証
- バリアタッチ（Knock-In / Knock-Out）およびアベレージレートFixing（Observation / Reset）のイベント表現サンプルJSONの有無をリポジトリ全域（全3,686ファイル）から網羅的に調査。
- 調査結果と不整合の実態解明：
  1. イベント表現（`BusinessEvent` / `WorkflowStep`）のサンプルJSONの不存在: 為替におけるレートFixing（`Reset`）やバリア到達（ノックアウト・消滅・リベート支払）のライフサイクルイベント実行結果JSONはリポジトリ内に一切存在しない（0件）。
  2. 契約定義（`TradeState`）の静的サンプルの実態:
     - アベレージオプション: 実在ファイルは `fx-ex21-avg-rate-option-parametric-plus-rate-observation.json` であり、初期契約時の `OptionPayout.observationTerms`（観測スケジュール、情報源、観測時刻）を保持するが、期中観測値や平均確定イベントは未収録。
     - バリアオプション: `fx-ex13-fx-dbl-barrier-option.json` 等は `incomplete-products` に分類されており、FpML Ingest 変換器の未対応により `OptionPayout.feature.barrier` は出力されず欠落（商品タクソノミ名 `DOUBLEBARRIER` のみ保持）。
  3. Rosetta DSLイベントモデル設計の精査:
     - `TradeState.observationHistory`（型: `ObservationEvent`）はクレジットイベント・コーポレートアクション専用であり、市場クォート観測値は `Reset.observations: Observation (1..*)` として保持され `TradeState.resetHistory` に蓄積される仕様を解明。
     - `Trigger` は契約側の条件型でありイベントプリミティブではないこと、ノックアウト消滅は `QuantityChangeInstruction`（数量0・Terminated）および `TransferInstruction`（リベート）の複合イベント（認定: `Qualify_Termination`）として表現される仕様を解明。
- `concepts/fx_products_and_synthetic_forward.md`（Section 4 & 5.6）および `index.md` を更新同期。
 
## [2026-10-09] query | FX TARF、デジタル系オプションおよび行使後ペイアウト（現物スポット派生 vs 差金決済）のモデリング調査と還元
- **FX TARF (Target Accrual Redemption Forward)** の金融工学構造および CDM モデリング手法を体系化：
  - 各期日のレバレッジ構造（クライアント買Call $N$ ＋ クライアント売Put $L \times N$）の非対称 Payout ペア設計。
  - 累積利益計算エンジンと CDM プロトコルの境界（連続的累積損益計算は外部エンジンに委譲、確定後の状態遷移を CDM イベントとして記録）。
  - 目標到達時の早期消滅（Redemption）を `QuantityChangeInstruction`（将来期日数量の0化置換、`ClosedState = Terminated`、認定: `Qualify_Termination`）としてモデル化。
  - 最終期の数量按分調整（Exact Accrual）における部分数量縮小（Downsize）と決済の連動。
- **デジタル系通貨オプション (Digital / Binary Options)** の類型と CDM 表現・実態を解明：
  - European Cash-or-Nothing / Asset-or-Nothing、American One-Touch / No-Touch、Double One/No-Touch のペイオフと判定条件を対比整理。
  - CDM 正規表現: `OptionPayout` の `feature.barrier`（`knockIn` / `knockOut`）、`Trigger`（`PriceSchedule`, `triggerType`, `triggerTimeType`）、固定額受渡（`FeaturePayment` または `CashSettlementTerms.cashSettlementAmount`）。
  - 一次ソース Ingest 実装の実態検証: `ingest-fpml-confirmation-product-fxdigitaloption-func.rosetta`（`MapFxDigitalOptionNonTransferableProduct`）がスケルトン実装（`underlier: empty`、トリガー欠落）であること、一次リポジトリのサンプル出力（`fx-ex14` 〜 `fx-ex19`）が `incomplete-products` に隔離されている要因をコード裏どり。
  - タクソノミ認定関数（`Qualify_ForeignExchange_VanillaOption` / `NDO` のみ存在、Digital 用判定関数は未定義）の実態を解明。
- **権利行使後のペイアウト（Payout after Exercise）の決定論的メカニズム** を完全解明：
  - `event-common-func.rosetta` の `Create_Exercise`（L498-553）の厳密な仕様と 2 つの `TradeState`（原契約の減額・終了 ＋ 派生取引約定）返却仕様を解明。
  - **現物受渡（Physical Exercise）**: 通貨アンダーライング（`Cash`）から `Create_NonTransferableProduct`（L568-578）が起動し、為替スポット取引の型である `SettlementPayout` を持つ新規プロダクトを自動合成、Put オプション時の方向反転（`Update_ProductDirection` L554-567）、および `replacementTradeIdentifier` による新規 UTI 付番から受渡日（Value Date）の `Transfer` 決済までのエンドツーエンドのフローを解明。
  - **差金決済（Cash Settlement / NDO）**: 新規スポット契約を生成せず、`Reset` によるレート確定後、`ExerciseInstruction.exerciseQuantity` 内の `TransferInstruction` により差金決済額を送金し原契約を `Terminated` とするパスを対比整理。
- `concepts/fx_products_and_synthetic_forward.md` を大幅拡充（タイトル更新、新第3.2節、新第4章、新第5章、新第7.7節・7.8節追加）、および `index.md` を更新同期。

## [2026-10-09] query | NDF (Non-Deliverable Forward) の CDM モデリング調査と還元
- 直物差金決済為替先渡（NDF: Non-Deliverable Forward）の金融工学背景（規制新興国通貨・資本規制・差金決済計算式 $\text{USD} = N_{USD} \times \frac{S - K}{S}$）と CDM モデリング仕様を解明。
- CDM データ構造の決定論的特徴:
  - ペイアウト基底型は Spot / Deliverable Forward と同一の `SettlementPayout`。
  - 判別キーは `SettlementTerms.cashSettlementTerms`（存在する場合、ISDA タクソノミが `ForeignExchange_NDF` と自動判定。Spot/Forward は `cashSettlementTerms is absent`）。
  - 通貨規制により新興国通貨（INR, KRW, BRL 等）の受渡は行われず、単一のハードカレンシー（通常 `USD`）が `settlementCurrency` として指定。
  - 為替フィキシング日は `cashSettlementTerms.valuationDate.fxFixingDate` に保持され、決済期日（`settlementDate.valueDate`）とは明確に分離。
- NDF のライフサイクル状態遷移（約定 $\to$ 市場観測 $\to$ フィキシング確定（`Reset`） $\to$ 差金決済送金（`Transfer`） $\to$ 契約消滅（`Terminated`））のシーケンスと NDS（Non-Deliverable Swap）・NDO（Non-Deliverable Option）との対比を整理。
- 実機サンプル検証: FpML 入力 XML（`fx-ex07-non-deliverable-forward.xml`）および CDM 出力 JSON（`fx-ex07-non-deliverable-forward.json`）の全フィールド対比検証を実施。FpML 5-13 の旧 `<nonDeliverableSettlement>` が CDM では `CashSettlementTerms` 配下に統一正規化（Harmonization）されていること、およびタクソノミ `ForeignExchange_NDF` が `calculated: true` で自動推論される仕様を裏どり。
- `concepts/fx_products_and_synthetic_forward.md`（新第2章、新第8.2節の追加、セクション番号繰り下げ、Frontmatter 更新）、`index.md`、および `log.md` を更新同期。

## [2026-10-09] query | FX TARF、デジタルオプション、NDF の一次ソース整合性監査とハルシネーション是正
- 一次ソース（`common-domain-model/rosetta-source/` の Rosetta DSL コードおよび `ingest/output/` の JSON サンプル）に照らし合わせ、`concepts/fx_products_and_synthetic_forward.md` の記載を厳密に監査し、以下のハルシネーション（過剰解釈・誤謬）およびパス不整合を洗い出して是正。
- **1. FX TARF (Target Accrual Redemption Forward) のハルシネーション是正**:
  - 一次ソース内に `tarf` や `TargetAccrual` といったキーワードや型定義、Qualification 関数は **完全皆無（0件）** である事実を明記。
  - `EconomicTerms.earlyTerminationProvision` というパスは存在せず、正しくは `EconomicTerms.terminationProvision.earlyTerminationProvision`。
  - `MandatoryEarlyTermination` は金利スワップ等の日付指定型・公正価値解約規定（ISDA ird-44）であり、累積利益（Target Cap）や超過利益処理（Full / Exact Accrual）を表現する属性は一切持たない誤用を是正。
  - `Barrier.knockOut` も単一レート判定であり累積損益集計には使えない。TARF は CDM 上は非対称ストリップオプションとして保持し、消滅条件は CDM スキーマ外の非標準条項（`nonStandardisedTerms: true`）とし、外部のリスク管理エンジンが計算・判定して `QuantityChangeInstruction`（数量0置換）で終了させる運用限界を明記。
- **2. デジタル系FXオプション (Digital / Binary Options) の是正**:
  - `product-qualification-func.rosetta` にデジタルオプション用の自動判定関数（`Qualify_ForeignExchange_DigitalOption` 等）は **0件（非存在）** であり、実サンプルでも ISDA 分類ではなく `taxonomy.source = Other` として保持される事実を明記。
  - `FeaturePayment` の必須属性 `payerReceiver PartyReferencePayerReceiver (1..1)` の記載漏れを修正。
  - `CashSettlementTerms.cashSettlementAmount` による代替案はクレジットイベント用であり為替オプションには適用されない事実を明記。
  - `output/` 配下の実在サンプル `fx-ex14` 〜 `fx-ex19`（`euro-range-digital`, `one-touch`, `no-touch`, `double-one-touch`, `double-no-touch`）の JSON リンクをすべて配備・引用し、マッピング関数未整備による属性欠落の実態を裏どり。
- **3. NDF (Non-Deliverable Forward) の是正**:
  - `ValuationDate.fxFixingDate`（型: `FxFixingDate`）内に属性 `fxFixingDate`（型: `AdjustableOrRelativeDate`）が存在する二重ネスト構造（`valuationDate.fxFixingDate.fxFixingDate...`）を実サンプル `fx-ex07.json` と照合して正確なパスに修正。
  - CDM 内部の関数（`CalculateReset` 等）には NDF の差金決済額自動計算ロジックは存在せず、計算は外部システムが行い CDM は監査ログ（`ResetInstruction`, `TransferInstruction`）を記録する責務境界を明確化。
- `concepts/fx_products_and_synthetic_forward.md`, `index.md`, `log.md` を更新同期。

## [2026-10-09] query | スポット・フォワード・通貨オプション・シンセティックフォワードのハルシネーション監査と是正
- 一次ソース（Rosetta DSL コードベースおよび Ingest JSON/XML 成果物）に照らし合わせ、`concepts/fx_products_and_synthetic_forward.md` における主要為替プロダクトの記載を徹底監査し、以下のハルシネーション・不整合を是正。
- **1. スポット（FX Spot）＆ プレーンフォワード（FX Forward）**:
  - `settlementType: Physical` の未出力実態の反映: Rosetta DSL（`SettlementBase`）では必須 `(1..1)` だが、FpML Ingest 変換関数（`MapFxCashSettlementToSettlementTerms`）では現物受渡時に値がセットされず、実サンプル JSON（`fx-ex01`, `fx-ex03`）では未出力（省略）となる実態を注記。
  - ISDA タクソノミ名の統一: プレーンフォワードは `Qualify_ForeignExchange_Spot_Forward` で判定されるため、実サンプル（`fx-ex03`）の出力値は `ForeignExchange_Spot_Forward` である事実を整合化。
- **2. NDF (Non-Deliverable Forward)**:
  - クラス図の型修正: `settlementCurrency` を `Unit` から正規の `string [metadata scheme]` に修正。
  - 多重度修正: `cashSettlementTerms` を `(0..*)` リスト表記に修正。
  - 情報源階層補正: `ValuationSource.informationSource` の型 `FxSpotRateSource` および内部の `primarySource InformationSource` の中抜きを是正。
- **3. プレーンな通貨オプション (Vanilla FX Option)**:
  - ストライク参照構造のハルシネーション是正: `strike.strikePrice` はインラインの直接 `Price` 型であり、外部への `@ref:scoped` アドレス参照属性は持たない事実を解明（実サンプル `fx-ex09`, `fx-ex10`, `fx-ex11` と整合化）。`tradeLot` 側には計算済名目額 `derivedQuantity` のみが入る仕様を明記。
  - `ExerciseTerms` の必須属性 `expirationTimeType (1..1)` および `expirationDate (0..*)` を反映。
  - バニラ適格性判定関数（`Qualify_ForeignExchange_VanillaOption`）において `averagingFeature only exists` が許容される一次ソース特有の包含関係を補足。
  - 現物受渡オプション（`fx-ex09`, `fx-ex10`）における `settlementType` の未出力実態を明記。
- **4. 複数受け渡し日をもつシンセティックフォワード（Strip of Synthetic Forwards）**:
  - 架空の `TradePackage` 型を全廃し、一次ソースの正規表現である `ExecutionDetails.packageReference`（型: `IdentifiedList`）およびイベントレベルの `packageInformation`（型: `IdentifiedList`）に是正。
  - 単一 Trade 複数 Payout 構造（アプローチ 1）の致命的制約（ISDA タクソノミ推論脱落、`Create_Exercise` の `tradeLot only-element` ハードコードによるライフサイクル処理破綻）を明記し、実務的には `IdentifiedList` によるマルチ Trade 構造（アプローチ 2）が事実上唯一の整合解である結論を提示。
  - 一次ソースにシンセティックフォワードやオプション複数戦略の完全サンプルは存在せず、FpML `<strategy>`（`fx-ex23-straddle`, `fx-ex25`）は Ingest 未実装のため `incomplete-products` に隔離されている事実を裏どり。
- **5. 権利行使後の派生生成（Physical Exercise によるスポット生成）**:
  - `Create_NonTransferableProduct`（L568-578）が `underlier` と `payerReceiver` のみをセットし、受渡期日（`settlementTerms`）を設定しない不完全な実装にとどまっている一次ソースのコード制約を客観的に注記。
- `concepts/fx_products_and_synthetic_forward.md`, `index.md`, `log.md` を更新同期。

