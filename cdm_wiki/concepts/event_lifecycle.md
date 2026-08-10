---
title: "取引イベント & ライフサイクル"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [events, lifecycle, execution, clearing, novation, allocation, position]
---

# 取引イベント & ライフサイクル

CDM は、取引の状態遷移、アロケーション、ノベーション、清算、ポジション調整を表す統一イベントモデルを提供します。

---

## 1. イベント分類 & 状態管理

- **イベント定義**: [event-common-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-type.rosetta) にて管理。中心となる型は `BusinessEvent`, `TradeState`, `Instruction`。
- **状態遷移関数**: [event-common-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-func.rosetta) にて `Create_Execution`, `Process_Allocation` などとして実装。

---

## 2. イベント適格性判定 & ワークフロー

- **イベント自動判定 (Event Qualification)**: ペイロードが特定の ISDA ビジネスイベントに適合するかを [event-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-qualification-func.rosetta) の `Qualify_BusinessEvent`, `isQualifyingEvent` にて判定。
- **ワークフローオーケストレーション**: ワークフローのステップ遷移は [event-workflow-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-workflow-type.rosetta) の `WorkflowStep`, `EventInstruction` にて定義。
- **ポジション管理**: ポートフォリオレベルの残高・ポジション追跡は [event-position-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-position-type.rosetta) の `Position`, `PortfolioState` にて定義。
