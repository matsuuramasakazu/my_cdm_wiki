---
title: "法的契約文書、CSA & マージンスケジュール"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [legal, isda, csa, margin, collateral]
---

# 法的契約文書、CSA & マージンスケジュール

CDM は、マスターアグリーメント、Credit Support Annex (CSA) 規則、規制マージン計算スケジュールをデジタルモデル化しています。

---

## 1. マスターアグリーメント & 法的条件

- **ISDA / ICMA / ISLA 枠組み**: [legaldocumentation-master-isda-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-master-isda-type.rosetta) および [legaldocumentation-master-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-master-type.rosetta) にてモデル化。主要型は `MasterAgreement`, `MasterConfirmation`。

---

## 2. Credit Support Annex (CSA) & 担保マージン

- **適格担保 & CSA 規則**: [legaldocumentation-csa-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/legaldocumentation-csa-type.rosetta) の `EligibleCollateral`, `CollateralValuation` にて定義。
- **マージン計算 (IM / VM)**: [margin-schedule-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/margin-schedule-type.rosetta) の `InitialMarginSchedule`, `VariationMargin` にて定義。
