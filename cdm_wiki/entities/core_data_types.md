---
title: "主要データ型 & エンティティリファレンス"
category: "entities"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [entities, data-types, Rosetta, TradeState, BusinessEvent, Payout]
---

# 主要データ型 & エンティティリファレンス

本ページでは、CDM の金融商品モデルおよびイベントモデルで横断的に使用される主要な Rosetta `type` 定義について解説します。

---

## 1. 取引 & イベント関連エンティティ

- **`TradeState`**: 取引の現在状態、経済条件、ポジション、運用ステータスを追跡するルート型 ([event-common-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta))。
- **`BusinessEvent`**: 状態遷移、命令、取引履歴をカプセル化するイベント構造 ([event-common-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta))。

---

## 2. 商品 & ペイアウト関連エンティティ

- **`Payout`**: 各アセットクラスのペイアウト（`InterestRatePayout`, `CreditDefaultPayout`, `EquityPayout`, `CommodityPayout`, `OptionPayout`）を格納する抽象ポリモーフィック構造 ([product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta))。

---

## 3. 基礎エンティティ

- **`Party` & `LegalEntity`**: 当事者情報、法人識別子 (LEI)、ロールの表現 ([base-staticdata-party-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-staticdata-party-type.rosetta))。
- **`PriceQuantity`**: 価格スケジュールと数量概念を結びつける二重表現構造 ([observable-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-type.rosetta))。
