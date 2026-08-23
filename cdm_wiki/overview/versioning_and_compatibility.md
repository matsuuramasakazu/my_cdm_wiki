---
title: "FINOS CDM バージョニング体系 & 互換性ガイドライン"
category: "overview"
sources:
  - "../CDM_INDEX.md"
  - "../sources/official_external_sources.md"
  - "https://cdm.finos.org/docs/versioning"
  - "https://cdm.finos.org/docs/change-control-guidelines"
  - "https://cdm.finos.org/docs/maintenance-and-release"
  - "https://cdm.finos.org/docs/major-release-scheduling-guidelines"
  - "https://semver.org/spec/v2.0.0.html"
last_updated: "2026-08-24"
tags: [cdm, finos, versioning, semver, compatibility, breaking-changes, releases, governance]
---

# FINOS CDM バージョニング体系 & 互換性ガイドライン

FINOS Common Domain Model (CDM) は、金融業界全体（デリバティブ、レポ、証券貸借、規制報告など）で共有される共通データ・業務ロジック標準として、厳格な **Semantic Versioning 2.0.0 (SemVer)** を採用してバージョン管理を行っています。

本ドキュメントでは、FINOS CDM 公式技術ドキュメント（[Versioning](https://cdm.finos.org/docs/versioning)、[Change Control Guidelines](https://cdm.finos.org/docs/change-control-guidelines)、[Maintenance and Release](https://cdm.finos.org/docs/maintenance-and-release)、[Major Release Scheduling Guidelines](https://cdm.finos.org/docs/major-release-scheduling-guidelines)）の原文規定を具体的に引用し、バージョン番号の構造、変更種別（破壊的変更 vs 許容される変更）、後方互換性（Backward Compatibility）の保証範囲、および PR・リリースの承認ガバナンスを体系的に解説します。

---

## 1. CDM バージョン番号の基本構造 & リリーストレイン

### 1.1 SemVer 2.0.0 の採用
CDM のリリースバージョンは `MAJOR.MINOR.PATCH`（例: `6.24.0`, `7.1.0`）という 3 つの数字で表されます。

```text
       MAJOR . MINOR . PATCH  [-DEV.x]
         │       │       │        │
         │       │       │        └── 開発プレリリース識別子（プロトタイプ・破壊的変更含む）
         │       │       └─────────── 後方互換性のあるバグ修正・誤記訂正（Bug fixes）
         │       └─────────────────── 後方互換性のある機能追加（Feature additions）
         └─────────────────────────── 後方互換性のない破壊的変更（Breaking changes）
```

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Versioning - Semantic Versioning](https://cdm.finos.org/docs/versioning#semantic-versioning)）
> *"The CDM is released using the semantic versioning 2.0 system - See SemVer 2.0.0. At high-level, the format of a version number is MAJOR.MINOR.PATCH (e.g. 1.23.456), where:*
> - *A **MAJOR** (`1`) version may introduce backward-incompatible changes and will be used as high level release name (e.g. "CDM Version 1"). See our major release scheduling guidelines for guidelines on how major releases are scheduled.*
> - *A **MINOR** (`23`) version may introduce new features but in a backward-compatible way, for example supporting a new type of event or function.*
> - *A **PATCH** (`456`) version is for backward-compatible bug fixes, for example fixing the logic of a condition.*
> - *In addition, pre-release versions of a major release will be denoted with a DEV tag as follows: `MAJOR.0.0-DEV.x` (e.g. `1.0.0-DEV.789`), where x gets incremented with each new pre-release version until it becomes the MAJOR.0.0 release."*

### 1.2 リリーストレインと提供形態（Version Availability）
CDM では、コミュニティによる迅速な機能開発と金融機関の本番安定運用の両立（dual objective）を図るため、以下の 2 種類のリリーストレインが並行管理されます。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Versioning - Version Availability](https://cdm.finos.org/docs/versioning#version-availability)）
> - ***The latest development version*** *(i.e. with a pre-release tag): fosters continued, rapid change development and involves model contributions made by the industry community. Changes that break backward compatibility are allowed. This development version is available in read-only and read-write access on the CDM's modelling-platforms.*
> - ***The latest production version*** *(i.e. without any pre-release tag): offers a stable, well-supported production environment for consumers of the model. Unless under exceptional circumstances, no new disruptive feature shall be introduced, mostly bug fixes only. Any change shall adhere to a strict governance process as it must be backward-compatible. Generally, it can only be developed by a CDM Maintainer.*
> - ***Earlier production versions***: *when still supported, are also available in read-only access for industry members who are still implementing older versions of the model. Over time, those earlier production versions enter long-term support in which supportability will be degraded, until they eventually become unsupported.*

| トレイン種別 | バージョン表記例 | 破壊的変更の可否 | 主な用途・利用対象 | アクセス権限 |
|---|---|---|---|---|
| **Development Version (DEV)** | `7.0.0-DEV.12` | ⭕ **許可**（互換性保証なし） | 次期メジャー向け新機能のプロトタイピング、コミュニティ開発 | Read / Write |
| **Production Version (安定本番版)** | `6.24.0` | ❌ **厳格禁止**（後方互換性維持） | 本番システム、金融インフラ、規制報告パイプラインでの安定運用 | Read-Only |
| **Earlier Production / LTS** | `5.20.0` | ❌ **厳格禁止**（保守のみ） | 旧バージョンを利用中の機関向け（段階的にサポート終了へ移行） | Read-Only |

---

## 2. バージョンごとのインクリメント基準 & 変更種別の公式定義

### 2.1 メジャーバージョン（MAJOR: `6`, `7` など）のインクリメント基準
**「後方互換性のない破壊的変更（Backward-Incompatible / Breaking Changes）」**が導入された場合にインクリメントされます。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Major Release Scheduling Guidelines](https://cdm.finos.org/docs/major-release-scheduling-guidelines#detailed-guidelines--changes-vs--major-versions)）
> *"Breaking changes (as defined in the change control guidelines) can only be implemented in a major version... When a major version includes breaking changes, the SWG will endeavour to ensure that appropriate migration guides and transition plans are in place."*
>
> *(同ドキュメント: Scheduling Guidelines)*
> *"The intention is that major releases shall be planned and reviewed at the SWG at least 3 months ahead of the anticipated release date... It is anticipated that for at least the next several years at least one major release will be planned each year."*

- **事前計画と承認**: メジャーリリースは Steering Working Group (SWG) により、リリース予定日の少なくとも 3 ヶ月前に事前計画・承認され、[ROADMAP.md](https://github.com/finos/common-domain-model/blob/master/ROADMAP.md) に公開されます。
- **移行支援**: 破壊的変更を含むメジャーリリースでは、旧構造から新構造へのマッピングや移行ガイド（Migration Guide）の提供が義務付けられます。

---

### 2.2 破壊的変更（Prohibited）と許容される変更（Allowed）の公式分類
FINOS CDM ドキュメントでは、同一メジャーバージョン内で何が「禁止される変更（Prohibited changes）」で、何が「許容される変更（Allowed changes）」であるかが厳密に定義されています。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Change Control Guidelines - Backward Compatibility](https://cdm.finos.org/docs/change-control-guidelines#backward-compatibility)）
> 
> **Prohibited changes（禁止される破壊的変更）:**
> - *Change to the structure (e.g. the attributes of a data type or the inputs of a function) or removal of any model element*
> - *Change to the name of any model element (e.g. types, attributes, enums, functions or reporting rules)*
> - *Change to any condition or cardinality constraint that makes validation more restrictive*
> - *Change to the DSL that results in any existing expression becoming invalid*
> - *Change to the DSL that results in change to any of the generated code's public interfaces*
> 
> **Allowed changes（許容される後方互換な変更）:**
> - *Change that relaxes any condition or cardinality constraint*
> - *Addition of new examples or test packs*
> - *Change to the user documentation or model descriptions*
> - *Addition of new data types, optional attributes, enumerations, rules or functions that do not impact current functionality*
> 
> **Exceptions（例外規定）:**
> - *Exceptions to backward compatibility may be granted for emergency bug fixes following decision from the relevant governance body.*

#### 具体的な変更種別の対比：

| カテゴリ | ❌ 禁止される破壊的変更（MAJOR アップグレードが必要） | ⭕ 許容される変更（MINOR / PATCH で導入可能） |
|---|---|---|
| **データ型・属性** | 既存型・属性の削除、リネーム、型の差し替え（`string` → `LegalEntity` 等） | 新規型の追加、既存型への**任意属性 `(0..1)` / `(0..*)`** の追加 |
| **カーディナリティ & 制約** | 任意属性の必須化（`0..1` → `1..1`）、バリデーション条件（`condition`）の厳格化 | カーディナリティや制約条件の緩和（`1..1` → `0..1` など） |
| **列挙型 (Enum)** | 既存 Enum や列挙値（Value）の削除・名称変更 | 既存 Enum への新規列挙値（Value）の追加、新規 Enum の追加 |
| **関数 (Function)** | 関数の削除・改名、必須入力引数（`inputs`）の追加、引数・戻り値型の変更 | 新規関数の追加、既存関数の内部計算バグ修正 |
| **Rosetta DSL / コード生成** | DSL 構文変更に伴う既存式の無効化、Java 生成クラスの公開 API/シグネチャの破壊 | コードジェネレータのバグ修正、DSL の後方互換な新構文追加 |

---

### 2.3 マイナーバージョン（MINOR: `6.24` の `24`、`7.1` の `1` など）のインクリメント基準
**「後方互換性を完全に維持した機能追加・拡張（Backward-Compatible Feature Additions）」**が行われた場合にインクリメントされます。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Change Control Guidelines - Change Control Rules](https://cdm.finos.org/docs/change-control-guidelines#change-control-rules)）
> *"Within multiple minor releases of a single major release, the following must be true:*
> - *Within business objects, any object that is valid in version M.N should be representable and valid in version M.N+1.*
> - *All validations that pass in version M.N should also pass in version M.N+1.*
> - *Function signatures may not be changed in such a way as to invalidate previous callers...*
> - *Test cases that passed in a prior version shall continue to work."*

- **リリース頻度の指針**:
  > **【公式ドキュメント引用】**（[FINOS CDM Docs: Maintenance and Release - Minor Production Release Scheduling](https://cdm.finos.org/docs/maintenance-and-release#minor-production-release-scheduling-and-approvals)）
  > *"Minor production releases to introduce enhancements should be combined to minimize the number of production releases, targeting minor production releases to be issued around four weeks or so as long as there is a queue of approved PRs."*
  > （※承認済み PR のキューに基づき、エンドユーザーの追従負荷を減らすため約4週間ごとに集約してリリースされる）

---

### 2.4 パッチバージョン（PATCH: `6.24.1` の `1` など）のインクリメント基準
**「後方互換性のあるバグ修正（Backward-Compatible Bug Fixes）」**や非機能的修正が行われた場合にインクリメントされます。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Maintenance and Release - Production Patch Release Scheduling](https://cdm.finos.org/docs/maintenance-and-release#production-patch-release-scheduling-and-approvals)）
> *"Production patch releases to correct defects without releasing new functionality may be scheduled by the maintainers based on the presence of approved defect correction PRs, or other non-functional PRs (e.g. security remediations)."*

- 条件式（`condition`）や計算ロジックの不具合修正（意図された設計仕様への適合化）。
- 定義記述（Descriptions）やドキュメントの誤記修正。
- セキュリティ脆弱性の修正やライブラリ依存関係のパッチ適用。

---

## 3. 同一メジャーバージョン内における互換性の保証範囲

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Change Control Guidelines - Backward Compatibility](https://cdm.finos.org/docs/change-control-guidelines#backward-compatibility)）
> *"Like other types of software, backward compatibility in the context of a domain model means that an implementor of that model would not have to make any change to update to such version."*

メジャーバージョンが同一である限り（例: CDM 6.0.0 から 6.24.0 まで）、CDM は以下の互換性を保証します。

### 3.1 データ互換性（インスタンスの後方互換性）
- **過去データの妥当性保証**:
  古いマイナーバージョン（例: CDM 6.0）で作成・シリアライズされた有効な JSON/XML メッセージ（`TradeState` や `BusinessEvent` など）は、同一メジャー内の最新マイナーバージョン（例: CDM 6.24）のスキーマやバリデーションにかけても、**100% 有効（Valid）**として検証を通過します。
- **理由**:
  既存のフィールドは削除・改名されず、必須化もされないため、既存のデータ構造が壊れることはありません。

### 3.2 ソースコード & API 互換性（コンパイル・バインディング互換性）
- **既存 API 呼び出しの非破壊**:
  Rosetta DSL から生成される Java クラスやインターフェースにおいて、既存の型名、ゲッター/セッター、ビルダーメソッドのシグネチャは維持されます。
- **ライブラリ差し替え**:
  CDM 6.0 を前提に書かれた業務アプリケーションコードは、ライブラリの依存関係を CDM 6.24 に更新しても、再コンパイルが通り、そのまま動作します。

---

## 4. プルリクエスト (PR) 分類と承認ガバナンス要件

FINOS CDM では、変更が誤って破壊的にならないよう、PR の種別および互換性の有無に応じて厳格なレビュー・承認マトリクスが定められています。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Change Control Guidelines - Summary of PR Approval Requirements](https://cdm.finos.org/docs/change-control-guidelines#summary-of-pr-approval-requirements)）

### 4.1 PR 承認要件マトリクス

| PR 種別 | 後方互換（Backward Compatible） | 破壊的変更（Backward Incompatible） |
|---|---|---|
| **Model - Bug Fix（モデル不具合修正）** | **Maintainer 1 名**（提出者とは別組織の Maintainer が望ましい） | **Maintainer 2 名** + **CRWG レビュー** + **SWG 承認**（※本番バージョンの場合。原則として最近追加された機能の修正のみに限定） |
| **Model - Enhancement（機能追加・拡張）** | **Maintainer 2 名** + **Working Group (WG) または CRWG の承認** | **Maintainer 2 名**（うち1名は別組織） + **SWG 承認 / ロードマップ記載** + **WG/CRWG 承認**（※必ず DEV バージョンへ投入） |
| **Technical（依存関係、マッピング、テスト、文書等）** | **Maintainer 1 名以上**（必要に応じて TAWG に相談） | **TAWG (Technology Architecture WG) 承認**（※必ず DEV バージョンへ投入） |

### 4.2 リリースビルドの承認要件マトリクス

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Maintenance and Release - Summary of Release Approval Requirements](https://cdm.finos.org/docs/maintenance-and-release#summary-of-release-approval-requirements)）

| リリース種別 | 承認要件 | スケジューリング & 備考 |
|---|---|---|
| **Major Release** (例: `7.0.0`) | **Maintainer 2 名 + SWG** | SWG による事前計画（3ヶ月前）。前回メジャーからの変更差分分析を含む。 |
| **Minor Release** (例: `6.24.0`) | **Maintainer 2 名** | Maintainer が管理。約4週間隔での集約リリースを目標とする。 |
| **Patch Release** (例: `6.24.1`) | **Maintainer 1 名** | Maintainer が不具合修正 PR の状況に応じて随時スケジューリング。 |
| **Development Release** (例: `7.0.0-DEV.12`) | **Maintainer 1 名** | Maintainer が随時発行（PR 承認・テスト通過後即座にリリース可能）。 |

---

## 5. 互換性の境界と実装上の注意点

同一メジャーバージョン内であっても、システム実装上で留意すべき「境界」が存在します。

> **【公式ドキュメント引用】**（[FINOS CDM Docs: Change Control Guidelines](https://cdm.finos.org/docs/change-control-guidelines#change-control-rules)）
> *"Please note that full, bidirectional interoperability between minor versions is not required. If an application uses functionality in version M.N, it does not need to fully interoperate with version M.N-1, assuming that the older version does not include that functionality. However, if an application uses functionality found in version M.N, it should be able to interoperate with version M.N+1."*

| 観点 | 保証状況 | 公式見解・実装上の注意点 |
|---|---|---|
| **後方互換性 (Backward)** | **完全保証** | 古いバージョン（M.N）で作られたデータ・コードは新しいバージョン（M.N+1）で問題なく動作する。 |
| **前方互換性 (Forward)** | **非保証** | 新しいマイナーバージョンで追加された要素を含むデータを古いバージョンのパーサーで読み込む場合、パーサー設定（例: Jackson の `FAIL_ON_UNKNOWN_PROPERTIES=false`）等で未知のフィールドを無視する設計が必要。 |
| **Enum の網羅性チェック** | **実装依存** | 既存の `enum` に新しい値が追加された場合、Java コードで `switch-case` の網羅分岐を記述していると、未知の Enum 値を受信した際に `default` 句のハンドリングや例外処理が必要になる。 |
| **Pre-release (DEV版)** | **保証外** | `-DEV` タグが付いたプレリリースビルド同士の間では破壊的変更が許可されているため、本番運用には必ず正式リリース版（Production Version）を使用する。 |
| **ダウンストリーム検証** | **必須** | モデル変更時は、下流プロジェクト（Translate、CDM Homepage、CDM Java Examples）のビルド・回帰テストが全て成功することを確認する。 |

---

## 6. 一次情報・引用元リファレンス一覧

本ガイドラインに記載された内容は、以下の公式ドキュメントおよびガバナンス規約に基づいています（すべて HTTP 200 OK 事前検証済み）：

| ドキュメント名 | 公式 URL | 主な参照・引用範囲 |
|---|---|---|
| **FINOS CDM - Versioning** | [https://cdm.finos.org/docs/versioning](https://cdm.finos.org/docs/versioning) | SemVer 2.0.0 の採用、バージョン番号構造、Production / Development バージョンの提供形態 |
| **FINOS CDM - Change Control Guidelines** | [https://cdm.finos.org/docs/change-control-guidelines](https://cdm.finos.org/docs/change-control-guidelines) | 後方互換性の定義、Prohibited / Allowed 変更の個別規定、PR 承認マトリクス |
| **FINOS CDM - Maintenance and Release** | [https://cdm.finos.org/docs/maintenance-and-release](https://cdm.finos.org/docs/maintenance-and-release) | リリースビルド承認マトリクス、レビューチェックリスト、ダウンストリーム依存関係 |
| **FINOS CDM - Major Release Scheduling Guidelines** | [https://cdm.finos.org/docs/major-release-scheduling-guidelines](https://cdm.finos.org/docs/major-release-scheduling-guidelines) | メジャーリリースの目的・原則、SWG による3ヶ月前計画、移行ガイド作成義務 |
| **Semantic Versioning 2.0.0 Specification** | [https://semver.org/spec/v2.0.0.html](https://semver.org/spec/v2.0.0.html) | SemVer 2.0.0 公式仕様（MAJOR.MINOR.PATCH の一般的定義） |
| **FINOS CDM - GitHub Roadmap** | [https://github.com/finos/common-domain-model/blob/master/ROADMAP.md](https://github.com/finos/common-domain-model/blob/master/ROADMAP.md) | FINOS CDM 公式リリース計画およびロードマップ |

---

## 関連リファレンス
- [CDM 全体アーキテクチャ](cdm_architecture.md)
- [Rosetta DSL 定義カタログ](rosetta_dsl_inventory.md)
- [公式外部一次情報・リファレンスリンク集](../sources/official_external_sources.md)
- [FINOS CDM 公式ドキュメント](https://cdm.finos.org/)

