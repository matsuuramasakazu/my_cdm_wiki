---
name: cdm-workflowstep-validator
description: >-
  FINOS CDM の WorkflowStep JSON（ライフサイクルイベント、業務イベント、提案ステップ）が CDM 公式エンジン仕様に適合しているかを 5 レベル（構文、内部参照、DSL データルール、イベント適格性認定）で完全検証・自律修正するためのスキル。
---

# CDM WorkflowStep バリデータ スキル (`cdm-workflowstep-validator`)

本スキルは、FINOS Common Domain Model (CDM) における `WorkflowStep`（ライフサイクルイベント、業務イベント、提案・受付ステップ）の JSON ファイルを作成・変更した際に、CDM 公式 Java エンジンを用いて 100% 厳格に検証し、エラーを自律修正するためのガイドです。

---

## 🎯 トリガー条件（いつ使うか）

エージェントは以下のいずれかの作業を行う際、**必ず本スキルを起動して検証を実行**しなければなりません：
1. `cdm_wiki/samples/` 配下等に新しい `WorkflowStep` JSON を作成した時。
2. 既存の `WorkflowStep` JSON を編集・更新した時。

---

## 🛠️ 検証コマンド（実行手順）

Fat-JAR（公式 CDM ランタイム組み込み済み）を用いて、引数に検証対象の JSON ファイルパスを指定して実行します：

```powershell
java -jar .agents/skills/cdm-workflowstep-validator/target/cdm-workflowstep-validator.jar <対象JSONファイルへのパス>
```

### 実行例
```powershell
java -jar .agents/skills/cdm-workflowstep-validator/target/cdm-workflowstep-validator.jar cdm_wiki/samples/fx_lifecycle/01_observation.json
```

---

## 🔍 検証深度（Layer 1〜5 完全検証）

バリデータは以下の 5 つの検証レイヤーを自動で連続実行します：

1. **Layer 1 & 2: JSON 構文・プロパティ名・型・Enum・必須カーディナリティ**
   - 不正な JSON 構文、未知のフィールド名（タイポ・スペルミス）、不正な Enum 定数、多重度違反（`1..1` の欠落）を検出。
   - CDM v7 新形式（`@type`, `@key`, `@data` を含む Rune JSON）および Legacy Rosetta JSON の双方を自動判別。
2. **Layer 3: 内部参照解決（Reference Resolution）**
   - `meta.globalKey` と `meta.reference` / `href` のポインタ整合性を解決。
3. **Layer 4: Rosetta DSL データルール・条件制約（Data Rules / Conditions）**
   - Rosetta DSL（`.rosetta`）で宣言された `condition`、`choice` ルール、日付整合性、計算整合性ルールを Java 公式バリデータ（`RosettaTypeValidator`）で完全検証。
4. **Layer 5: イベント適格性認定（Event Qualification）と自動突合**
   - CDM の `QualifyProcessorStep` を駆動し、イベント構造から適格性関数（例: `Qualify_Reset`, `Qualify_Exercise` 等）を実行。
   - JSON 内で宣言されたイベント名（`eventQualifier` や `intent`）と実際の認定結果を自動突合。

---

## 📊 エラーレポートの読み解き方

バリデータは終了コード（Exit Code）と詳細サマリーを出力します：
- **Exit Code 0**: `Overall: PASS`（全ルール適合、イベント適格性合致）
- **Exit Code 1**: `Overall: FAIL`（構文エラー、ルール違反、適格性不一致のいずれか）

### レポート出力例
```text
======================================================================
                  CDM WORKFLOWSTEP VALIDATION REPORT                  
======================================================================
Target File : sample.json
JSON Format : Rune JSON (CDM v7+)
Overall     : FAIL (Exit Code: 1)
Step Status : Accepted (BusinessEvent present)
Total Rules : 1200 | Success: 1198 | Failures: 2
Declared Evt: Reset (Intent: CASH_SETTLEMENT)
Qualified   : [Reset]
Event Match : MATCH (Declared 'Reset' matched qualified events)
======================================================================
--- [RULE FAILURES] ---
[1] Type  : CARDINALITY
    Name  : ExecutionInstruction
    Model : ExecutionInstruction
    Path  : WorkflowStep.proposedEvent.instruction(0).primitiveInstruction.execution
    Reason: 'executionDetails' is a required field but does not exist.

[2] Type  : DATA_RULE
    Name  : IdentifierIssuerChoice
    Model : Identifier
    Path  : WorkflowStep.eventIdentifier(0)
    Reason: One and only one field must be set of 'issuerReference', 'issuer'. No fields are set.
======================================================================
```

---

## 🔄 自律修正ループ（Fix Loop SOP）

バリデーションで `Overall: FAIL` が返された場合、エージェントは以下の標準手順に従って JSON を自律修正します：

1. **Failure Type の特定**:
   - `JSON Deserialization / Unknown Property`: 未知のキー、スペルミス、不正な型。既知のプロパティ一覧を確認して修正。
   - `CARDINALITY`: `(1..1)` や `(1..*)` の必須フィールドが欠落。対象モデルの Rosetta DSL を確認して属性を追加。
   - `DATA_RULE / CHOICE_RULE`: 条件式（`condition`）の不成立。`Reason` に出力された条件ロジックを確認。
   - `MISMATCH / UNQUALIFIED`: 意図したライフサイクルイベントとして CDM に認定されていない。イベント関数の前提（Payout, PrimitiveInstruction, Quantity 等）を確認。
2. **Rosetta DSL ソースの確認（一次情報照会）**:
   - スキル `cdm-navigator` を活用し、該当モデル（`Name` や `Model`）の DSL ファイルを探索：
     - イベント/ワークフロー: `common-domain-model/rosetta-source/src/main/rosetta/event-*-type.rosetta`
     - 商品/ペイアウト: `product-*-type.rosetta`
     - 基盤型/日時/識別子: `base-*-type.rosetta`
3. **JSON の修正と再検証**:
   - 修正後、再度 `java -jar ...` を実行し、`Overall: PASS (Exit Code: 0)` になるまで反復。

---

## 📦 バリデータ本体の再ビルド手順

バリデータ CLI 本体のソースコード（`.agents/skills/cdm-workflowstep-validator/`）を変更した場合のビルド手順：

```powershell
mvn -f .agents/skills/cdm-workflowstep-validator/pom.xml package -DskipTests
```
成功すると `.agents/skills/cdm-workflowstep-validator/target/cdm-workflowstep-validator.jar` が更新されます。
