---
title: "プレーン金利スワップ（Vanilla IRS）の Trade 型構造 & クラス図リファレンス"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
  - "common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta"
  - "common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta"
  - "common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta"
  - "common-domain-model/rosetta-source/src/main/rosetta/product-asset-floatingrate-type.rosetta"
  - "common-domain-model/rosetta-source/src/main/rosetta/product-common-schedule-type.rosetta"
last_updated: "2026-08-19"
tags: [irs, swap, vanilla, trade, tradestate, class_diagram, rosetta_dsl]
---

# プレーン金利スワップ（Vanilla IRS）の Trade 型構造 & クラス図リファレンス

FINOS Common Domain Model (CDM) におけるバニラ金利スワップ（Vanilla Interest Rate Swap: 固定金利レグ vs 浮動金利レグ）の `TradeState` / `Trade` の完全なデータ構造と Rosetta DSL 型定義のクラス図リファレンスです。

---

## 1. 全体構造クラス図 (Mermaid Class Diagram)

```mermaid
classDiagram
    direction TB

    class TradeState {
        +Trade trade
        +State state
        +ResetHistory[0..*] resetHistory
        +TransferHistory[0..*] transferHistory
    }

    class Trade {
        +TradeIdentifier[1..*] tradeIdentifier
        +date tradeDate
        +TimeZone tradeTime
        +Party[0..*] party
        +PartyRole[0..*] partyRole
        +ExecutionDetails executionDetails
        +ContractDetails contractDetails
    }

    class TradableProduct {
        +NonTransferableProduct product
        +TradeLot[1..*] tradeLot
        +Counterparty[2..2] counterparty
        +AncillaryParty[0..*] ancillaryParty
    }

    class NonTransferableProduct {
        +ProductIdentifier[0..*] identifier
        +ProductTaxonomy[0..*] taxonomy
        +EconomicTerms economicTerms
    }

    class EconomicTerms {
        +AdjustableOrRelativeDate effectiveDate
        +AdjustableOrRelativeDate terminationDate
        +BusinessDayAdjustments dateAdjustments
        +Payout[2..2] payout
        +CalculationAgent calculationAgent
    }

    class Payout {
        <<choice>>
        InterestRatePayout (Fixed Leg)
        InterestRatePayout (Floating Leg)
    }

    class PayoutBase {
        <<abstract>>
        +PayerReceiver payerReceiver
        +ResolvablePriceQuantity priceQuantity
        +PrincipalPayments principalPayment
        +SettlementTerms settlementTerms
    }

    class InterestRatePayout {
        +RateSpecification rateSpecification
        +DayCountFractionEnum dayCountFraction
        +CalculationPeriodDates calculationPeriodDates
        +PaymentDates paymentDates
        +ResetDates resetDates
        +CompoundingMethodEnum compoundingMethod
    }

    class RateSpecification {
        <<choice>>
        FixedRateSpecification
        FloatingRateSpecification
    }

    class FixedRateSpecification {
        +RateSchedule rateSchedule
    }

    class FloatingRateSpecification {
        +InterestRateIndex rateOption
        +SpreadSchedule spreadSchedule
        +StrikeSchedule capRateSchedule
        +StrikeSchedule floorRateSchedule
        +NegativeInterestRateTreatmentEnum negativeInterestRateTreatment
        +Rounding finalRateRounding
    }

    class CalculationPeriodDates {
        +AdjustableDate effectiveDate
        +AdjustableDate terminationDate
        +CalculationPeriodFrequency calculationPeriodFrequency
        +BusinessDayAdjustments calculationPeriodDatesAdjustments
    }

    class PaymentDates {
        +Frequency paymentFrequency
        +PayRelativeToEnum payRelativeTo
        +BusinessDayAdjustments paymentDatesAdjustments
    }

    class ResetDates {
        +ResetRelativeToEnum resetRelativeTo
        +RelativeDateOffset fixingDates
        +ResetFrequency resetFrequency
    }

    class TradeLot {
        +PriceQuantity[1..*] priceQuantity
        +Identifier[0..*] lotIdentifier
    }

    class PriceQuantity {
        +NonNegativeQuantitySchedule quantity
        +PriceSchedule price
        +Observable observable
    }

    TradeState *-- Trade : 1. trade
    Trade --|> TradableProduct : extends
    TradableProduct *-- NonTransferableProduct : product
    TradableProduct *-- TradeLot : tradeLot (Notional & Rates)
    NonTransferableProduct *-- EconomicTerms : economicTerms
    EconomicTerms *-- Payout : payout (Fixed & Floating Legs)
    InterestRatePayout --|> PayoutBase : extends
    Payout ..> InterestRatePayout : 2 Legs
    InterestRatePayout *-- RateSpecification : rateSpecification
    RateSpecification ..> FixedRateSpecification : Fixed Leg
    RateSpecification ..> FloatingRateSpecification : Floating Leg
    InterestRatePayout *-- CalculationPeriodDates : calculationPeriodDates
    InterestRatePayout *-- PaymentDates : paymentDates
    InterestRatePayout *-- ResetDates : resetDates (Floating only)
    TradeLot *-- PriceQuantity : priceQuantity (Global Notional)
```

