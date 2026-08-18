---
title: "Rosetta 関数: 自動判定 & 計算"
category: "functions"
sources:
  - "../CDM_INDEX.md"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/event-qualification-func.rosetta"
last_updated: "2026-08-18"
tags: [functions, func, qualification, calculation, math, isda_taxonomy]
---

# Rosetta 関数: 自動判定 & 計算

本ページでは、FINOS CDM におけるビジネスロジック、商品自動分類（Product Qualification）、イベント自動判定（Event Qualification）、および各種計算ルーチンを実行する Rosetta `func` 定義について詳しく解説します。

---

## 1. 商品自動分類エンジン (Product Qualification)

### 1.1 設計思想: コンポーザブルな動的判定
従来の金融システムでは、取引データ自身に「金利スワップ」「NDF」などの固定された商品名ラベルを持たせることが一般的でした。しかし、各金融機関や規制当局ごとに用語や分類粒度が異なり、データ不整合の原因となっていました。

FINOS CDM では、商品は独立した構成要素（`Payout` レグ群、スケジュール、決済条件等）の組み合わせ（`EconomicTerms`）によって完全に記述されます（**Composability 原則**）。
**商品自動分類（Product Qualification）** は、取引の経済条件（`EconomicTerms`）を入力とし、その構造をルールベースで解析して、対応する **ISDA Taxonomy (v1 / v2)** などの標準タクソノミラベルを動的かつ決定論的に付与する仕組みです。

Rosetta DSL では、`isProduct root EconomicTerms;` ディレクティブおよび各判定関数に付与された `[qualification Product]` アノテーションによって言語レベルでサポートされています。

---

### 1.2 ISDA Taxonomy に基づく4階層判定アーキテクチャ

CDM の商品判定は、ISDA Taxonomy v2 の分類体系に準拠した4つの階層で構成されています：

```
Level 1: 資産クラス (Asset Class)       [InterestRate, ForeignExchange, Credit, Equity, Commodity]
   │
Level 2: 基本商品 (Base Product)        [IRSwap, Fra, CrossCurrency, Forward, Option, Swap など]
   │
Level 3: サブ商品 (Sub Product)         [FixedFloat, FixedFixed, Basis, SingleName, Index, Basket など]
   │
Level 4: 取引特性/指標 (Transaction)     [OIS, ZeroCoupon, YoY, NDF, Variance, Volatility など]
```

| 階層 | 主な判定関数例 | 判定基準・着目属性 |
|---|---|---|
| **Level 1: Asset Class** | `Qualify_AssetClass_InterestRate`<br>`Qualify_AssetClass_ForeignExchange`<br>`Qualify_AssetClass_Equity` | 含まれる `Payout` の型（`InterestRatePayout`, `SettlementPayout`, `PerformancePayout` 等）やアンダーライヤーの資産クラス |
| **Level 2: Base Product** | `Qualify_BaseProduct_IRSwap`<br>`Qualify_BaseProduct_CrossCurrency`<br>`Qualify_BaseProduct_Fra` | レグ数、支払頻度（複数期か単一期か）、通貨の一致/相違、インフレ仕様の有無 |
| **Level 3: Sub Product** | `Qualify_SubProduct_FixedFloat`<br>`Qualify_SubProduct_FixedFixed`<br>`Qualify_SubProduct_Basis` | レグごとの金利仕様（`FixedRateSpecification`, `FloatingRateSpecification`）や原資産の構成 |
| **Level 4: Transaction** | `Qualify_Transaction_OIS`<br>`Qualify_Transaction_ZeroCoupon`<br>`Qualify_Transaction_YoY` | 参照金利インデックス（SOFR/TONA等）、支払タイミング（満期一括/年次リセット）、決済方式（差金決済/現物） |

---

### 1.3 具体的な分類例と判定ロジック

以下は、[product-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta) における主要商品の判定ロジックの実装例です。

#### 例 1: バニラ固定/変動金利スワップ (`InterestRate_IRSwap_FixedFloat`)
- **タクソノミ**: `InterestRate:IRSwap:FixedFloat`
- **判定条件**:
  1. `Qualify_BaseProduct_IRSwap`: `InterestRatePayout` が2つ存在し、支払期日が複数あり、単一通貨であり、インフレ仕様がない。
  2. `Qualify_SubProduct_FixedFloat`: 1つの固定金利レグ（`FixedRateSpecification`）と1つの変動金利レグ（`FloatingRateSpecification`）で構成。
  3. `Qualify_Transaction_ZeroCoupon = False`: 満期一括払い（ゼロクーポン）ではない。
  4. `Qualify_Transaction_OIS = False`: 浮動金利インデックスが OIS 指標（SOFR, TONA 等）ではない（例: ターム物 EURIBOR / TIBOR）。

```rosetta
func Qualify_InterestRate_IRSwap_FixedFloat:
    [qualification Product]
    inputs:
        economicTerms EconomicTerms (1..1)
    output:
        is_product boolean (1..1)
    set is_product:
        Qualify_BaseProduct_IRSwap(economicTerms) = True
            and Qualify_SubProduct_FixedFloat(economicTerms) = True
            and Qualify_Transaction_ZeroCoupon(economicTerms) = False
            and Qualify_Transaction_OIS(economicTerms) = False
```

---

