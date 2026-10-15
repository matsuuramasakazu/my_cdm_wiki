---
title: "FpML メッセージ取り込み & マッピングアーキテクチャ"
category: "concepts"
sources:
  - "../CDM_INDEX.md"
last_updated: "2026-10-14"
tags: [fpml, xml, ingestion, mapping, confirmation, swap, tradestate, partyreference, idref, execution_notification, test_pack, incomplete]
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
  - CDM 側では `ReferenceWithMetaParty`（`externalReference` / `globalReference`）型として取り込まれ、CDM の参照解決エンジンにより該当 `Party` オブジェクトへの紐付けが行われます。

---

## 6. 執行通知 (ExecutionNotification) および自然人識別子マッピング

FpML Ingestion では、執行通知メッセージおよび詳細な当事者識別子の取り込みロジックが提供されています：

1. **`executionNotification` から `ExecutionInstruction` へのマッピング**:
   - `ingest-fpml-confirmation-message-func.rosetta` および `ingest-fpml-confirmation-workflowstep-func.rosetta` において、FpML の `executionNotification` メッセージから CDM の `ExecutionInstruction` を直接生成するマッピングロジック（`MapTradeToExecutionInstruction` 等）が定義されています。
2. **自然人・当事者識別子スキームのサポート**:
   - `ingest-fpml-confirmation-party-func.rosetta` および `ingest-fpml-confirmation-other-func.rosetta` において、`personId` / `identifierType` と FpML 標準スキーム（LEI, NaturalPerson 等）を相互変換する `MapPersonIdentifierTypeEnum` 等の関数が備わっており、規制報告（MiFIR/EMIR REFIT）における自然人識別子の取り込みに対応しています。

---

## 7. Ingestion テストパック構成と incomplete フォルダの位置づけ

CDM リポジトリの [common-domain-model/rosetta-source/src/main/resources/ingest](../../common-domain-model/rosetta-source/src/main/resources/ingest) 配下には、FpML XML から CDM オブジェクトへの変換（Translation）を検証するためのテストリソース（Test Pack）が格納されています。

### 7.1 ディレクトリ構成

- `config/`: 各テストパックの構成定義 JSON（`test-pack-translate-*.json`）。入力 XML パス、期待値 JSON 出力パス、およびアサーション条件（ノード数や検証エラー許容数等）を定義。
- `input/`: 入力となる FpML XML サンプルファイル（FpML 5.10, 5.12, 5.13 各バージョンの公式配布サンプル等）。
- `output/`: Ingestion 変換パイプライン（`Ingest_FpmlConfirmationToTradeState` や `Ingest_FpmlConfirmationToWorkflowStep`）の出力期待値となる CDM JSON（`TradeState` / `WorkflowStep`）。

### 7.2 `incomplete` の有無による違い

`input/` および `output/` のサブフォルダ名には、`incomplete` が含まれるフォルダと含まれないフォルダが存在します：

| 分類 | フォルダ名の例 | 定義と役割 |
|---|---|---|
| **通常フォルダ**（完了） | `fpml-5-10-products-rates`<br>`fpml-5-13-products-credit-derivatives`<br>`fpml-5-10-processes` | **完全なマッピングカバレッジ（Complete Mapping Coverage）**<br>CDM の Rosetta Synonym および Ingestion 関数によって安定して変換可能と認定された公式サポートサンプル。プロダクト仕様やライフサイクルイベントが CDM 構造へ十全にマッピングされる。 |
| **`incomplete` フォルダ**（未完了・開発途上） | `fpml-5-10-incomplete-products-bond-options`<br>`fpml-5-13-incomplete-products-equity-options`<br>`fpml-5-10-incomplete-processes` | **不完全なマッピングカバレッジ（Incomplete Mapping Coverage）**<br>FpML 公式サンプルのうち、CDM 側のモデル化が未対応、または Ingestion マッピングが未実装・一部不完全なサンプル。エキゾチック条項、複雑なバスケット、特殊な修正通知などが隔離・分類されている。 |

### 7.3 ライフサイクルと運用

1. **隔離とバックログ化**:
   - FpML の新バージョン（例: FpML 5.13）取り込み時、まだ CDM 側でマッピングが未整備なサンプルは `incomplete` フォルダに配置され、開発対象バックログ（WIP）として管理されます。