---

## 2. プレーン IRS の 4 階層モデリング詳細

### 2.1 第 1 階層：ライフサイクル & 取引ヘッダー (`TradeState` / `Trade`)
- **`TradeState`** (`cdm.event.common.TradeState`):
  - CDM のルートエンティティ。取引の最新状態（`Trade`）とそのライフサイクル進捗（`State`）をカプセル化。
- **`Trade`** (`cdm.event.common.Trade` extends `TradableProduct`):
  - `tradeIdentifier`: 取引識別子（UTI / USI 等）。
  - `tradeDate`: 約定日（Trade Date）。
  - `party`: 取引に関与する法人エンティティ一覧（`LegalEntity`, `Party`）。
  - `partyRole`: 当事者の役割（`Buyer`, `Seller`, `Broker`, `Custodian` 等）。

### 2.2 第 2 階層：取引可能商品 & カウンターパーティ (`TradableProduct`)
- **`counterparty`** (`cdm.base.staticdata.party.Counterparty`):
  - 取引の 2 当事者（`Party1`, `Party2`）を定義し、抽象的なロールと実際の `Party` 参照をバインド。
- **`tradeLot`** (`cdm.product.template.TradeLot`):
  - 取引のロット単位の価格・想定元本（`PriceQuantity`）を保持。
  - `quantity`: 想定元本額（Notional Amount、例: 50,000,000 EUR）。
- **`product`** (`cdm.product.template.NonTransferableProduct`):
  - `taxonomy`: ISDA 分類（`InterestRate:IRSwap:FixedFloat`）。
  - `economicTerms`: 経済条件・契約本体。

### 2.3 第 3 階層：経済条件 & ペイアウト (`EconomicTerms` / `Payout`)
- **`EconomicTerms`** (`cdm.product.template.EconomicTerms`):
  - スワップ契約全体の有効期間（`effectiveDate`, `terminationDate`）および共通営業日補正。
  - `payout`: プレーン IRS では **2 つの `InterestRatePayout`**（Fixed Leg と Floating Leg）を配列で保持。

### 2.4 第 4 階層：金利レグ仕様 (`InterestRatePayout`)
- **共通基盤属性 (`PayoutBase`)**:
  - `payerReceiver`: 支払当事者（`payer`）と受取当事者（`receiver`）（例: Fixed Leg は `Party1` 払 / `Party2` 受、Floating Leg は `Party2` 払 / `Party1` 受）。
  - `priceQuantity`: `TradeLot` の想定元本を参照する `ResolvablePriceQuantity`。
- **固定金利レグ (Fixed Leg)**:
  - `rateSpecification` $\rightarrow$ **`FixedRateSpecification`**:
    - `rateSchedule`: 固定金利（例: `0.025` = 2.5% p.a.）。
  - `dayCountFraction`: 日数計算基準（例: `30/360`, `30E/360`, `ACT/365.FIXED`）。
  - `calculationPeriodDates`: 利息計算期間（半年ごと `6M`, 年1回 `1Y` 等）。
  - `paymentDates`: 支払スケジュール（期末払い `CalculationPeriodEndDate`）。
- **浮動金利レグ (Floating Leg)**:
  - `rateSpecification` $\rightarrow$ **`FloatingRateSpecification`**:
    - `rateOption`: 参照金利インデックス（`EURIBOR-6M`, `USD-SOFR-COMPOUND`, `JPY-TONA` 等）。
    - `spreadSchedule`: スプレッド（例: +0.0010 = 10bps）。
    - `negativeInterestRateTreatment`: マイナス金利時の処理方法（`NegativeInterestRateTreatmentEnum -> ZeroRate` 等）。
  - `dayCountFraction`: 日数計算基準（例: `ACT/360`）。
  - `calculationPeriodDates`: 利息計算期間。
  - `paymentDates`: 支払スケジュール。
  - `resetDates`: **利率決定日（Fixing/Reset スケジュール）**（例: 各計算期間開始日の 2 営業日前 `periodMultiplier: -2, dayType: Business`）。

---

## 3. 関連ドキュメント
- [product_modeling.md](product_modeling.md): 商品モデリング & ISDA 分類体系
- [event_lifecycle.md](event_lifecycle.md): 取引ライフサイクルと TradeState 状態遷移
- [core_data_types.md](../entities/core_data_types.md): 主要エンティティ & データ型リファレンス
- [fpml_ingestion.md](fpml_ingestion.md): FpML XML から CDM へのマッピング対応
