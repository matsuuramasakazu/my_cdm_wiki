---
name: cdm-navigator
description: >-
  FINOS Common Domain Model (CDM) の Rosetta DSL コードベース（140+ファイル）および Java 生成クラス群を探索、特定、分析する際に使用するスキル。
---

# CDM ナビゲーター スキル

本スキルは、FINOS Common Domain Model (CDM) の大規模な Rosetta DSL コードベース（`common-domain-model/rosetta-source/src/main/rosetta/` 配下の 140+ ファイル）および Java クラス群を迷わず高速に探索・特定・分析するためのガイドです。

---

## 🗺️ 探索の基本原則

1. **一次ナビゲーションインデックス**:
   - 必ず [CDM_INDEX.md](../../../cdm_wiki/CDM_INDEX.md) を起点として構造を把握します。
2. **命名規則によるファイル特定**:
   - Rosetta DSL ファイル名は `<domain>-<subdomain>-<type|func|enum|desc>.rosetta` という厳密なプレフィックス・サフィックス規則に従っています。
3. **不可変性の遵守**:
   - `common-domain-model/` 内のファイルは読み取り専用です。

---

## 📂 ドメインプレフィックス & サフィックス早見表

### 1. ドメインプレフィックス

| ドメイン | 対象領域 | 主要ファイル例 |
|---|---|---|
| **`product-`** | デリバティブ商品定義、ペイアウト、スケジュール、決済条件、商品自動判定 | `product-asset-type.rosetta`, `product-template-type.rosetta`, `product-qualification-func.rosetta` |
| **`event-`** | ライフサイクルイベント、約定、清算、契約更改、ポジション管理、ワークフロー | `event-common-type.rosetta`, `event-common-func.rosetta`, `event-workflow-type.rosetta` |
| **`legaldocumentation-`** | ISDA/ICMA/ISLA マスター契約、CSA 担保契約、契約条項 | `legaldocumentation-csa-type.rosetta`, `legaldocumentation-master-isda-type.rosetta` |
| **`observable-`** | 市場データ、参照金利（SOFR/TONA等）、価格、インデックス、コーポレートアクション | `observable-asset-type.rosetta`, `observable-asset-fro-enum.rosetta` |
| **`ingest-fpml-`** | FpML XML メッセージからの Ingestion マッピング（全33ファイル） | `ingest-fpml-confirmation-common-func.rosetta`, `ingest-fpml-confirmation-product-swap-func.rosetta` |
| **`base-`** | 日時計算、数値計算、当事者データ、識別子、コードリスト等の基盤定義 | `base-datetime-type.rosetta`, `base-math-func.rosetta`, `base-staticdata-party-type.rosetta` |
| **`margin-schedule-`** | 規制証拠金（Initial Margin / Variation Margin）計算スケジュール | `margin-schedule-func.rosetta`, `margin-schedule-type.rosetta` |

### 2. サフィックス種別

- **`-type.rosetta`**: データ構造（`type` 定義、属性、多重度 `(1..1)`, `(0..*)`、条件 `condition`）。
- **`-func.rosetta`**: ビジネスロジック・計算処理・マッピング処理（`func` 定義、`inputs`, `output`, `assign-output`）。
- **`-enum.rosetta`**: 列挙型定義（`enum` 定義、値一覧、シノニム定義）。
- **`-desc.rosetta`**: ドメイン名前空間の記述・メタデータ定義。

---

## 🔍 Rosetta DSL 構文クイックリファレンス

Rosetta (Rune) DSL を読み解く際の主要構文：

```rosetta
// 1. 型定義 (Type)
type TradeState:
    trade Trade (1..1)                    // 必須 (多重度 1..1)
    state State (0..1)                    // 任意 (多重度 0..1)
    resetHistory ResetHistory (0..*)      // リスト (多重度 0..*)

// 2. 制約条件 (Condition)
condition TradeChoice:
    optional choice trade, instruction

// 3. 関数定義 (Function)
func Create_Execution:
    inputs:
        instruction ExecutionInstruction (1..1)
    output:
        event BusinessEvent (1..1)
    
    assign-output event -> instruction:
        instruction

// 4. 商品・イベントの自動適格性判定 (Qualify)
func Qualify_InterestRateSwap:
    inputs:
        economicTerms EconomicTerms (1..1)
    output:
        is_qualify boolean (1..1)
```

---

## 🎯 ユースケース別 クイック探索レシピ

### Q1: 金利スワップ (IRS) の金利計算や固定/変動レグの構造を調べたい
1. `common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta` を参照（`InterestRatePayout`, `FixedPrice`, `FloatingRate`）。
2. `product-common-schedule-type.rosetta` で計算期間 (`CalculationPeriodDates`) や支払スケジュールを確認。
3. `product-asset-floatingrate-func.rosetta` で浮動金利の計算ロジックを確認。

### Q2: 取引ライフサイクル（成約から決済、更改）のフローを調べたい
1. `event-common-type.rosetta` で `BusinessEvent`, `TradeState`, `Instruction` の型構造を確認。
2. `event-common-func.rosetta` で `Create_Execution`, `Create_Novation`, `Create_Allocation` などのライフサイクル関数を確認。
3. `event-workflow-type.rosetta` で複数パーティ間のワークフローステップ（`WorkflowStep`）を確認。

### Q3: FpML XML からのデータ抽出・変換ロジックを調べたい
1. 全体共通: `ingest-fpml-confirmation-common-func.rosetta`
2. 商品別: `ingest-fpml-confirmation-product-<product_name>-func.rosetta`（例: `ingest-fpml-confirmation-product-swap-func.rosetta`）
3. 参照解決: `ingest-fpml-confirmation-party-func.rosetta`
