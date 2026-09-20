---
title: "市場観測データ、参照金利 (FRO) & 市場データ"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-09-20"
tags: [rates, fro, sofr, euribor, tona, compounding, daycount, observation_type]
---

# 市場観測データ、参照金利 (FRO) & 市場データ

CDM は、市場価格データ、参照金利インデックス (FRO)、金利複利計算規則、および日数計算規約をモデル化しています。

---

## 1. 参照金利インデックス (Floating Rate Option: FRO)

- **参照インデックス一覧**: [observable-asset-fro-enum.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-enum.rosetta) (`FloatingRateOptionEnum`: SOFR, EURIBOR, TONA, LIBOR 等)。
- **インデックス定義構造**: [observable-asset-fro-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-type.rosetta) にて定義。
- **観測種別の自動判定**:
  - [observable-asset-fro-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-func.rosetta) の `DetermineObservationType` 関数により、指定された FRO および計算条件から観測種別（`FloatingRateIndexPeriodObservationTypeEnum`）を自動判定します。

---

## 2. 複利計算 & 日数計算 (Day Count Fraction)

- **金利計算関数**: [observable-asset-calculatedrate-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-func.rosetta) (`CalculateFloatingRate`, `CompoundedIndex`)。
- **日数計算規約**: [base-datetime-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-type.rosetta) および [base-datetime-daycount-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-daycount-func.rosetta) (`DayCountFractionEnum`, `BusinessCenterEnum`)。
- **営業日・カレンダー演算**: [base-datetime-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-func.rosetta) による営業日シフト・休日判定。
