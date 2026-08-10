# FINOS Common Domain Model (CDM) 総合ナビゲーションガイド・目次 (`CDM_INDEX.md`)

`common-domain-model` リポジトリに含まれる Rosetta (Rune) DSL ファイル群（145ファイル）および Java コード（手動実装・自動生成）を、用途や目的に応じて効率的に探索・解析するためのインデックスガイドです。

---

## 1. ディレクトリ構造と主要構成要素

```
common-domain-model/
└── rosetta-source/
    └── src/
        ├── main/
        │   ├── rosetta/           # Rosetta (Rune) DSL モデル定義ファイル（本体：145ファイル）
        │   ├── java/              # 手動作成された Java コード（Guice モジュール、Qualification ハンドラー等）
        │   └── resources/         # 設定ファイル、コードリスト、関数評価用 Descriptor JSON 等
        ├── generated/
        │   └── java/              # Rosetta DSL から自動生成された Java クラス群
        └── test/                  # Java / DSL のテストコードとリソース
```

---

## 2. ファイル命名規則と階層サフィックスの役割

Rosetta DSL ファイルは `[ドメイン]-[サブドメイン]-[種類].rosetta` という統一的な命名規則に従っています。

### 2.1 接尾辞（サフィックス）による機能分類

| サフィックス | 内容・役割 | 代表的なファイル例 | 参照すべきタイミング |
|---|---|---|---|
| **`-type.rosetta`** | データ構造・型定義 (`type`, `choice`, `metaFields`) | [product-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta) | オブジェクトの属性、フィールド、構造を確認したい時 |
| **`-func.rosetta`** | ビジネスロジック・計算関数・マッピング・評価規約 (`func`) | [event-common-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-common-func.rosetta) | イベント処理、計算ロジック、判定規則を解読したい時 |
| **`-enum.rosetta`** | 列挙型定義 (`enum`) | [base-datetime-enum.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-enum.rosetta) | 選択可能な値の一覧や定数コードを確認したい時 |
| **`-desc.rosetta`** | ドメインの説明・注釈・スコープ定義 (`annotation`) | [product-desc.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-desc.rosetta) | ドメインの全体概要やスコープを確認したい時 |

### 2.2 接頭辞（プレフィックス）によるドメイン分類

- **`base-`**: 基礎データ型（日時、営業日、日数計算、数学関数、当事者、法人識別子、資産共通データ）
- **`product-`**: 金融商品モデル（金利・株式・FX・コモディティ・クレジットのデリバティブ定義、ペイアウト、決済、スケジュール、自動商品分類）
- **`event-`**: ライフサイクル・取引イベント（約定、清算、ノベーション、解約、アロケーション、状態遷移、ポジション管理）
- **`legaldocumentation-`**: 法的契約文書（ISDA/ICMA/ISLAマスターアグリーメント、Credit Support Annex (CSA)、取引追記条件）
- **`observable-`**: 市場観測データ（参照金利 (FRO)、SOFR/EURIBOR 複利計算、評価額、観察イベント）
- **`ingest-fpml-`**: 外部標準データ取り込み（FpML XML メッセージから CDM オブジェクトへのマッピング関数群）
- **`margin-schedule-`**: マージン計算・Initial Margin / Variation Margin スケジュール規則

---

## 3. 目的別（ユースケース別）ファイル検索ガイド

知りたい機能やビジネス上の目的に応じて、最優先で参照すべきファイルをまとめたナビゲーション表です。

### 3.1 金融商品・経済条件 (Product Modeling & Economic Terms)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **金利スワップ (IRS) / 浮動・固定金利レッグ** | [product-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)<br>[product-asset-floatingrate-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-floatingrate-type.rosetta) | `InterestRatePayout`, `FloatingRateSpecification` |
| **クレジット・デリバティブ (CDS)** | [product-template-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta)<br>[base-staticdata-asset-credit-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-asset-credit-type.rosetta) | `CreditDefaultPayout`, `ProtectionTerms` |
| **株式デリバティブ・オプション (Equity / Option)** | [product-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)<br>[product-template-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta) | `EquityPayout`, `OptionPayout` |
| **コモディティ商品** | [base-staticdata-asset-commodity-enum.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-asset-commodity-enum.rosetta)<br>[product-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta) | `CommodityPayout`, `Commodity` |
| **支払スケジュール・計算期間・リセット日** | [product-common-schedule-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-common-schedule-type.rosetta)<br>[product-common-schedule-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-common-schedule-func.rosetta) | `PaymentSchedule`, `CalculationPeriodDates` |
| **決済条件・受渡方法** | [product-common-settlement-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-common-settlement-type.rosetta)<br>[product-common-settlement-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-common-settlement-func.rosetta) | `SettlementTerms`, `CashSettlementTerms` |
| **商品適格性・自動分類 (Product Qualification)** | [product-qualification-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta) | `isQualifyingProduct`, `Qualify_` |

### 3.2 取引イベント・ライフサイクル (Business Events & Lifecycle)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **取引イベント定義 (Execution, Clearing, Novation, Termination 等)** | [event-common-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta) | `BusinessEvent`, `TradeState`, `Instruction` |
| **イベント発生・状態更新ロジック** | [event-common-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-common-func.rosetta) | `Create_Execution`, `Process_Allocation` |
| **イベント自動判定 (Event Qualification)** | [event-qualification-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-qualification-func.rosetta) | `Qualify_BusinessEvent`, `isQualifyingEvent` |
| **ワークフロー・オーケストレーション** | [event-workflow-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-workflow-type.rosetta)<br>[event-workflow-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-workflow-func.rosetta) | `WorkflowStep`, `EventInstruction` |
| **ポジション・残高管理** | [event-position-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-position-type.rosetta)<br>[event-position-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/event-position-func.rosetta) | `Position`, `PortfolioState` |

