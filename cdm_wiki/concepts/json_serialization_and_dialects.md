---
title: "CDM JSON シリアライゼーション仕様 & バージョン比較 (v6.x vs v7.x)"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
  - "../../common-domain-model/docs/serialization.md"
last_updated: "2026-09-25"
tags: [cdm, json, serialization, rune, rosetta, v6, v7, jsonschema]
---

# CDM JSON シリアライゼーション仕様 & バージョン比較 (v6.x vs v7.x)

本ページでは、FINOS Common Domain Model (CDM) における JSON シリアライゼーション方式の根本的刷新（CDM v6.x 系「Legacy JSON」から CDM v7.x 系「Rune JSON」への移行）について、FpML Ingestion 出力サンプル（`ird-ex01-vanilla-swap.json`）および `cdm-json-schema`（v6.28.1 と v7.4.0）の実機検証・比較結果に基づき詳説します。

---

## 1. エグゼクティブサマリ & 主要メトリクス

CDM はバージョン 7.0.0 以降、基盤言語である Rune DSL のシリアライゼーション標準に完全移行しました。この改変により、人間に対する可読性（Human-readability）、データ容量の圧縮（Compactness）、多言語間の相互運用性（Interoperability）が大幅に向上しました。

金利スワップ（Vanilla IRS）の FpML Ingest 出力サンプル（`ird-ex01-vanilla-swap.json`）における定量的比較は以下の通りです：

| 項目 | CDM v6.28.1 (Legacy JSON) | CDM v7.4.0 (Rune JSON) | 変化率・効果 |
| :--- | :--- | :--- | :--- |
| **ファイルサイズ** | 16,625 文字 | 9,488 文字 | **約 43% 削減** |
| **総行数** (Pretty Print) | 560 行 | 316 行 | **約 44% 削減** |
| **デフォルト Object Mapper** | `RosettaObjectMapper` | `RuneJsonObjectMapper` | 新エンジン採用 |
| **メタデータ表現** | `meta: { globalKey, ... }` | `@`-prefixed 属性 (`@key`, `@data` 等) | 階層のフラット化 |
| **ポリモーフィズム** | ラッパーオブジェクト形式 | `@type` 判別プロパティ形式 | ネスト解消 |
| **未参照キー (globalKey)** | すべて無差別に出力 | 参照のない `@key` は枝刈り (Pruning) | 大幅なノイズ削減 |

---

## 2. ルートレベル構造の比較

シリアライズされたドキュメントの最上位（ルート）において、CDM v7 ではモデル名、バージョン、および完全修飾型名（FQN: Fully Qualified Type Name）が明示されるようになりました。

### CDM v6.28.1 (Legacy JSON)
ルートレベルには型情報やモデルメタデータが存在せず、ビジネスデータ（`trade`）と `meta.globalKey` のみが配置されていました。
```json
{
  "trade": {
    "product": { ... },
    "tradeLot": [ ... ],
    "party": [ ... ],
    "meta": { ... }
  },
  "meta": {
    "globalKey": "4c3b889a"
  }
}
```

### CDM v7.4.0 (Rune JSON)
`@model`、`@version`、`@type`、およびドキュメント全体の識別子 `@key` が最上位に直接記述されます。
```json
{
  "@model": "cdm",
  "@version": "7.4.0",
  "@type": "cdm.event.common.TradeState",
  "@key": "ba4f9326",
  "trade": {
    "product": { ... },
    "tradeLot": [ ... ],
    "party": [ ... ]
  }
}
```

---

## 3. メタデータアノテーション構造の刷新（`@` プレフィックス属性）

CDM v6 までは、メタデータ（キー、参照、スキーム、ロケーション等）を表現するために `meta` オブジェクトや `value` ラッパー（`FieldWithMeta` / `ReferenceWithMeta`）による多重ネストが発生していました。CDM v7 では、これらがすべて `@` プレフィックスの特別属性（Special Attributes）にフラット化されました。

### メタデータ・キーワード対応表

| 概念 | CDM v6.x (Legacy JSON) | CDM v7.x (Rune JSON) | 役割・説明 |
| :--- | :--- | :--- | :--- |
| **グローバルキー** | `meta.globalKey` | `@key` | ドキュメント内一意のハッシュ識別子 |
| **グローバル参照** | `globalReference` | `@ref` | `@key` を参照するポインタ |
| **スコープ付きキー** | `meta.location` (`scope`, `value`) | `@key:scoped` | ドキュメント内局所識別子（FpMLのid相当） |
| **スコープ付き参照**| `address` (`scope`, `value`) | `@ref:scoped` | `@key:scoped` を参照するポインタ |
| **外部キー** | `meta.externalKey` | `@key:external` | 外部システム由来の識別子（FpML partyId等） |
| **外部参照** | `externalReference` | `@ref:external` | `@key:external` を参照するポインタ |
| **メタ付き基本値** | `value` (alongside `meta`) | `@data` | スキームやキーが付与されたプリミティブ値本体 |
| **スキーム** | `meta.scheme` | `@scheme` | FpML coding-scheme などの値ドメイン定義 URI |

