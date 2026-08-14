---
title: "FINOS CDM 外部一次情報・公式リファレンスリンク集"
category: "sources"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-08-14"
tags: [cdm, finos, isda, icma, isla, fpml, rosetta, rune, standards, references]
---

# FINOS CDM 外部一次情報・公式リファレンスリンク集

本ドキュメントは、FINOS Common Domain Model (CDM) の仕様策定・保守・拡張に関わる公式組織、国際標準化団体、業界コンソーシアム、および関連する金融市場標準の**一次情報（Primary Sources）**へのリンク集です。

※掲載されているすべての URL は、AI Agent ハーネスにより HTTP 接続性（200 OK）が事前検証されています。

---

## 1. FINOS CDM 公式リソース（コード・ドキュメント・コミュニティ）

| リソース名 | URL | 内容・用途 |
|---|---|---|
| **FINOS CDM ドキュメントポータル** | [https://cdm.finos.org/](https://cdm.finos.org/) | CDM 公式技術ドキュメント。6つのモデリング次元、プロダクトモデル、イベントライフサイクル仕様。 |
| **FINOS CDM GitHub リポジトリ** | [https://github.com/finos/common-domain-model](https://github.com/finos/common-domain-model) | CDM 公式オープンソースコードベース（Rosetta DSL ソース、Java 生成クラス、テストスイート）。 |
| **FINOS CDM プロジェクト概要** | [https://www.finos.org/common-domain-model](https://www.finos.org/common-domain-model) | FINOS コミュニティ、ガバナンス、ワーキンググループ活動情報。 |
| **FINOS コミュニティ** | [https://www.finos.org/community](https://www.finos.org/community) | FINOS 各プロジェクトのコミュニティ参加およびワーキンググループ情報。 |
| **Rune DSL (旧 Rosetta DSL) ドキュメント** | [https://docs.rosetta-technology.io/](https://docs.rosetta-technology.io/) | REGnosys / FINOS 提供の DSL 言語仕様、構文リファレンス、およびモデリングガイド。 |
| **Rune DSL GitHub リポジトリ** | [https://github.com/finos/rune-dsl](https://github.com/finos/rune-dsl) | Rune (Rosetta) DSL のパーサー・ジェネレーター・IDE プラグインのオープンソースリポジトリ。 |
| **REGnosys Rosetta DSL リポジトリ** | [https://github.com/REGnosys/rosetta-dsl](https://github.com/REGnosys/rosetta-dsl) | Rosetta DSL コア実装およびコンパイラリポジトリ。 |

---

## 2. 業界標準化 3 大団体（ISDA / ICMA / ISLA）公式リソース

CDM は、デリバティブ・レポ・証券貸借の 3 大金融業界団体が FINOS と共同で統一標準として推進しています。

### 2.1 ISDA (International Swaps and Derivatives Association) - デリバティブ市場
- **[ISDA 公式サイト](https://www.isda.org/)**: 国際スワップ・デリバティブ協会の公式ポータル。
- **[ISDA CDM ニュース・アナウンスメント](https://www.isda.org/tag/common-domain-model/)**: ISDA における CDM のリリース情報、ホワイトペーパー、Digital Regulatory Reporting (DRR) イニシアティブ。
- **[FpML (Financial products Markup Language) 公式サイト](https://www.fpml.org/)**: デリバティブ電子取引 XML 標準の公式ハブ。
- **[FpML 仕様ライブラリ (Specifications)](https://www.fpml.org/spec/)**: FpML 5.12 / 5.11 Confirmation 等の XML スキーマ定義・仕様書。
- **[ISDA Create](https://isdacreate.org/)**: ISDA マスター契約、CSA (担保契約) のデジタル交渉・合意プラットフォーム。

### 2.2 ICMA (International Capital Market Association) - レポ & 債券市場
- **[ICMA 公式サイト](https://www.icmagroup.org/)**: 国際資本市場協会の公式ポータル。
- **[ICMA レポ・担保市場ポータル](https://www.icmagroup.org/market-practice-and-regulatory-policy/repo-and-collateral-markets/)**: レポ取引（Repo）、現物債券取引、GMRA (Global Master Repurchase Agreement) への CDM 適用イニシアティブ。

### 2.3 ISLA (International Securities Lending Association) - 証券貸借市場
- **[ISLA 公式ポータル](https://www.islaemea.org/)**: 国際証券貸借協会の公式ポータル（GMSLA デジタル条項化および CDM 適用イニシアティブ）。

---

## 3. 関連国際規格・市場インフラ・規制報告標準

| 規格 / 機関 | URL | 関連領域・CDM との連携 |
|---|---|---|
| **GLEIF (LEI 規格)** | [https://www.gleif.org/](https://www.gleif.org/) | Global Legal Entity Identifier Foundation。CDM `LegalEntity` 型の取引主体識別子（LEI）標準。 |
| **CPMI-IOSCO / BIS** | [https://www.bis.org/cpmi/publ/d175.pdf](https://www.bis.org/cpmi/publ/d175.pdf) | CPMI-IOSCO による CDE (Critical Data Elements)、UTI (Unique Trade Identifier)、UPI の国際報告標準。 |
| **ANNA DSB (UPI)** | [https://www.anna-dsb.com/](https://www.anna-dsb.com/) | OTC デリバティブの Unique Product Identifier (UPI) 発行・検索サービス。CDM Qualification と連動。 |