2. **マッピング開発による通常フォルダへの昇格**:
   - コミュニティやワーキンググループによってマッピングが実装され、カバレッジが満たされると、サンプルは `incomplete` フォルダから通常フォルダへ昇格・移動されます（例: PR #2397 による Equity サンプルの再配置、PR #1626 による Novation サンプルの昇格、PR #4340 による CDS Option マッピング追加など）。
3. **回帰防止テストでのベースライン管理**:
   - `incomplete` のテストパックも CI/CD（`IngestFpmlConfirmationToTradeStateTest` 等）で実行されます。`config/` 内の設定ファイルで現時点のバリデーション失敗数（`modelValidationFailures`）がアサーションとして記録されており、開発途中の状態をスナップショットとして固定・監視することで不慮のリグレッションを検知します。

### 7.4 実例分析: FpML 5.13 為替デリバティブ (`incomplete-products-fx-derivatives`) 全16サンプルの不完全要因一覧

[fpml-5-13-incomplete-products-fx-derivatives](../../common-domain-model/rosetta-source/src/main/resources/ingest/output/fpml-confirmation-to-trade-state/fpml-5-13-incomplete-products-fx-derivatives) に格納されている全16サンプルの具体的な未完了・欠落要因の一覧です：

| # | サンプル名 | FpML 要素 | XML 主仕様 | CDM 変換状態 | 具体的な不完全要因・欠落内容 | 検証エラー |
|---|---|---|---|---|---|:---:|
| 1 | `dcd-ex01-dual-currency-deposit` | `<termDeposit>` | 二重通貨定期預金（元本、固定金利、為替リンク条項、利息） | `product` なし<br>(ヘッダーのみ) | **マッピング完全未対応 (0%)**。<br>`termDeposit` をパースする Ingestion 関数が存在せず、プロダクト・条件が全損。 | 3 |
| 2 | `fx-ex04-fx-fwd-w-settlement` | `<fxSingleLeg>` | 為替フォワード ＋ SWIFT 決済指示・コルレス情報 | `SettlementPayout` あり<br>`tradeLot` あり | **決済指示の欠落**。<br>`<settlementInformation>`（SWIFTコード、コルレス銀行、受取人口座・ルーティング）が CDM 側に一切マッピングされず消失。 | 2 |
| 3 | `fx-ex06-fx-fwd-w-splits` | `<fxSingleLeg>` | 為替フォワード ＋ 分割決済指示（Split Settlement） | `SettlementPayout` あり<br>`tradeLot` あり | **分割決済指図の欠落**。<br>`<splitSettlement>`（同一レグに対する複数口座・金額への送金分割指図）がマッピングされず消失。 | 2 |
| 4 | `fx-ex12-fx-barrier-option` | `<fxOption>` | 為替オプション ＋ シングルバリア（Knock-in Up, 0.8975） | `OptionPayout` あり<br>(バニラに縮退) | **バリア条項の未マッピング**。<br>`<features><barrier>`（トリガーレート、ノックイン条件、監視情報源）が完全消失し、タクソノミもバニラオプションと誤認。 | 6 |
| 5 | `fx-ex13-fx-dbl-barrier-option` | `<fxOption>` | 為替オプション ＋ ダブルバリア（上下限トリガーレート） | `OptionPayout` あり<br>(バニラに縮退) | **ダブルバリア条項の未マッピング**。<br>上限・下限のトリガーレート（0.8950 / 0.8800）および監視条件がマッピングされず消失。 | 6 |
| 6 | `fx-ex14-euro-digital-option` | `<fxDigitalOption>` | 欧州型バイナリー（デジタル）オプション（トリガー判定＋固定ペイアウト） | `OptionPayout` 骨格のみ<br>(ロット・金額欠落) | **トリガー＆固定ペイアウト金額の欠落**。<br>`<trigger>` レートおよび `<payout>`（支払額）、原資産、`tradeLot` が消失し、満期日のみの空骨格に縮退。 | 5 |
| 7 | `fx-ex15-euro-range-digital-option` | `<fxDigitalOption>` | 欧州型レンジデジタルオプション（2つのトリガーレート範囲判定） | `OptionPayout` 骨格のみ | **レンジトリガー＆固定ペイアウトの欠落**。<br>上下2つの `<trigger>` レートおよび `<payout>` 金額が完全消失。 | 5 |
| 8 | `fx-ex16-one-touch-option` | `<fxDigitalOption>` | アメリカン型ワンタッチオプション（期間中1回でも到達で支払） | `OptionPayout` 骨格のみ | **タッチ条件＆固定ペイアウトの欠落**。<br>`<touch>` 条件、判定レート、支払金額が一切マッピングされず消失。 | 5 |
| 9 | `fx-ex17-no-touch-option` | `<fxDigitalOption>` | アメリカン型ノータッチオプション（期間中一度も触れなければ支払） | `OptionPayout` 骨格のみ | **ノータッチ条件＆固定ペイアウトの欠落**。<br>`<touch>` 監視条件および固定ペイアウト金額が完全消失。 | 5 |
| 10 | `fx-ex18-double-one-touch-option` | `<fxDigitalOption>` | ダブルワンタッチオプション（上下いずれかに触れたら支払） | `OptionPayout` 骨格のみ | **ダブルタッチ条件＆固定ペイアウトの欠落**。<br>上下2つの `<touch>` 条件および支払金額が完全消失。 | 5 |
| 11 | `fx-ex19-double-no-touch-option` | `<fxDigitalOption>` | ダブルノータッチオプション（上下どちらにも触れなければ支払） | `OptionPayout` 骨格のみ | **ダブルノータッチ条件＆固定ペイアウトの欠落**。<br>上下2つの `<touch>` 条件および支払金額が完全消失。 | 5 |
| 12 | `fx-ex23-straddle` | `<strategy>` | ストラドル戦略（同一ストライクの Call ＋ Put 合成） | `product` なし<br>(ヘッダーのみ) | **マルチレグ戦略の完全未対応 (0%)**。<br>`strategy` コンテナ内の 2 つの `fxOption` が丸ごと脱落。 | 3 |
| 13 | `fx-ex24-delta-hedge` | `<strategy>` | デルタヘッジ戦略（オプション ＋ 直物/先物の複合） | `product` なし<br>(ヘッダーのみ) | **複合戦略の完全未対応 (0%)**。<br>`fxOption` と `fxSingleLeg` の両脚が丸ごと脱落。 | 3 |
| 14 | `fx-ex25-option-strategyComponentIdentifier` | `<strategy>` | 戦略コンポーネント識別子付きオプション戦略 | `product` なし<br>(ヘッダーのみ) | **戦略・脚識別子の完全未対応 (0%)**。<br>`strategyComponentIdentifier` および内包されるオプションが脱落。 | 3 |
| 15 | `fx-ex27-flexible-term-forward` | `<fxFlexibleForward>` | 任意期日為替先渡（受渡可能期間、最低行使額、先渡レート） | `product` なし<br>(ヘッダーのみ) | **フレキシブル先渡の完全未対応 (0%)**。<br>`fxFlexibleForward` のパースロジックがなく、受渡期間やレートが全損。 | 3 |
| 16 | `fx-ex32-forward-volatility-agreement` | `<fxForwardVolatilityAgreement>` | フォワード・ボラティリティ合意（将来のボラティリティ取引） | `calculationAgent` のみ<br>`payout: []` | **ボラティリティ取引条項の欠落**。<br>ボラティリティストライク（`forwardVolatilityStrikePrice`）、通貨ペア、プレミアムが脱落。 | 3 |

