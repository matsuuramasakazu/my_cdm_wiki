---
title: "TradableProduct における product と tradeLot の分離構造 & 元本参照解決"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
  - "vanilla_irs_trade_structure.md"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-common-settlement-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-payment-func.rosetta"
last_updated: "2026-09-16"
tags: [cdm, rosetta, tradableproduct, tradelot, nontransferableproduct, notional, swap, principal_payment]
---

# TradableProduct における product と tradeLot の分離構造 & 元本参照解決

FINOS Common Domain Model (CDM) において、店頭デリバティブ取引（スワップ等）を `TradeState` / `Trade` で表現する際、根幹をなすのが `TradableProduct` の構成要素である **`product` (`NonTransferableProduct`)** と **`tradeLot` (`TradeLot`)** の関係性です。

本ドキュメントでは、`TradableProduct` における商品条項と約定ロットの関心事の分離設計、スコープ内参照（`@ref:scoped`）による元本・価格の解決メカニズム、および元本交換（`principalPayment`）の実額表現仕様について解説します。

---

## 1. TradableProduct における構成要素の役割定義

| 構成要素 | データ型 | 役割と保持する情報 |
|---|---|---|
| **`product`** | `NonTransferableProduct` | **金融商品の契約条項・利息計算ルール（Terms & Conditions / Payout）の定義**。<br>当事者や約定金額から抽象化された不変の計算ルール構造（レグ構成、金利指標、計算期間、Day Count、元本交換ルール等）を保持。 |
| **`tradeLot`** | `TradeLot` | **取引ロットごとの約定条件（Price & Quantity）**。<br>`quantity` には**名目元本額の実額（例: 1,000,000,000 JPY）**が、`price` には約定価格（固定金利、スプレッド等）が直接格納される。 |
| **両者の結合** | スコープ内ポインタ参照 | **`@ref:scoped` によるアドレス解決**。<br>`product` 側の各レグ（Payout）が `tradeLot` 側の元本・金利を参照して計算する。 |
| **`principalPayment`** | `PrincipalPayments` | **実際の元本受渡金額そのもの（実額、`Money` 型）**。<br>期初・期末の元本交換において、授受されるキャッシュ金額の実額を表現。 |

---

## 2. `TradableProduct` の設計思想（関心事の分離）

