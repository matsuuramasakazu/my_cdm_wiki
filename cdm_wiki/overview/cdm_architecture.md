---
title: "CDM システムアーキテクチャ & コード生成規則"
category: "overview"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [architecture, rosetta, java, guice]
---

# CDM システムアーキテクチャ & コード生成規則

本ドキュメントでは、FINOS Common Domain Model の全体的なディレクトリレイアウトと、Rosetta DSL 定義と自動生成 Java コード間の構造的対応法則について解説します。

---

## 1. ディレクトリ構造

```
../common-domain-model/
└── rosetta-source/
    └── src/
        ├── main/
        │   ├── rosetta/           # Rosetta DSL 定義ファイル（本体：145ファイル）
        │   ├── java/              # 手動作成された Java コード（Guice モジュール、Qualification ハンドラー等）
        │   └── resources/         # 設定ファイル、コードリスト、JSON デスクリプタ等
        ├── generated/
        │   └── java/              # Rosetta DSL から自動生成された Java クラス群
        └── test/                  # Java / DSL のテストコード
```

---

## 2. Rosetta DSL ↔ Java 自動生成対応規則

Rosetta のパッケージ宣言は Java パッケージに 1:1 で対応します：
- DSL: `namespace cdm.product.template`
- Java: `cdm.product.template.*`

DSL 内の 1 つの `type` 定義（例: `Payout`）から生成される構造：
1. **インターフェース**: `Payout` - データ読み取り用インターフェース
2. **Builder インターフェース**: `Payout.PayoutBuilder` - オブジェクト生成・編集用の Builder
3. **`functions/` サブパッケージ**: DSL 内の `func` に対応する Java クラス（`evaluate(...)` メソッドを実装）
4. **`validation/` サブパッケージ**: フィールドチェックや制約チェックを行うバリデータクラス

---

## 3. 手動実装 Java 拡張 (`src/main/java`)

Rosetta DSL 単体では表現できない処理やフレームワーク結合を担う全 42 ファイル（43 クラス）の手動 Java 実装群です。

1. **ネイティブ関数実装 (`cdm.*.functions.*Impl.java`)**: 28 ファイル
   - 日時・カレンダー計算（`cdm.base.datetime.functions`: 11 ファイル）
   - 数学・丸め・ベクトル演算（`cdm.base.math.functions`: 6 ファイル）
   - FpML データ抽出・キー生成（`cdm.ingest.fpml.*`: 6 ファイル）
   - スケジュール計算 & OpenGamma Strata 連携（`cdm.product.common.schedule.functions`: 5 ファイル）
2. **証券貸借・決済ワークフロー (`cdm.security.lending.functions`)**: 5 ファイル
   - 新規・返却決済ワークフロー実行（`RunNewSettlementWorkflow`, `RunReturnSettlementWorkflow` 等）
3. **自動分類ハンドラー & エンジン (`org.finos.cdm.qualify`)**: 3 ファイル
   - `EconomicTermsQualificationHandler.java`: 商品適格性判定エンジン
   - `BusinessEventQualificationHandler.java`: イベント適格性判定エンジン
   - `CdmQualificationHandlerProvider.java`: ハンドラープロバイダー
4. **フレームワーク DI & ランタイム設定 (`org.finos.cdm.*`)**: 3 ファイル
   - `CdmRuntimeModule.java`: Guice 依存性注入モジュール
   - `CdmReferenceConfig.java`: 参照解決・ハッシュ設定
   - `ResourcesUtils.java`: クラスパス内リソース読み込み
5. **市場観測プロバイダ & コードリスト (`cdm.observable.*`, `org.finos.cdm.codelist`)**: 3 ファイル

詳細なクラス一覧とメトリクスについては [rosetta_dsl_inventory.md](rosetta_dsl_inventory.md) を参照してください。