### 7.5 バージョン間比較検証: FpML 5.12 (`products-fx`) vs 5.13 (`incomplete-products`) のバリアオプション (`fx-ex12`)

同一のバリアオプションサンプル `fx-ex12-fx-barrier-option` について、通常フォルダに属する FpML 5.12 版（[fpml-5-12-products-fx](../../common-domain-model/rosetta-source/src/main/resources/ingest/output/fpml-confirmation-to-trade-state/fpml-5-12-products-fx/fx-ex12-fx-barrier-option.json)）と、`incomplete` フォルダに属する FpML 5.13 版（[fpml-5-13-incomplete-products-fx-derivatives](../../common-domain-model/rosetta-source/src/main/resources/ingest/output/fpml-confirmation-to-trade-state/fpml-5-13-incomplete-products-fx-derivatives/fx-ex12-fx-barrier-option.json)）を対比検証した結果は以下の通りです：

1. **TradeState JSON 本文の完全一致（差分ゼロ）**:
   - 2 つの JSON ファイルは、**SHA-256 ハッシュ値（`cadddb857410...`）およびファイルサイズ（5,530 バイト）がバイト単位で 100% 一致**しています。
   - すなわち、**「incomplete」に分類されているかどうかの違いは、生成される TradeState JSON の内部構造・値・メタプロパティには一切反映されていません**（CDM の JSON 内に `incomplete` フラグや隔離ステータス等は埋め込まれない）。
