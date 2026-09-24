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
