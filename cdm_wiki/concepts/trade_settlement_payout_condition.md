---
title: "Trade の SettlementPayout 条件ルール（condition SettlementPayout）と Rosetta DSL 構文解析"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta"
  - "../../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-party-type.rosetta"
last_updated: "2026-10-28"
tags: [cdm, rosetta, trade, settlementpayout, condition, datarule, validation, buyer_seller, fx]
---

# Trade の SettlementPayout 条件ルール（condition SettlementPayout）と Rosetta DSL 構文解析

FINOS Common Domain Model (CDM) における約定データ型 [`Trade`](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta#L295) には、取引データの整合性を保証するためのバリデーション条件（`condition`、いわゆる **Data Rule**）が定義されています。

本ドキュメントでは、[`event-common-type.rosetta`](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta#L310-L315) の 310 行目に定義されている `condition SettlementPayout` の構文、動作ロジック、業務的背景、および Rosetta DSL の読み方について詳細に解説します。

---

## 1. 対象コードとルールの概要

### 1.1 一次ソースコード

```rosetta
// event-common-type.rosetta (L310-L315)
condition SettlementPayout: <"When the product uses a settlement payout, both buyer and seller party roles, and a price, must exist.">
    if SettlementPayoutOnlyExists(product -> economicTerms -> payout)
    then partyRole -> role contains PartyRoleEnum -> Buyer
            and partyRole -> role contains PartyRoleEnum -> Seller
            and tradeLot -> priceQuantity -> price exists
```

### 1.2 ルールの要約
> **「対象プロダクトが決済ペイアウト（SettlementPayout）単独で構成される取引（例: FX Spot、FX Forward、証券現物など）である場合、取引当事者として買手（Buyer）と売手（Seller）のロールが両方指定され、かつ約定価格（Price）が存在しなければならない。」**

金利スワップ（IRS）などの「支払側（Payer）／受取側（Receiver）」の関係性で記述される取引とは異なり、直物・先渡等の受渡決済取引では「誰が買い、誰が売り、いくらで約定したか」という関係性が不可欠であるため、このデータルールによって不完全な取引データの生成を抑止しています。

---

## 2. Rosetta DSL 構文のステップ別分解

Rosetta DSL の `condition` は、**「ガード節（`if <前提条件>`）」** と **「表明節（`then <制約式>`）」** で構成される条件付きバリデーションルールです。

### 2.1 ガード節（Trigger / Prerequisite）
```rosetta
if SettlementPayoutOnlyExists(product -> economicTerms -> payout)
```
- **評価タイミング**: この条件式が `true` を返した場合にのみ、`then` 以降の検証が実行されます（`false` の場合はルールをパス・スキップします）。
- **`product -> economicTerms -> payout`**:
  - `Trade` は [`TradableProduct`](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta#L321) を継承（`extends`）しています。
  - `product`（`NonTransferableProduct`）の契約経済条件 `economicTerms` に含まれる `payout`（`Payout (0..*)` のコレクション）をナビゲーション演算子 `->` で抽出します。
- **関数 [`SettlementPayoutOnlyExists`](../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta#L1981)**:
  ```rosetta
  func SettlementPayoutOnlyExists: <"At least one SettlementPayout exists and no other payouts exist.">
      inputs:
          payouts Payout (0..*)
      output:
          result boolean (1..1)

      set result:
          payouts
              extract SettlementPayout exists
              then all = True
              then default False
  ```
  - **`extract SettlementPayout exists`**: 各 `Payout` 要素について、ポリモーフィックな具象型として `SettlementPayout` が存在するか（インスタンス化されているか）を boolean リストとして抽出します。
  - **`then all = True`**: リスト内の全要素が `True` であること（すなわち、すべての payout が `SettlementPayout` であり、他の `InterestRatePayout` や `OptionPayout` 等が一切混ざっていないこと）を検証します。
  - **`then default False`**: `payouts` が空の場合は `False` を返します。
  - **判定結果**: 純粋な外為スポット・フォワードや現物受渡取引の場合に `True` となります。

### 2.2 表明節（Assertion / Invariant）
ガード節が `True` の場合、`then` の後にある 3 つの制約すべて（`and` 結合）を満たす必要があります。

#### ① 買手ロールの必須性
```rosetta
partyRole -> role contains PartyRoleEnum -> Buyer
```
- `Trade.partyRole`（[`PartyRole (0..*)`](../../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-party-type.rosetta#L169)）から全要素の `role`（`PartyRoleEnum`）をコレクションとして収集します。
- そのコレクションの中に、列挙値 `PartyRoleEnum -> Buyer` が少なくとも 1 つ含まれている（`contains`）ことを要求します。

#### ② 売手ロールの必須性
```rosetta
and partyRole -> role contains PartyRoleEnum -> Seller
```
- 同様に、`partyRole -> role` の中に `PartyRoleEnum -> Seller` が少なくとも 1 つ含まれていることを要求します。

#### ③ 約定価格の必須性
```rosetta
and tradeLot -> priceQuantity -> price exists
```
- `TradableProduct` から継承された `tradeLot`（[`TradeLot (1..*)`](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta#L317)）内の `priceQuantity`（`PriceQuantity (1..*)`）から `price`（`Price (0..*)`）を参照します。
- `price` が空でなく 1 つ以上存在する（`exists`）ことを要求します。

---

## 3. 金融業務・CDM モデリングにおける背景

### 3.1 デリバティブ（Swap） vs 直渡・先渡（Settlement）の対比

| 観点 | スワップ型取引（IRS, CDS, Equity Swap） | 受渡・決済型取引（FX Spot, FX Forward, 証券現物） |
|---|---|---|
| **主要ペイアウト** | `InterestRatePayout`, `CreditDefaultPayout`, `PerformancePayout` | `SettlementPayout` |
| **取引の本質** | 双方向の将来キャッシュフローや利息の交換 | 資産・通貨の受渡と対価（約定代金）の決済 |
| **当事者関係の表現** | `Payer` / `Receiver`（支払側／受取側）<br>※各レグごとに独立指定 | **`Buyer` / `Seller`（買手／売手）**<br>※取引全体における売買関係の確定 |
| **価格（Price）の性格** | 固定金利（例: 0.5%）、スプレッド、指数レート等 | **約定価格・約定為替レート（例: 155.50 USD/JPY）** |

スワップ取引では、どちらか一方が一方的な「買手」であるとは一概に言えないため、カウンターパーティは Payer/Receiver で抽象化されます。
一方、`SettlementPayout` が単独で用いられる取引では、「誰が何をいくらで買ったか／売ったか」という片道あるいは同時決済の売買契約であるため、**Buyer / Seller のロール指定** と **Price の存在** が取引成立の前提条件となります。

---

## 4. Rosetta DSL 構文パターンの要約

| 構文要素 | 意味・役割 | 本ルールでの実例 |
|---|---|---|
| **`condition <Name>:`** | データ検証ルール（Data Rule）の宣言 | `condition SettlementPayout:` |
| **`<"説明文">`** | 自然言語ドキュメンテーション（仕様説明） | `<"When the product uses a settlement payout...">` |
| **`if <条件> then <検証>`** | 条件付き制約（ガード節）。`if` が偽なら検証スキップ | `if SettlementPayoutOnlyExists(...) then ...` |
| **`->` (Arrow)** | ナビゲーション演算子（属性参照 & リストの暗黙的 FlatMap） | `product -> economicTerms -> payout` |
| **`contains`** | リスト内に指定要素が含まれているかの判定 | `... role contains PartyRoleEnum -> Buyer` |
| **`exists`** | 属性値が存在する（non-null かつ非空）ことの判定 | `... price exists` |
| **`Enum -> Value`** | 列挙型定数へのアクセス | `PartyRoleEnum -> Buyer` |

---

## 5. 自動生成 Java コードとの関係

Rosetta DSL コンパイラ（Rune Java Generator）は、この `condition` を Java クラスへと自動コンパイルします：
- **生成クラス**: `TradeValidator` または `TradeSettlementPayoutDataRule`。
- **実行挙動**: CDM のデシリアライズ時（Ingestion時）やライフサイクルイベント生成時に `validate` メソッドが自動実行されます。
- **エラー処理**: `SettlementPayoutOnlyExists` が `true` にもかかわらず `Buyer` や `Seller`、`price` が欠落していた場合、バリデーション結果として `ValidationResult.failure` が出力され、無効な取引オブジェクトとして検出されます。
