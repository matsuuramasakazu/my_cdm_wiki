---
title: "FpML メッセージ取り込み & マッピングアーキテクチャ"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-14"
tags: [fpml, xml, ingestion, mapping, confirmation, swap, tradestate, partyreference, idref]
---

# FpML メッセージ取り込み & マッピングアーキテクチャ

CDM は、FpML (Financial products Markup Language) XML メッセージをパースし、型安全な CDM オブジェクトへ変換するマッピングレイヤー（Ingestion）および双方向の構造マッピングを備えています。

---

## 1. FpML ↔ CDM 変換機能の仕様と範囲

- **FpML XML → CDM (Ingestion)**: CDM リポジトリ標準の Rosetta DSL (`ingest-fpml-*.rosetta` 全33ファイル) により直接パースおよびモデル変換関数が標準提供されています。
- **CDM → FpML XML (Export / Projection)**: **CDM の標準モデル（Rosetta DSL）には、CDM から FpML XML への自動逆変換（エクスポート）機能は提供されていません。** Rosetta DSL のマッピング仕様は単方向の Ingestion 用であり、CDM から FpML XML を作成する場合は利用者が独自に Java API (`TradeState`) を操作するカスタムマッパー・シリアライザーを構築する必要があります。

---

## 2. 共通マッピング

- **ヘッダー & 当事者データ**: [ingest-fpml-confirmation-common-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-common-func.rosetta) および [ingest-fpml-confirmation-party-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-party-func.rosetta) の `Ingest_FpML_Confirmation` により処理。

---

## 3. 商品別 FpML マッピング（全33ファイル）

特定商品ノードを CDM Payout 構造に変換：
- **スワップ (IRS)**: [ingest-fpml-confirmation-product-swap-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-swap-func.rosetta)
- **クレジットデフォルトスワップ (CDS)**: [ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-creditdefaultswap-func.rosetta)
- **FX オプション**: [ingest-fpml-confirmation-product-fxoption-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-fxoption-func.rosetta)

---

## 4. プレーン金利スワップ (IRS) `TradeState` ↔ FpML マッピング表

プレーンな金利スワップの `TradeState` と FpML の主要要素の対応一覧：

| CDM (`TradeState`) | FpML XML ノード | 概要 |
|---|---|---|
| `TradeState` -> `trade` -> `tradeHeader` | `<tradeHeader>` | 取引識別子・約定日 |
| `TradeState` -> `trade` -> `party` | `<party>` | 取引当事者・LEI |
| `payout` -> `interestRatePayout` (固定) | `<swapStream>` (Fixed Stream) | 固定金利、支払頻度 |
| `payout` -> `interestRatePayout` (浮動) | `<swapStream>` (Floating Stream) | 参照金利 (SOFR, EURIBOR 等)、リセット日 |
| `calculationPeriodDates` | `<calculationPeriodDates>` | 計算期間・日数計算フラクション |

---

## 5. FpML PartyReference 属性仕様と CDM 参照解決

FpML における当事者参照（`PartyReference`）は、XML 文書内での正規化と重複排除のためにスキーマレベルで以下のように定義されています：

- **`href` 属性と `xsd:IDREF`**:
  - 各 `<party id="party1">` 要素には XML スキーマの `xsd:ID` 型属性が付与され、`<partyReference href="party1"/>` などの参照要素は `xsd:IDREF` 型として定義されます。これにより XML パーサーレベルで参照整合性が保証されます。
- **`ecore:reference` メタデータ**:
  - FpML XML Schema に付与される EMF (Eclipse Modeling Framework) 用アノテーションであり、XML スキーマから Java オブジェクトモデル（EMF ECore）を生成する際に、単なる文字列 ID ではなく該当の `Party` クラスインスタンスへの直接オブジェクト参照としてバインドされるよう指示します。
- **CDM での参照解決 (`ReferenceWithMetaParty`)**:
  - CDM (Rosetta DSL) では、`PartyReference` は `ReferenceWithMetaParty` / `Party` オブジェクトとして扱われ、FpML Ingestion 時に `href` ID を元に `trade -> party` リスト内の該当 `Party` インスタンスと自動解決・バインドされます（[ingest-fpml-confirmation-party-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-party-func.rosetta) 参照）。