### 3.3 FpML XML メッセージ取り込み (Ingestion Mapping)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **ヘッダー・当事者・共通データの取り込み** | [ingest-fpml-confirmation-common-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-common-func.rosetta)<br>[ingest-fpml-confirmation-party-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-party-func.rosetta) | `Ingest_FpML_Confirmation` |
| **特定商品別 FpML マッピング (全33ファイル)** | [ingest-fpml-confirmation-product-swap-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-swap-func.rosetta)<br>[ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta)<br>[ingest-fpml-confirmation-product-fxoption-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-fxoption-func.rosetta) など | `ingest-fpml-confirmation-product-*.rosetta` |

### 3.4 法的文書・契約・担保 (Legal Documentation & Margin)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **ISDA / ICMA / ISLA マスターアグリーメント** | [legaldocumentation-master-isda-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-master-isda-type.rosetta)<br>[legaldocumentation-master-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-master-type.rosetta) | `MasterAgreement`, `MasterConfirmation` |
| **CSA (Credit Support Annex) / 担保契約** | [legaldocumentation-csa-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-csa-type.rosetta)<br>[legaldocumentation-csa-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-csa-func.rosetta) | `EligibleCollateral`, `CollateralValuation` |
| **マージンスケジュール (IM / VM)** | [margin-schedule-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/margin-schedule-type.rosetta)<br>[margin-schedule-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/margin-schedule-func.rosetta) | `InitialMarginSchedule`, `VariationMargin` |

### 3.5 市場データ・参照金利 (Observables & Market Rates)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **FRO (Floating Rate Option / 参照金利インデックス)** | [observable-asset-fro-enum.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-enum.rosetta)<br>[observable-asset-fro-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-type.rosetta) | `FloatingRateOptionEnum`, `SOFR`, `EURIBOR`, `TONA` |
| **金利計算・複利・Term Rate 計算** | [observable-asset-calculatedrate-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-func.rosetta)<br>[observable-asset-calculatedrate-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-type.rosetta) | `CalculateFloatingRate`, `CompoundedIndex` |
| **価格・評価・単価・数量 (PriceQuantity)** | [observable-asset-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-type.rosetta)<br>[observable-asset-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-func.rosetta) | `Price`, `Quantity`, `Observable` |

### 3.6 基礎データ・共通ユーティリティ (Base Types & Datetime)

| 目的・知りたいこと | 優先参照ファイル | 補足キーワード・型名 |
|---|---|---|
| **営業日・カレンダー・日数計算 (Day Count)** | [base-datetime-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-type.rosetta)<br>[base-datetime-daycount-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-daycount-func.rosetta) | `BusinessCenterEnum`, `DayCountFractionEnum` |
| **当事者・法人識別子 (Party & LEI)** | [base-staticdata-party-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-party-type.rosetta)<br>[base-staticdata-identifier-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-identifier-type.rosetta) | `Party`, `PartyRole`, `LegalEntity` |
| **数学・端数処理 (Rounding)** | [base-math-type.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-math-type.rosetta)<br>[base-math-func.rosetta](../common-domain-model/rosetta-source/src/main/rosetta/base-math-func.rosetta) | `Rounding`, `ArithmeticOperationEnum` |

---

## 4. Rosetta DSL ↔ Java 自動生成コードの構造対応

### 4.1 手動実装 Java コード (`src/main/java`)

- **ランタイム設定**: [CdmRuntimeModule.java](../common-domain-model/rosetta-source/src/main/java/org/finos/cdm/CdmRuntimeModule.java)（Guice モジュール）
- **自動分類判定エンジン**: [org/finos/cdm/qualify](../common-domain-model/rosetta-source/src/main/java/org/finos/cdm/qualify)
  - `EconomicTermsQualificationHandler.java`: 商品適格性のハンドラー
  - `BusinessEventQualificationHandler.java`: イベント適格性のハンドラー

### 4.2 Rosetta DSL と自動生成 Java クラス (`src/generated/java`) の対応法則

Rosetta DSL のパッケージ宣言 `namespace cdm.product.template` は Java パッケージ `cdm.product.template.*` にそのまま対応します。

1 つの `type` 定義（例: `Payout`）から生成される構成品：
- **`Payout`** (Interface): データ読み取り用インターフェース
- **`Payout.PayoutBuilder`** (Builder Interface): インミュータブルオブジェクトの生成・編集用
- **`functions/`**: DSL 内の `func` に対応する Java クラス（`evaluate(...)` メソッドを実装）
- **`validation/`**: フィールドチェックや制約評価を行うバリデータクラス

---

## 5. 高速探索・検索テクニック

### 5.1 ファイル名での絞り込み規則
- 商品構造: `../common-domain-model/rosetta-source/src/main/rosetta/product-*.rosetta`
- 取引イベント: `../common-domain-model/rosetta-source/src/main/rosetta/event-*.rosetta`
- 法的文書: `../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-*.rosetta`
- FpML変換: `../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-*.rosetta`

### 5.2 目的のキーワード検索パターン (`grep_search` 推奨クエリ)
- **型定義の探索**: `Query: "type <型名>"` (例: `type Payout`, `type TradeState`)
- **関数定義の探索**: `Query: "func <関数名>"` (例: `func Create_Execution`, `func Qualify_`)
- **列挙型の探索**: `Query: "enum <列挙型名>"` (例: `enum DayCountFractionEnum`)
- **FpML変換ツリーの探索**: `Query: "ingest-fpml"` または `Query: "FpML"`
