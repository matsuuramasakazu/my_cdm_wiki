---
title: "契約日付モデリング：EconomicTerms と CalculationPeriodDates における effectiveDate / terminationDate の使い分け"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
  - "vanilla_irs_trade_structure.md"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-common-schedule-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-func.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/margin-schedule-func.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-swap-func.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta"
last_updated: "2026-09-20"
tags: [cdm, rosetta, effectivedate, terminationdate, economicterms, calculationperioddates, swap, dates, businessday]
---

# 契約日付モデリング：EconomicTerms と CalculationPeriodDates における effectiveDate / terminationDate の使い分け

FINOS Common Domain Model (CDM) において、契約の開始日（`effectiveDate`）と終了日（`terminationDate`）は、**契約全体レベル（`EconomicTerms`）** と **個別ペイアウト・レグレベル（`CalculationPeriodDates` 等）** の 2 つの異なる階層に定義されています。

本ドキュメントでは、両者のスコープの違い、金融実務に基づく使い分けの理由、FpML からのインジェスト対応、および CDM 関数における日付解決ロジック（Date Resolution）を解説します。

---

## 1. 階層とスコープの対比

| 比較項目 | `EconomicTerms` の日付 | `CalculationPeriodDates` の日付 |
|---|---|---|
| **配置階層** | `TradableProduct` $\rightarrow$ `product` $\rightarrow$ `economicTerms` | `economicTerms` $\rightarrow$ `payout` $\rightarrow$ `InterestRatePayout` $\rightarrow$ `calculationPeriodDates` |
| **スコープ** | **契約全体（Global / Contract-level）** | **個別レグ・ストリーム（Local / Leg-level）** |
| **多重度** | `(0..1)`（オプショナル） | `(0..1)`（オプショナル） |
| **定義の意味** | 契約商品全体に**一律・共通に適用される開始日および満期終了日**。 | その金利レグの**利息計算期間スケジュール（キャッシュフロー）を生成するための開始日・終了日**。 |
| **主要適用商品** | レポ（Repo / GMRA）、証券貸借（GMSLA）、CDS、リターンスワップ、コモディティスワップ | 金利スワップ（IRS）、通貨スワップ（CCS）、FRA 等の定期利息ストリーム |

---

## 2. なぜ 2 つの階層に存在するのか？（使い分けの理由）