---

## 4. 具体例による対比

### 4.1 当事者（Party）と取引主体参照（PartyReference）

#### 【v6.28.1】
```json
// party 定義側
{
  "partyId": [
    {
      "identifier": {
        "value": "549300VBWWV6BYQOWM67",
        "meta": { "scheme": "http://www.fpml.org/coding-scheme/external/iso17442" }
      },
      "identifierType": "LEI",
      "meta": { "globalKey": "4a5d2d9f" }
    }
  ],
  "name": { "value": "Party A" },
  "meta": { "globalKey": "5bbdd746", "externalKey": "party1" }
}

// counterparty 参照側
{
  "role": "Party1",
  "partyReference": {
    "globalReference": "5bbdd746",
    "externalReference": "party1"
  }
}
```

#### 【v7.4.0】
```json
// party 定義側: meta や value ラッパーが消え、@key:external, @scheme, @data に統合
{
  "@key:external": "party1",
  "partyId": [
    {
      "identifier": {
        "@scheme": "http://www.fpml.org/coding-scheme/external/iso17442",
        "@data": "549300VBWWV6BYQOWM67"
      },
      "identifierType": "LEI"
    }
  ],
  "name": { "@data": "Party A" }
}

// counterparty 参照側: @ref:external のみで簡潔に表現
{
  "role": "Party1",
  "partyReference": {
    "@ref:external": "party1"
  }
}
```

### 4.2 ポリモーフィズム（直和型・抽象クラス）の表現

CDM における最も劇的な構造変化の一つが、ポリモーフィックな型の表現です。

- **v6.x (Wrapper Object Pattern)**: 具象クラス名をプロパティ名とするラッパー階層を挟むため、無駄なネストが2〜3階層深くなっていました。
- **v7.x (Discriminator Property Pattern)**: `@type` 属性に完全修飾型名を指定し、同一階層にフィールドを展開します。

#### 【v6.28.1 の payout】
```json
"payout": [
  {
    "InterestRatePayout": {
      "payerReceiver": { ... },
      "rateSpecification": {
        "FloatingRateSpecification": {
          "rateOption": {
            "address": { "scope": "DOCUMENT", "value": "InterestRateIndex-1" }
          },
          "meta": { "globalKey": "0" }
        }
      },
      "priceQuantity": {
        "quantitySchedule": {
          "address": { "scope": "DOCUMENT", "value": "quantity-1" }
        },
        "meta": { "globalKey": "0" }
      }
    },
    "meta": { "globalKey": "..." }
  }
]
```

#### 【v7.4.0 の payout】
```json
"payout": [
  {
    "@type": "cdm.product.asset.InterestRatePayout",
    "payerReceiver": { ... },
    "rateSpecification": {
      "@type": "cdm.product.asset.FloatingRateSpecification",
      "rateOption": {
        "@ref:scoped": "InterestRateIndex-1"
      }
    },
    "priceQuantity": {
      "quantitySchedule": {
        "@ref:scoped": "quantity-1"
      }
    }
  }
]
```

### 4.3 未参照キーの枝刈り（Pruning）

- **v6.x**: Rosetta DSL の `[metadata key]` や `[metadata id]` が付与された型は、シリアライズ時に無条件で一意なハッシュ値（`globalKey`）を生成して出力していました。このため、日付調整、営業日カレンダー、支払頻度など、どこからも参照されないフィールドにも大量の `meta: { "globalKey": "..." }` が溢れていました。
- **v7.x**: **「他の場所から `@ref` で参照されていない `@key` は出力しない」**というシリアライズ生成規則（Generation Pruning Rule）が徹底されました。その結果、必要な参照関係（例: `InterestRateIndex-1` や `party1`）のみが残り、JSON 全体のノイズが劇的に排除されました。

---

## 5. cdm-json-schema（v6.28.1 vs v7.4.0）の比較と実態

### 5.1 スキーマファイル群の比較メトリクス

`cdm_json/6.28.1/jsonschema` と `cdm_json/7.4.0/jsonschema` を網羅的に比較した結果は以下の通りです：