#### 例 2: OIS 金利スワップ (`InterestRate_IRSwap_FixedFloat_OIS`)
- **タクソノミ**: `InterestRate:IRSwap:FixedFloat:OIS`
- **判定条件**:
  - 固定/変動スワップの基本構造を満たしつつ、`Qualify_Transaction_OIS` が `True`（変動レグの `floatingRateIndex` が `USD_SOFR_OIS_Compound`, `JPY_TONA_OIS_COMPOUND`, `EUR_EuroSTR_OIS_Compound` などの翌日物金利複利インデックス列挙値に合致）。

---

#### 例 3: 通貨スワップ (`InterestRate_CrossCurrency_FixedFloat`)
- **タクソノミ**: `InterestRate:CrossCurrency:FixedFloat`
- **判定条件**:
  - 2つの `InterestRatePayout` において、元本通貨が異なる（`currency distinct count = 2`）、または為替連動元本（`fxLinkedNotionalSchedule`）が設定されている。

```rosetta
func Qualify_BaseProduct_CrossCurrency:
    inputs:
        economicTerms EconomicTerms (1..1)
    output:
        is_product boolean (1..1)
    set is_product:
        Qualify_AssetClass_InterestRate(economicTerms) = True
            and economicTerms -> payout as InterestRatePayout count = 2
            and (economicTerms -> payout as InterestRatePayout -> priceQuantity -> quantitySchedule -> unit -> currency
                    distinct count = 2
                or (...))
```

---

#### 例 4: 為替ノンデリバラブル・フォワード (`ForeignExchange_NDF`)
- **タクソノミ**: `ForeignExchange:NDF`
- **判定条件**:
  - `Payout` が単一の `SettlementPayout` のみで構成される。
  - `settlementTerms -> cashSettlementTerms` が **存在する**（差金決済であること）。
  - ※ 差金決済条件が存在しない場合は、通常の直物/先物（`ForeignExchange_Spot_Forward`）として分類される。

```rosetta
func Qualify_ForeignExchange_NDF:
    [qualification Product]
    inputs:
        economicTerms EconomicTerms (1..1)
    output:
        is_product boolean (1..1)
    set is_product:
        Qualify_AssetClass_ForeignExchange(economicTerms) = True
            and economicTerms -> payout only-element as SettlementPayout exists
            and economicTerms -> payout as SettlementPayout -> settlementTerms -> cashSettlementTerms exists
```

---

#### 例 5: スワップション (`InterestRate_Option_Swaption`)
- **タクソノミ**: `InterestRate:Option:Swaption`
- **判定条件**:
  - `Payout` が単一の `OptionPayout` のみ。
  - オプションの原資産（`underlier`）が `Product`（金融商品）であり、その原資産を再帰的に評価すると `Qualify_AssetClass_InterestRate`（金利商品）に適合する。

```rosetta
func Qualify_InterestRate_Option_Swaption:
    [qualification Product]
    inputs:
        economicTerms EconomicTerms (1..1)
    output:
        is_product boolean (1..1)
    set is_product:
        Qualify_AssetClass_InterestRate(economicTerms) = True
            and economicTerms -> payout only-element as OptionPayout exists
            and Qualify_AssetClass_InterestRate(
                    economicTerms -> payout as OptionPayout -> underlier as Product ->> economicTerms
                        only-element
                ) = True
```

---

#### 例 6: 株式トータルリターンスワップ (`EquitySwap_TotalReturnBasicPerformance_SingleName`)
- **タクソノミ**: `Equity:Swap:TotalReturnBasicPerformance:SingleName`
- **判定条件**:
  - 1つの `PerformancePayout`（価格リターン `priceReturnTerms` と配当リターン `dividendReturnTerms` を含む）と 1つの `InterestRatePayout`（資金調達金利レグ）で構成。
  - 原資産（アンダーライヤー）が単一の株式（Single Name Security）。
  - オプション権利が存在しない。

---

## 2. イベント自動判定関数 (Event Qualification)

商品分類と同様に、取引ライフサイクル上で発生するビジネスイベントも [event-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-qualification-func.rosetta) の `Qualify_BusinessEvent` 関数群によって動的に自動判定されます。

- **新規約定 (Execution)**: 指示が `ExecutionInstruction` を含み、新規ポジションを生成。
- **契約更改 (Novation)**: 指示が `NovationInstruction` を含み、一方の契約が消滅（Transferor）し、第三者（Transferee）との新契約が生成。
- **配分 (Allocation)**: 一括取引（Block Trade）から複数口座への配分取引を生成。
- **金利リセット (Reset)**: 浮動金利指標の観測値（Observation）に基づいて次期支払額を確定。

---

## 3. 金利計算 & 数学ユーティリティ

- **浮動金利計算**: [observable-asset-calculatedrate-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-func.rosetta) の `CalculateFloatingRate`。SOFR/TONA等のデイリールックバック複利計算、スプレッド加算、フロア適用などを実行。
- **数学・端数処理**: [base-math-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-math-func.rosetta) の `ArithmeticOperationEnum` および端数処理ヘルパー。

---

## 4. 商品自動分類の実務的メリット

1. **規制報告の自動化 (Automated Trade Reporting)**:
   - CFTC、EMIR、JFSA 等の報告規制で求められる UPI（Unique Product Identifier）や ISDA タクソノミコードを、取引データから決定論的に自動導出。
2. **システム間相互運用の向上**:
   - フロント、ミドル、バック、清算機関（CCP）間で異なる商品呼称を使用していても、CDM 上の構造から同一の商品として正確に照合可能。
3. **データ品質の向上**:
   - 入力データの商品名ラベルと実際のキャッシュフロー構造（レグ構成）の乖離・設定ミスを自動検知。

