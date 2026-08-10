---
title: "Rosetta 関数: 自動判定 & 計算"
category: "functions"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [functions, func, qualification, calculation, math]
---

# Rosetta 関数: 自動判定 & 計算

本ページでは、ビジネスロジック、商品/イベント自動判定、計算ルーチンを実行する Rosetta `func` 定義について解説します。

---

## 1. 商品 & イベント自動判定関数 (Qualification Functions)

- **商品自動分類 (Product Qualification)**: [product-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta) 内の `isQualifyingProduct` および `Qualify_` 関数群。ペイアウト構造を動的に解析し、タクソノミラベル（例: `InterestRate:IRSwap:FixedFloat`）を付与。
- **イベント自動判定 (Event Qualification)**: [event-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-qualification-func.rosetta) 内の `Qualify_BusinessEvent` および `isQualifyingEvent` 関数群。ペロード指示を ISDA イベントカテゴリ（Execution, Novation, Allocation など）へと自動分類。

---

## 2. 金利計算 & ユーティリティ

- **浮動金利計算**: [observable-asset-calculatedrate-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/observable-asset-calculatedrate-func.rosetta) の `CalculateFloatingRate`。
- **数学・端数処理**: [base-math-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-math-func.rosetta) の `ArithmeticOperationEnum` および端数処理ヘルパー。