CDM において、取引可能な商品（`TradableProduct`）は以下のように定義されています（[`product-template-type.rosetta:L321-L325`](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta#L321-L325)）：

```rosetta
type TradableProduct: <"Definition of a product as ready to be traded, i.e. included in an execution or contract, by associating a specific price and quantity to this product plus an (optional) mechanism for any potential future quantity adjustment.">
    product NonTransferableProduct (1..1) <"The underlying product to be included in a contract or execution.">
    tradeLot TradeLot (1..*) <"Specifies the price, quantity and effective date of each trade lot, when the same product may be traded multiple times in different lots with the same counterparty...">
    counterparty Counterparty (2..2)
    ancillaryParty AncillaryParty (0..*)
    adjustment NotionalAdjustmentEnum (0..1)
```

### 2.1 商品定義と約定条件の直交性
スワップのレグ仕様（変動金利インデックス、利息計算期間、Day Count Fraction、営業日補正ルールなど）は、約定金額（10億円か100億円か）や約定金利（0.01%か0.02%か）とは独立して成立します。
CDM では `product` に商品の計算骨格を閉じ込め、`tradeLot` に約定ごとの具体的な経済数値（Price & Quantity）を持たせることで、高いモジュール性と再利用性を実現しています。

### 2.2 ロットの複数性（`tradeLot (1..*)`）とライフサイクル管理
`tradeLot` が配列（`1..*`）として設計されている理由は、**同一プロダクトに対する追加約定（Trade Increase）や一部解約（Trade Decrease / Partial Unwind）をロット単位で独立管理するため**です。
- **増額（Trade Increase / 追加ロット）**: 同一のスワップ契約条件（同じ `product`）のまま後から追加約定した場合、`tradeLot` リストに新たなロット（有効日・約定金利・追加元本）を追加します。
- **減額（Trade Decrease / Partial Unwind）**: 対象の `tradeLot` の数量（`quantity`）を減額します。
- これにより、商品本体の定義（`product`）を改変することなく、取引ライフサイクルの状態遷移をスマートに記録できます。

---

## 3. 金利スワップ（Swap）での参照解決メカニズム

金利スワップでは、`product` 側の各レグ（`InterestRatePayout`）がどのように `tradeLot` の名目元本と結びつくのかを、実際の CDM JSON 出力構造から確認します。

### 3.1 構造イメージ（参照ポインタ関係）

```mermaid
graph TD
    TP[TradableProduct] --> P[product: NonTransferableProduct]
    TP --> TL[tradeLot: TradeLot]

    subgraph Product側（契約条項）
        P --> ET[economicTerms]
        ET --> Payout1[InterestRatePayout: 固定レグ]
        Payout1 --> RPQ1[priceQuantity: ResolvablePriceQuantity]
        RPQ1 -- "@ref:scoped = quantity-1" --> Q1
        Payout1 --> RS[rateSchedule]
        RS -- "@ref:scoped = price-1" --> PR1
    end

    subgraph TradeLot側（約定数値）
        TL --> PQ[priceQuantity]
        PQ --> PR1["price: price-1 (value: 0.01 / 1.0%)"]
        PQ --> Q1["quantity: quantity-1 (value: 1,000,000,000 JPY)"]
    end
```

### 3.2 実際の JSON 表現

#### (1) `product` 側（レグの定義）：数値を直書きせず参照ポインタを指定
```json
{
  "@type": "cdm.product.asset.InterestRatePayout",
  "payerReceiver": { "payer": "Party1", "receiver": "Party2" },
  "priceQuantity": {
    "quantitySchedule": {
      "@ref:scoped": "quantity-1"   // <-- tradeLot 側の quantity-1 を参照
    }
  },
  "rateSpecification": {
    "@type": "cdm.product.asset.FixedRateSpecification",
    "rateSchedule": {
      "price": {
        "@ref:scoped": "price-1"      // <-- tradeLot 側の price-1 を参照
      }
    }
  }
}
```

#### (2) `tradeLot` 側（ロットの実体）：名目元本額と価格の実額を定義
```json
"tradeLot": [ {
  "priceQuantity": [ {
    "price": [ {
      "@key:scoped": "price-1",
      "value": 0.01,
      "priceType": "InterestRate"
    } ],
    "quantity": {
      "@key:scoped": "quantity-1",
      "value": 1000000000,           // <-- 名目元本額の実額（10億円）
      "unit": {
        "currency": { "@data": "JPY" }
      }
    }
  } ]
} ]
```

---

## 4. `principalPayment`（元本交換）の実額表現

通貨スワップ等で期初・期中・期末に元本交換（Principal Exchange）が発生する場合、`product` 側の `InterestRatePayout` に配置される `principalPayment`（`PrincipalPayments` 型）の金額表現仕様について解説します。

### 4.1 `PrincipalPayment` の型定義（`product-common-settlement-type.rosetta`）

[`product-common-settlement-type.rosetta:L350-L356`](../../common-domain-model/rosetta-source/src/main/rosetta/product-common-settlement-type.rosetta#L350-L356) の定義：

```rosetta
type PrincipalPayment: <"Any kind of principal payments when the amount is known and thus fixed.">
    principalPaymentDate AdjustableDate (0..1)
    payerReceiver PayerReceiver (0..1)
    principalAmount Money (0..1) <"When known at the time the transaction is made, the cash amount to be paid.">
    discountFactor number (0..1)
    presentValuePrincipalAmount Money (0..1)
```

`principalAmount` の型は `Money`（数値 `value` と通貨 `currency` を持つ複合型）であり、定義コメントにも `"When known at the time the transaction is made, the cash amount to be paid."`（取引締結時に判明している場合、**支払われるキャッシュ金額そのもの**）と明記されています。

### 4.2 クロスッカレンシースワップ（CCS）での具体例（`ird-ex06-xccy-swap.json`）

期初・期末に元本交換がある通貨スワップでは、以下のように **1,000万USDの実額** が直接格納されます：

```json
"principalPayment": {
  "initialPayment": true,
  "finalPayment": true,
  "intermediatePayment": false,
  "principalPaymentSchedule": {
    "initialPrincipalPayment": {
      "principalPaymentDate": { "adjustedDate": { "@data": "1994-12-14" } },
      "payerReceiver": { "payer": "Party2", "receiver": "Party1" },
      "principalAmount": {
        "value": 10000000.00,       // <-- 1,000万USD（実額）
        "unit": { "currency": { "@data": "USD" } }
      }
    },
    "finalPrincipalPayment": {
      "principalPaymentDate": { "adjustedDate": { "@data": "1999-12-14" } },
      "payerReceiver": { "payer": "Party1", "receiver": "Party2" },
      "principalAmount": {
        "value": 10000000.00,       // <-- 1,000万USD（実額）
        "unit": { "currency": { "@data": "USD" } }
      }
    }
  }
}
```

### 4.3 Ingestion ロジックにおける実装
FpML から CDM への変換関数（[`ingest-fpml-confirmation-payment-func.rosetta:L660-L680`](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-payment-func.rosetta#L660-L680) の `MapPrincipalPayment`）でも、FpML の `principalExchangeAmount`（元本交換金額の実額）がそのまま `principalAmount` にマッピングされています：

```rosetta
func MapPrincipalPayment:
    ...
    alias amount: fpmlPrincipalExchange -> principalExchangeAmount
    set principalPayment:
        PrincipalPayment {
            principalPaymentDate: MapPrincipalPaymentDate(fpmlPrincipalExchange),
            payerReceiver: MapPrincipalPayerReceiver(...),
            principalAmount:
                Money {
                    value: if amount < 0 then amount * -1 else amount,
                    unit: UnitType { currency: MapCurrency(fpmlCurrency), ... }
                }
        }
```

---

## 5. 証券（TransferableProduct）と店頭デリバティブ（NonTransferableProduct）の比較

| 分類 | 対象商品 | 価格・数量モデル | CDM での表現 |
|---|---|---|---|
| **証券 (`TransferableProduct`)** | 株式、債券、投信、ETF | **単価（Price） × 数量（Units/Shares）**<br>例: 1口100円 × 10,000口 = 100万円 | `ConstituentWeight` や `Security` において、1口あたりの額面・株価と保有口数（Units）を掛け合わせる構造。 |
| **店頭デリバティブ (`NonTransferableProduct`)** | 金利スワップ (IRS)、通貨スワップ (CCS)、CDS | **金利/スプレッド（Rate） と 想定元本額（Notional Amount）**<br>将来キャッシュフロー交換契約 | 金利スワップ自体は分割売買される証券ではないため、**`tradeLot` の `quantity` に名目元本額そのもの（Currency 単位）を直接指定**する。 |

---

## 6. まとめ

1. **`product` (`NonTransferableProduct`)**: 取引の不変ルールである利息計算ロジックや契約条項（レグ構成、参照指標、計算期間、Day Count、元本交換ルール等）を定義する。
2. **`tradeLot` (`TradeLot`)**: 各ロットで約定した経済数値の実体（名目元本実額 `Quantity` および約定金利・スプレッド `Price`）を直接保持する。
3. **参照解決（ポインタ構造）**: `product` 側の各 Payout が `tradeLot` 側の `PriceQuantity` をスコープ内キー参照（`@ref:scoped`）することで、ルールと数値が結合される。
4. **`principalPayment`**: 元本交換金額（`principalAmount`）は比率ではなく、実際の受渡金額（`Money` 型の実額）として表現される。
5. **ロットの複数性**: `tradeLot (1..*)` により、商品条項を変更することなく Trade Increase や Partial Unwind をロット単位で追跡・管理できる。

---

## 関連ドキュメント
- [vanilla_irs_trade_structure.md](vanilla_irs_trade_structure.md): プレーン金利スワップ（Vanilla IRS）の Trade 型構造 & クラス図リファレンス
- [product_modeling.md](product_modeling.md): 商品モデリング & ISDA 分類体系
- [core_data_types.md](../entities/core_data_types.md): 主要エンティティ & データ型リファレンス
