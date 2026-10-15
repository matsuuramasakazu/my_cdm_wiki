---
name: cdm-workflowstep-validator
description: >-
  FINOS CDM の WorkflowStep JSON（ライフサイクルイベント、業務イベント、提案ステップ）が CDM 公式エンジン仕様に適合しているかを 5 レベル（構文、内部参照、DSL データルール、イベント適格性認定）で完全検証・自律修正するためのスキル。
---

# CDM WorkflowStep バリデータ スキル (`cdm-workflowstep-validator`)

本スキルは、FINOS Common Domain Model (CDM) における `WorkflowStep`（ライフサイクルイベント、業務イベント、提案・受付ステップ）の JSON ファイルを作成・変更した際に、CDM 公式 Java エンジン（**CDM 7.x: v7.5.0** および **CDM 6.x: v6.29.0**）を用いて 100% 厳格に検証し、エラーを自律修正するためのガイドです。

---

## 🎯 トリガー条件（いつ使うか）

エージェントは以下のいずれかの作業を行う際、**必ず本スキルを起動して検証を実行**しなければなりません：
1. `WorkflowStep` JSON を新規作成した時。
2. 既存の `WorkflowStep` JSON を編集・更新した時。

---

## 🛠️ 検証コマンド（実行手順）

ディスパッチャスクリプトを実行します。エージェントはバージョンを意識する必要はなく、対象の JSON ファイルパスを指定するだけで、スクリプトが CDM 7.x / 6.x の両公式エンジンを自動プローブ（試行判定）して最適な検証を実施します：

```powershell
python .agents/skills/cdm-workflowstep-validator/scripts/validate_workflowstep.py <対象JSONファイルへのパス>
```

### オプション（バージョン明示指定）
特定の CDM データモデルバージョンで検証することがあらかじめ決まっている場合は、フラグを指定できます：
```powershell
python .agents/skills/cdm-workflowstep-validator/scripts/validate_workflowstep.py --version 7 <対象JSON>
python .agents/skills/cdm-workflowstep-validator/scripts/validate_workflowstep.py --version 6 <対象JSON>
```

---

## 🔍 検証深度（Layer 1〜5 完全検証）

バリデータは以下の 5 つの検証レイヤーを実行します：

1. **Layer 1 & 2: JSON 構文・プロパティ名・型・必須カーディナリティ**
   - 未知のフィールド名（タイポ・スペルミス）、不正な Enum 定数、多重度違反（`1..1` の欠落）を検出。
   - Rune JSON（CDM v7+）および Legacy Rosetta JSON（CDM 6.x / 7.x）の双方に対応。
2. **Layer 3: 内部参照解決（Reference Resolution）**
   - `meta.globalKey` と `meta.reference` / `href` のポインタ整合性を解決。
3. **Layer 4: Rosetta/Rune DSL データルール・条件制約（Data Rules / Conditions）**
   - Rosetta DSL で宣言された `condition`、`choice` ルール、日付整合性、計算整合性ルールを Java 公式バリデータ（`RosettaTypeValidator`）で完全検証。
4. **Layer 5: イベント適格性認定（Event Qualification）と自動突合**
   - CDM の `QualifyProcessorStep` を駆動し、イベント構造から適格性関数（例: `Qualify_Reset`, `Qualify_Exercise` 等）を実行。
   - JSON 内で宣言されたイベント名（`eventQualifier`）と実際の認定結果を自動突合。

---

## 📊 レポートの読み解き方（超コンパクト・高密度出力）

バリデータはトークン効率を最大化した超コンパクトなヘッダーおよびエラー詳細を出力します：

### 合格時（PASS）の出力例
```text
STATUS   : PASS (Exit Code: 0)
MODEL    : CDM 7.x (v7.5.0)
QUALIFIED: Reset (MATCH)
```
- **Exit Code 0**: 全データルールに適合し、イベント適格性も合致。自律修正は不要です。作業完了と判断してください。

### 不合格時（FAIL）の出力例
```text
STATUS   : FAIL (Exit Code: 1)
TARGET   : CDM 7.x (v7.5.0)
FAILURES :
[1] Path  : WorkflowStep.proposedEvent.instruction(0).primitiveInstruction.execution
    Rule  : ExecutionInstruction (CARDINALITY)
    Reason: 'executionDetails' is a required field but does not exist.
[2] Path  : WorkflowStep.eventIdentifier(0)
    Rule  : IdentifierIssuerChoice (DATA_RULE)
    Reason: One and only one field must be set of 'issuerReference', 'issuer'. No fields are set.
```
- **Exit Code 1**: ルール違反または適格性不一致。`TARGET` に示されたバージョンの `FAILURES` を修正対象としてください。

---

## 🔄 自律修正ループ（Fix Loop SOP）

`STATUS: FAIL` が返された場合、エージェントは以下の標準手順に従って JSON を自律修正します：

1. **Failure の内容確認**:
   - `Path`: JSON 内の修正対象ノード・配列インデックス。
   - `Rule`: 違反した Rosetta/Rune DSL のルール名（CARDINALITY または DATA_RULE）。
   - `Reason`: 修正すべき条件（例: 必須フィールドの欠落、Choice 条件の不成立）。
2. **Rosetta DSL ソースの確認（一次情報照会）**:
   - スキル `cdm-navigator` を活用し、該当モデル・ルールの DSL ファイルを探索：
     - イベント/ワークフロー: `common-domain-model/rosetta-source/src/main/rosetta/event-*-type.rosetta`
     - 商品/ペイアウト: `product-*-type.rosetta`
     - 基盤型/日時/識別子: `base-*-type.rosetta`
3. **JSON の修正と再検証**:
   - 修正後、再度 `python validate_workflowstep.py ...` を実行し、`STATUS: PASS (Exit Code: 0)` になるまで反復。

---

## 📦 バリデータ本体の再ビルド手順

本バリデータはローカルリポジトリに依存せず、**Maven Central Repository** から公式リリース版（v7: `7.5.0`, v6: `6.29.0`）を直接ダウンロードしてビルドされます。

ソースコードやバージョン設定を変更した場合のビルド手順：

```powershell
mvn -f .agents/skills/cdm-workflowstep-validator/pom.xml package -DskipTests
```
成功すると `.agents/skills/cdm-workflowstep-validator/target/` 配下に `cdm-validator-v7.jar` と `cdm-validator-v6.jar` が一括生成されます。