### 2.1 全体共通日（`EconomicTerms`）の役割
Rosetta DSL の型定義コメント（[`product-template-type.rosetta:L30`](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta#L30)）には次のように明記されています：
> *"the effective and termination date and the date adjustment provisions when applying uniformily across the payout components."*
> （すべてのペイアウトコンポーネントに**一律に適用される場合**の有効日および終了日、ならびに日付調整条項）

- **単一構造の取引**: レポ（GMRA）における `Purchase Date`（買付日）と `Repurchase Date`（買戻日）、CDS における `scheduledTerminationDate`（予定満期日）など、取引全体として単一の開始・終了日が定まっている商品は、契約ルートレベルである `EconomicTerms` に配置されます。

### 2.2 レグ個別日（`CalculationPeriodDates`）が必要な理由
金利スワップ（IRS）や通貨スワップ（CCS）では、固定レグと浮動レグ、あるいは 2 通貨レグの間で、金融工学上・決済実務上の理由から**日付条件が非対称になる**ことがあります：

1. **営業日カレンダーと休日調整則（Business Center / Holiday Calendar）の相違**:
   - 例: 通貨スワップ（USD vs JPY）では、USD レグはニューヨーク/ロンドン休日で調整され、JPY レグは東京休日で調整されます。
   - 理論上の指定日（Unadjusted Date）が同じであっても、営業日調整後（Adjusted Date）の実際の利息起算日・終了日がレグ間で異なる日になります。
2. **スタブ期間（Stub Period）と計算頻度の独立性**:
   - 一方のレグが年 1 回払い（1Y）、他方が 3 ヶ月払い（3M）の場合、端数期間（Short/Long Stub）の調整やロール日の適用境界がレグごとに独立して計算されます。
3. **レグ期間が異なる変形スワップ（Staggered Swap / Differing Leg Dates）**:
   - 一方のレグが即時開始（Spot Start）し、他方のレグが将来開始（Forward Start）するスワップや、一方のレグが途中で早期終了するスワップ構造に対応するため、各レグが固有の `effectiveDate` / `terminationDate` を持つ必要があります。

---

## 3. FpML Ingestion におけるマッピング実態

FpML（Financial products Markup Language）からの取り込みロジックにおいて、商品特性に応じた明確な振り分けが行われています。

### 3.1 金利スワップ（`ingest-fpml-confirmation-product-swap-func.rosetta`）
FpML の `<swap>` スキーマでは、ルート直下に日付はなく、各 `<swapStream>` の `<calculationPeriodDates>` 配下に日付が定義されています。
そのため、CDM の Ingestion でも各レグの `CalculationPeriodDates` に日付がマッピングされ、`EconomicTerms` 側の `effectiveDate` / `terminationDate` はセットされません（`empty`）。

```rosetta
func MapSwapCalculationPeriodDates:
    ...
    set calculationPeriodDates:
        CalculationPeriodDates {
            effectiveDate: MapAdjustableDateOrAdjustedRelativeDate(
                        fpmlCalculationPeriodDates -> effectiveDate, ...
                    ),
            terminationDate: MapAdjustableOrRelativeDate(
                        fpmlCalculationPeriodDates -> terminationDate, ...
                    ),
            ...
        }
```

### 3.2 クレジットデリバティブ CDS（`ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta`）
CDS では FpML の `<generalTerms>` に契約全体の日付が定義されているため、`EconomicTerms` 側に直接マッピングされます。

```rosetta
func MapCreditDefaultSwap:
    ...
    set economicTerms:
        EconomicTerms {
            effectiveDate: MapAdjustableDate2ToAdjustableOrRelativeDate(
                        fpmlCreditDefaultSwap -> generalTerms -> effectiveDate
                    ),
            terminationDate: MapAdjustableDate2ToAdjustableOrRelativeDate(
                        fpmlCreditDefaultSwap -> generalTerms -> scheduledTerminationDate
                    ),
            ...
        }
```

---

## 4. CDM 関数における日付解決ロジック（Date Resolution）

CDM の計算関数（規制証拠金 SIMM スケジュール計算等）では、商品ごとにどちらの日付を参照すべきかを判定・解決する標準ロジックが組み込まれています（[`margin-schedule-func.rosetta`](../../common-domain-model/rosetta-source/src/main/rosetta/margin-schedule-func.rosetta)）：

### 4.1 金利スワップの有効期間抽出関数
金利スワップにおいて取引全体の有効期間を求める場合、各レグ（`InterestRatePayout`）の `CalculationPeriodDates` を走査し、開始日の最小値（`min`）と終了日の最大値（`max`）を取引全体の期間として集約・解決します：

```rosetta
func AuxiliarEffectiveDate:
    ...
    set effectiveDate:
        // 金利スワップレグの CalculationPeriodDates から開始日の最小値を抽出
        if economicTerms -> payout as InterestRatePayout -> calculationPeriodDates -> effectiveDate -> adjustableDate exists
        then (economicTerms -> payout as InterestRatePayout -> calculationPeriodDates -> effectiveDate -> adjustableDate
            extract AdjustableDateResolution
            then min)

func AuxiliarTerminationDate:
    ...
    set terminationDate:
        // 金利スワップレグの CalculationPeriodDates から終了日の最大値を抽出
        if economicTerms -> payout as InterestRatePayout -> calculationPeriodDates -> terminationDate -> adjustableDate exists
        then (economicTerms -> payout as InterestRatePayout -> calculationPeriodDates -> terminationDate -> adjustableDate
            extract AdjustableDateResolution
            then max)
```

### 4.2 汎用商品の有効期間抽出関数
CDS や Repo など全体日付を持つ商品については、`economicTerms -> effectiveDate` および `economicTerms -> terminationDate` を直接抽出します（`StandardizedScheduleDuration` 関数等）。

### 4.3 営業日調整・日付ユーティリティ関数群 (`base-datetime-func`)
CDM では、日付計算および営業日調整に関する関数型ユーティリティ（[`base-datetime-func.rosetta`](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-func.rosetta)）が標準提供されています：

- **`AdjustDateToBusinessDayConvention`**: 指定された営業日調整慣行（Following, ModifiedFollowing, Preceding, Nearest 等）に基づき日付を調整。
- **`AdjustDateToFollowingBusinessDay` / `AdjustDateToPrecedingBusinessDay`**: 休日カレンダーを参照して翌営業日・前営業日にシフト。
- **`ShiftBusinessDays`**: 指定された営業日数だけ前後にシフトする関数。
- **`GenerateCalendarDateList` / `ExpandMissingObservationDates`**: 観測期間内の全日付の展開、および休日による欠落観測日を補完するリスト生成関数。
- **Java ネイティブ実装 (`CalculationPeriodImpl.java`)**: OpenGamma Strata ライブラリとの連携および日付・期間生成ロジックが実装され、精度の高いキャッシュフロー期間算出がサポートされています。

---

## 5. 使い分けのまとめ・モデリング指針

1. **商品が定期利息ストリーム（スワップ・FRA等）を持つ場合**:
   - 各レグ固有の計算スケジュール・営業日補正を表現するため、**`CalculationPeriodDates` 側の `effectiveDate` / `terminationDate` を必須として設定**する。
   - `EconomicTerms` 側の日付はオプショナルのため、通常は省略（またはレグ共通の代表契約期間として補助的に保持）される。
2. **商品が契約全体で単一の取引期間を持つ場合（Repo, CDS, Securities Lending 等）**:
   - レグごとの期間分岐が存在しないため、契約ルートレベルである **`EconomicTerms` 側の `effectiveDate` / `terminationDate` に直接設定**する。
3. **期間計算・分析を行うシステム側の処理**:
   - `EconomicTerms` の日付が存在すればそれを参照し、スワップのようにレグ側にのみ存在する場合はレグ群の `CalculationPeriodDates` から `min(effectiveDate)` / `max(terminationDate)` を解決する設計とする。

---

## 関連ドキュメント
- [vanilla_irs_trade_structure.md](vanilla_irs_trade_structure.md): プレーン金利スワップ（Vanilla IRS）の Trade 型構造 & クラス図リファレンス
- [tradable_product_and_tradelot.md](tradable_product_and_tradelot.md): TradableProduct における product と tradeLot の分離構造 & 元本参照解決
- [product_modeling.md](product_modeling.md): 商品モデリング & ISDA 分類体系
