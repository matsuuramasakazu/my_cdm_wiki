---
title: "市場観測データ、参照金利 (FRO) & 市場データ"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [rates, fro, sofr, euribor, tona, compounding, daycount]
---

# 市場観測データ、参照金利 (FRO) & 市場データ

CDM は、市場価格データ、参照金利インデックス (FRO)、金利複利計算規則、および日数計算規約をモデル化しています。

---

## 1. 参照金利インデックス (Floating Rate Option: FRO)

- **参照インデックス一覧**: [observable-asset-fro-enum.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-enum.rosetta) (`FloatingRateOptionEnum`: SOFR, EURIBOR, TONA, LIBOR)。
- **インデックス定義構造**: [observable-asset-fro-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-fro-type.rosetta) にて定義。

---

## 2. 複利計算 & 日数計算 (Day Count Fraction)

- **金利計算関数**: [observable-asset-calculatedrate-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-func.rosetta) (`CalculateFloatingRate`, `CompoundedIndex`)。
- **日数計算規約**: [base-datetime-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-type.rosetta) および [base-datetime-daycount-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-daycount-func.rosetta) (`DayCountFractionEnum`, `BusinessCenterEnum`)。