2. **フォルダ分類の相違の真因（CDM 開発チームによるマッピング未完了サンプルの隔離・整理）**:
   - `incomplete-products` という分類は FpML 標準側の仕様ではなく、**FINOS CDM 開発チーム（Hugo Hills 氏ら）が CDM のテストスイートにおいて「CDM 側でのモデル化・マッピングが未完成なサンプル」を通常サポート対象から隔離・管理するために設けた CDM 独自のテスト分類体系**です。
   - **FpML 5.12 導入時（PR #1034 / PR #1201）**: 2020年〜2021年の導入当初は `fx-ex01` 〜 `ex12` 等のサンプルが一括して `products/fx/`（通常フォルダ）に投入されており、バリアオプション（`fx-ex12`）もバリア条項未実装（バニラ縮退）のまま通常フォルダに配置されていました。
   - **FpML 5.13 導入時（PR #2797 / STORY-3208）**: 2024年3月に CDM 開発チームが FpML 5.13 テストパックを取り込んだ際、コミット `26ae072bc` の履歴（`* Separate incomplete products`）が示す通り、CDM 側で完全なマッピングが実現できていない製品群（バリアオプション `fx-ex12`、デジタルオプション `fx-ex14`〜`ex19`、マルチレグ戦略 `fx-ex23` 等）を通常フォルダから `incomplete-products` フォルダへ明示的に分離（Separate）しました。
3. **実態としての不完全性（両バージョン共通のマッピング脱落）**:
   - 2 つの JSON が同一である理由は、**どちらも FpML のバリア条項がマッピングされず、同じように不完全な状態で縮退出力されているため**です：
     - **バリア条項（`<features><barrier>`）の完全欠落**: FpML XML に定義された `Knockin`, `Up`, トリガーレート `0.8975`、監視期間が、CDM Ingestion 関数（[ingest-fpml-confirmation-product-fxoption-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-fxoption-func.rosetta) の `MapFxOptionFeaturesToObservationTerms`）において未実装（`asian` のみ対応）のため消失。
     - **商品自動判定の誤分類**: `OptionPayout -> feature` が空（absent）となるため、[product-qualification-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/product-qualification-func.rosetta) の `Qualify_ForeignExchange_VanillaOption` に合致し、バリアオプションであるにもかかわらず **`ForeignExchange_VanillaOption`（プレーンバニラ）** として出力。
     - **バリデーション失敗**: 5-12、5-13 ともにテストパックのアサーションで `modelValidationFailures: 6` が記録。

---

## 8. 関連ドキュメント
- [fx_products_and_synthetic_forward.md](fx_products_and_synthetic_forward.md): 為替プロダクトの CDM モデリング仕様および実サンプル検証
- [workflow_step_and_lifecycle_samples.md](workflow_step_and_lifecycle_samples.md): FpML executionAdvice からの WorkflowStep 変換サンプル解説
- [contract_dates_modeling.md](contract_dates_modeling.md): FpML Ingestion におけるレグ・商品日付の振り分け
- [vanilla_irs_trade_structure.md](vanilla_irs_trade_structure.md): TradeState 構造解説
- [ingest-fpml-confirmation-party-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-party-func.rosetta): 当事者マッピング関数定義
- [ingest-fpml-confirmation-product-fxoption-func.rosetta](../../common-domain-model/rosetta-source/src/main/rosetta/ingest-fpml-confirmation-product-fxoption-func.rosetta): 為替オプションの FpML マッピング関数定義