| 分類 | ファイル数 | 主な内容 |
| :--- | :--- | :--- |
| **v6.28.1 総ファイル数** | 1,066 | Draft-04 JSON Schema 群 |
| **v7.4.0 総ファイル数** | 1,142 | Draft-04 JSON Schema 群 |
| **両バージョンで完全一致** | 854 | 基礎的な共通型・Enum 定義 |
| **スキーマ定義に差分あり** | 120 | モデル改修（Quantity, Security, BusinessCenters 等） |
| **v7.4.0 で新規追加** | 168 | 担保管理（`cdm-legaldocumentation-csa`: 64件）、基本契約（`master`: 19件）、イベント合成（`instructioncomposition`: 17件）、静的データ（22件） |
| **v7.4.0 で削除** | 92 | 旧規制レポート（`cdm-regulation-...`: 39件）、旧CSA型（33件）、旧アセット型（7件） |

### 5.2 重要な留意点: スキーマとサンプル JSON の過渡期的非同期

実機検証の結果、**非常に重要な技術的留意点**が判明しています：

> [!WARNING]
> **v7.4.0 の `jsonschema` に収録されているスキーマ定義は、依然として Legacy JSON 形式（`FieldWithMeta...`, `ReferenceWithMeta...`, 型名ラッパー構造）のままです。**
> 
> すなわち、`cdm_json/7.4.0/jsonschema` には `@type`、`@data`、`@key:scoped`、`@ref:scoped` といった Rune JSON の特別属性はスキーマ内に一切定義されていません。
> 
> したがって、v7.4.0 の FpML Ingest サンプル（Rune JSON 形式）を、現行の v7.4.0 の `cdm-json-schema` でバリデーションしようとすると、`@` 属性が未定義プロパティとみなされたり、必須と定義されている `value` やラッパーが存在しないと判定されて**バリデーションエラー**となります。

この理由は、FINOS CDM の開発ロードマップにおいて、Java/Rune のランタイムシリアライザ（`RuneJsonObjectMapper`）が先行して v7.0.0 でデフォルト化された一方、外部配布用の JSON Schema ジェネレータ（Draft-04）は従来の Legacy JSON 構造を出力するパイプラインのまま維持されている（または過渡期にある）ためです。

---

## 6. Java ランタイムにおける後方互換性と相互変換

CDM v7.x の Java ライブラリ（`cdm-java`）では、新旧両方のフォーマットが完全にサポートされており、データ損失なしに双方向変換が可能です。

### 2つの Object Mapper
1. **`org.finos.rune.mapper.RuneJsonObjectMapper`**:
   - CDM v7.x のデフォルト。
   - 新しい Rune JSON 形式（`@` 属性、フラット化、プルーニング）をシリアライズ/デシリアライズ。
2. **`com.regnosys.rosetta.common.serialisation.RosettaObjectMapper`**:
   - CDM v6.x までのデフォルト（`getNewMinimalRosettaObjectMapper()` / `getNewRosettaObjectMapper()`）。
   - 従来の Legacy JSON 形式（`meta` / `value` ラッパー）を処理。

### 相互変換コード例 (`SerialisationTest.java` より抜粋)
```java
// 1. Rune JSON (v7) から Legacy JSON (v6) への変換
RuneJsonObjectMapper runeMapper = new RuneJsonObjectMapper();
TradeState tradeState = runeMapper.readValue(runeJsonString, TradeState.class);

ObjectMapper legacyMapper = RosettaObjectMapper.getNewMinimalRosettaObjectMapper();
String legacyJson = legacyMapper.writerWithDefaultPrettyPrinter().writeValueAsString(tradeState);

// 2. Legacy JSON (v6) から Rune JSON (v7) への変換
TradeState tradeStateFromLegacy = legacyMapper.readValue(legacyJson, TradeState.class);
String convertedRuneJson = runeMapper.writerWithDefaultPrettyPrinter().writeValueAsString(tradeStateFromLegacy);

// データ損失なし（完全一致）
assertEquals(runeJsonString, convertedRuneJson);
```

---

## 7. まとめ & 移行時のチェックリスト

CDM 6.x から 7.x へのバージョンアップ、または CDM JSON 連携を行うシステムにおける留意点は以下の通りです：

1. **JSON パーサーの対応**:
   - 自前で JSON をパース・生成している場合、`@type` や `@data` などの `@` プレフィックスキーのハンドリングを実装する必要がある。
   - Java 実装では `RuneJsonObjectMapper` を使用すれば自動的に透過処理される。
2. **ポリモーフィズムのアンラップ処理廃止**:
   - `payout.get("InterestRatePayout")` のような型名ラッパー前提のアクセスコードは、`payout.get("@type")` に基づく分岐へリファクタリングが必要。
3. **JSON Schema バリデーションの運用判断**:
   - 配布されている `cdm-json-schema`（Draft-04）を利用してバリデーションを行う場合は、データ電文を一度 `RosettaObjectMapper` 経由の Legacy JSON 形式で扱うか、Rune JSON に対応した最新のスキーマ生成器・Pydantic モデルを使用する必要がある。
