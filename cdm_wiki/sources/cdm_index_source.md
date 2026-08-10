---
title: "一次ソース要約: CDM_INDEX.md"
category: "sources"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-09"
tags: [source, cdm, index, rosetta]
---

# 一次ソース要約: CDM 総合ナビゲーションガイド (`CDM_INDEX.md`)

本ページは、FINOS Common Domain Model リポジトリのマスターナビゲーションガイドである [CDM_INDEX.md](../CDM_INDEX.md) の内容を要約したものです。

---

## 1. 主なリポジトリ構造

`common-domain-model` リポジトリの主要構成要素：
- **`rosetta-source/src/main/rosetta/`**: モデル定義を含む 145 ファイルの Rosetta (Rune) DSL。
- **`rosetta-source/src/main/java/`**: 手動作成された Java 拡張（Guice モジュール、Qualification ハンドラー等）。
- **`rosetta-source/src/main/resources/`**: 設定ファイル、コードリスト、Descriptor JSON 等。
- **`rosetta-source/src/generated/java/`**: Rosetta DSL から自動生成された不変 Java クラス群。

---

## 2. 命名規則とサフィックス分類

ファイルは `[ドメイン]-[サブドメイン]-[種類].rosetta` という命名規則に従っています：

| サフィックス | 役割・用途 | 代表例 |
|---|---|---|
| `-type.rosetta` | データ構造・型定義 (`type`, `choice`) | [product-asset-type.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-asset-type.rosetta) |
| `-func.rosetta` | ビジネスロジック・計算関数 (`func`) | [event-common-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/event-common-func.rosetta) |
| `-enum.rosetta` | 列挙型定義 (`enum`) | [base-datetime-enum.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/base-datetime-enum.rosetta) |
| `-desc.rosetta` | ドメインの説明・注釈 (`annotation`) | [product-desc.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-desc.rosetta) |

---

## 3. ドメインプレフィックス分類

- **`base-`**: 基礎データ型（日時、営業日、日数計算、数学関数、当事者、法人識別子）
- **`product-`**: 金融商品モデル（金利・クレジット・株式・FX・コモディティのデリバティブ、ペイアウト、決済、自動分類）
- **`event-`**: ライフサイクル・取引イベント（約定、清算、ノベーション、アロケーション、状態遷移、ポジション管理）
- **`legaldocumentation-`**: 法的契約文書（ISDA/ICMA/ISLAマスターアグリーメント、CSA）
- **`observable-`**: 市場観測データ（参照金利 (FRO)、SOFR/EURIBOR 複利計算）
- **`ingest-fpml-`**: FpML XML メッセージからのマッピング関数群
- **`margin-schedule-`**: マージン計算・Initial Margin / Variation Margin スケジュール規則
