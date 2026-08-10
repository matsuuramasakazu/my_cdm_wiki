---
title: "金融商品モデリング & 経済条件"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [products, irs, cds, equity, commodity, qualification]
---

# 金融商品モデリング & 経済条件

CDM は、モジュール化された `Payout` 型および経済条件仕様を用いて、金融商品やデリバティブ取引をモデル化します。

---

## 1. 主要アセットクラス別モデルと参照ファイル

| アセットクラス / 商品 | 最優先参照ファイル | 主要な型・インターフェース |
|---|---|---|
| **金利スワップ (IRS)** | [product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)<br>[product-asset-floatingrate-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-floatingrate-type.rosetta) | `InterestRatePayout`, `FloatingRateSpecification` |
| **クレジット・デリバティブ (CDS)** | [product-template-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta)<br>[base-staticdata-asset-credit-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-asset-credit-type.rosetta) | `CreditDefaultPayout`, `ProtectionTerms` |
| **株式デリバティブ & オプション** | [product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta)<br>[product-template-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-template-type.rosetta) | `EquityPayout`, `OptionPayout` |
| **コモディティ** | [base-staticdata-asset-commodity-enum.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-asset-commodity-enum.rosetta)<br>[product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta) | `CommodityPayout`, `Commodity` |

---

## 2. スケジュール & 決済条件

- **支払・計算スケジュール**: [product-common-schedule-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-common-schedule-type.rosetta) にて `PaymentSchedule` や `CalculationPeriodDates` として定義。
- **決済条件**: [product-common-settlement-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-common-settlement-type.rosetta) にて `SettlementTerms` や `CashSettlementTerms` として定義。

---

## 3. 商品自動分類エンジン (Product Qualification)

金融商品の自動タクソノミ分類は [product-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta) 内の `isQualifyingProduct` および `Qualify_` 関数群により実装されています。
