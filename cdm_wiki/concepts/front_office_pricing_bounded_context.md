---
title: "フロントオフィス・プライシング業務の Bounded Context 分割とマイクロサービス設計"
category: "concepts"
sources:
  - "CDM_INDEX.md"
  - "event-workflow-type.rosetta"
  - "observable-asset-type.rosetta"
  - "event-common-type.rosetta"
  - "product-template-type.rosetta"
last_updated: "2026-08-12"
tags: [cdm, pricing, bounded_context, microservices, front_office, ddd]
---

# フロントオフィス・プライシング業務の Bounded Context 分割とマイクロサービス設計

本ドキュメントでは、FINOS Common Domain Model (CDM) を標準データ表現およびドメインモデル（Ubiquitous Language / Canonical Data Model）のリファレンスとして用い、デリバティブ取引を中心とするフロントオフィス（Front Office: FO）のプライシング業務を「境界付けられたコンテキスト（Bounded Context）」に分割し、マイクロサービスアーキテクチャへと展開する標準設計を定義します。

---

## 1. CDMのリファレンスデータ型・イベントモデル対応表

CDMは、デリバティブ商品の経済条件、ライフサイクルイベント、観測市場データ、ワークフロー状態を統一的に表現する規格を提供しています。FOプライシング業務における各領域とCDM型・モデルの対応関係は以下の通りです。

| 業務フェーズ・概念 | CDM Rosetta DSL 型 / モデル | パッケージ / 定義ファイル |
|---|---|---|
| **商品定義・経済条件** | `TradableProduct`, `Product`, `Payout` (`InterestRatePayout`, `OptionPayout` 等) | `cdm.product.template.*`<br>`cdm.product.asset.*` |
| **価格・数量・スプレッド** | `PriceQuantity`, `Price`, `Quantity`, `Observable` | `cdm.observable.asset.*` |
| **参照金利・市場観測値** | `FloatingRateOptionEnum`, `Index`, `FloatingRateIndex` | `cdm.observable.asset.*` |
| **見積り・提示（Quoting）** | `PriceQuantity` (非確定値), `TradableProduct` (Draft) | `cdm.observable.asset.*` |
| **交渉・承認ワークフロー** | `WorkflowStep`, `WorkflowStepApproval`, `CreditLimitInformation` | `cdm.event.workflow.*` |
| **約定・実行指示** | `EventInstruction`, `Create_Execution` (Function) | `cdm.event.common.*` |
| **取引確定・状態保管** | `TradeState`, `Trade`, `BusinessEvent` | `cdm.event.common.*` |
| **ポジション・残高更新** | `Position`, `PortfolioState` | `cdm.event.position.*` |

---

## 2. 5つの Bounded Context（境界付けられたコンテキスト）の定義

ドメイン駆動設計（DDD）の観点に基づき、フロントオフィス・プライシング業務を相互に独立した5つの Bounded Context に分割します。

```
+-----------------------------------------------------------------------------------+
|                        Front Office Pricing Domain                                |
|                                                                                   |
|  +---------------------------+             +-----------------------------------+  |
|  | Market Data Context       |             | Indication & Quoting Context      |  |
|  | (Observables, Rates)      |             | (RFQ, Termsheet, Indicative Quote)|  |
|  +-------------+-------------+             +-----------------+-----------------+  |
|                |                                             |                    |
|                v                                             v                    |
|  +---------------------------+             +-----------------------------------+  |
|  | Pricing & Risk Context    | ------------| Negotiation & Confirmation Context|  |
|  | (PV, Greeks, CashFlow Engine|             | (WorkflowStep, Approval, Limits)  |  |
|  +---------------------------+             +-----------------+-----------------+  |
|                                                              |                    |
|                                                              v                    |
|                                            +-----------------------------------+  |
|                                            | Trade Capture & Booking Context   |  |
|                                            | (TradeState, BusinessEvent, Book) |  |
|                                            +-----------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### 2.1 Market Data & Observables Context (市場データ・観測データコンテキスト)
- **主要目的**: 外部市場ベンダー（Bloomberg, Refinitiv 等）からの金利・FX・ボラティリティデータの収集、正規化、およびリアルタイム配信。
- **Ubiquitous Language**: MarketQuote, FloatingRateOption, YieldCurve, VolatilitySurface.
- **中心となるCDM構造**: `cdm.observable.asset.FloatingRateOptionEnum`, `InformationSource`, `Observable`.
- **主要イベント/API**: `MarketDataUpdatedEvent`, `GetLatestCurveQuery`.

### 2.2 Indication & Quoting Context (概算試算・条件提示コンテキスト)
- **主要目的**: 顧客（Buy-side/法人）や営業（Sales）からの見積り要求（RFQ: Request for Quote）に対する高速非拘束試算（Indicative Price）およびタームシート生成。
- **Ubiquitous Language**: QuoteRequest, IndicativeQuote, TermsheetDraft, SpreadSensitivity.
- **中心となるCDM構造**: `cdm.product.template.TradableProduct` (草案状態), `cdm.observable.asset.PriceQuantity` (非拘束フラグ付き).
- **主要イベント/API**: `RequestForQuoteCommand`, `QuoteIndicatedEvent`.

### 2.3 Pricing & Risk Valuation Context (プライシング・リスク計算コンテキスト)
- **主要目的**: 金融工学評価モデル（Monte Carlo, PDE, Analytical）による厳密な時価（PV: Present Value）、リスク感応度（Delta, Gamma, Vega）、XVA（CVA/FVA）の算出、および**約定条件（Par Coupon, Par Strike 等）を解く Solver（逆算・数値探索）アルゴリズムの実行**。
- **Ubiquitous Language**: PresentValue, SensitivityGreeks, ValuationModel, CashFlowSchedule, SolverTarget, RootFinder.
- **中心となるCDM構造**: `cdm.product.asset.InterestRatePayout`, `cdm.product.common.schedule.CalculationPeriodDates`, `cdm.observable.asset.PriceQuantity`.
- **主要イベント/API**: `PriceProductCommand`, `SolveTradeParameterCommand`, `ValuationCalculatedEvent`.

### 2.4 Trade Negotiation & Confirmation Context (取引交渉・コンファーメーションコンテキスト)
- **主要目的**: 指値・確定プライシングにおけるトレーダー・顧客間の条件すり合わせ、与信枠（Credit Limit）のリアルタイム照会・確保、および合意（Approval）ステータスの制御。
- **Ubiquitous Language**: TradeProposal, LimitCheckRequest, StepApproval, ConfirmationWorkflow.
- **中心となるCDM構造**: `cdm.event.workflow.WorkflowStep`, `WorkflowStepApproval`, `CreditLimitInformation`, `EventInstruction`.
- **主要イベント/API**: `ProposeTradeCommand`, `ApproveWorkflowStepCommand`, `WorkflowStepUpdatedEvent`.

### 2.5 Trade Capture & Booking Context (ブッキング・取引管理コンテキスト)
- **主要目的**: 約定合意された取引の帳簿（Book/Portfolio）への公式確定登録、UTI（一意取引識別子）付与、`TradeState` の保存、および下流（ミドル・リスク・清算・決済）システムへの発行。
- **Ubiquitous Language**: BookedTrade, TradeState, ExecutionEvent, PortfolioPosition.
- **中心となるCDM構造**: `cdm.event.common.TradeState`, `BusinessEvent`, `cdm.event.position.Position`.
- **主要イベント/API**: `BookExecutionCommand`, `TradeBookedEvent` (CDM `BusinessEvent` 準拠).

### 2.6 約定条件 Solver（逆算・探索）処理の位置付けと PV エンジン依存性
デリバティブ取引において「NPV = 0 となるPar Rate（平準固定金利）の逆算」や「Target Premium を達成する Strike（行使価格）の探索」を行う **Solver 処理**の配置とコンテキスト構成は以下の通りです。

1. **コンテキストの所属**:
   - **主要計算エンジンとしての配置**: **Pricing & Risk Valuation Context**
     数値探索アルゴリズム（Newton-Raphson 法, Brent 法等）は各反復ステップで PV 算出を繰り返すため、低遅延なインメモリ評価が求められます。そのため Solver 処理は Pricing Service 内の計算機能として実装するのが一般的です。
   - **高レベル要求（Command）の発行元**: **Indication & Quoting Context** または **Trade Negotiation Context**
     営業やトレーダーが「NPV ゼロとなるスプレッドを解いてタームシート/オファーに設定する」ユースケースにおいて、`SolveTradeParameterCommand` を発行して Pricing Service の Solver 機能を呼び出します。

2. **PV 計算エンジン（Valuation Engine）との密結合性**:
   ご認識の通り、**Solver の実行には PV 計算エンジンが不可欠**です。
   Solver の目的関数は $f(x) = \text{PV}(x) - \text{TargetPV} = 0$ で表現され、探索変数 $x$ （Fixed Rate や Option Strike 等）を変更しながら PV エンジンを反復呼び出し（ループ）して収束判定を行います。ネットワーク経由の呼び出しオーバーヘッドを排除するため、Solver と PV エンジンは同一マイクロサービス内（または極めて高速なローカル IPC / メモリ内バインディング）で動作させる構成が推奨されます。

---

## 3. マイクロサービスアーキテクチャ設計

各 Bounded Context を独立したマイクロサービスとして設計し、疎結合かつ堅牢な分散アーキテクチャを実現します。

```
                       +-------------------------+
                       |   API Gateway / BFF     |
                       +------------+------------+
                                    |
          +-------------------------+-------------------------+
          | gRPC                    | REST/WebSocket          | gRPC
          v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| Market Data       |     | Indication &      |     | Pricing & Risk    |
| Gateway Service   |     | Quoting Service   |     | Analytics Service |
+---------+---------+     +---------+---------+     +---------+---------+
          |                         |                         |
          | PubSub                  | gRPC                    | gRPC
          v                         v                         |
    [ Market Data ]       +-------------------+               |
      Kafka Topic         | Trade Confirmation| <-------------+
                          | Workflow Service  |
                          +---------+---------+
                                    |
                                    | Event: WorkflowStep (Approved)
                                    v
                          [ Execution Event ]
                              Kafka Topic
                                    |
                                    v
                          +-------------------+
                          | Trade Booking     |
                          | & State Service   |
                          +---------+---------+
                                    |
                                    v
                             ( RDBMS / Store )
```

### 3.1 サービス間連携とプロトコル
- **同期型 API (gRPC)**: レテンシが要求されるリアルタイム計算（Pricing Service, Market Data Service）には Protobuf / gRPC を採用。
- **非同期型イベント (Event-Driven / Kafka)**: 取引ライフサイクルの進行やワークフローの状態遷移には Apache Kafka を使用し、ペイロードに CDM スキーマの JSON 表現 (`cdm.event.workflow.WorkflowStep`, `cdm.event.common.BusinessEvent`) を利用。

### 3.2 Anti-Corruption Layer (ACL: 防腐層) の設計方針
CDM は複雑かつ全網羅的なデータ構造を持つため、各マイクロサービス内部の永続化モデルやメモリ内ドメインオブジェクトに CDM クラスを直接使用することは推奨されません。

- **サービス内部**: 特定機能に特化した軽量かつ低遅延なドメインモデルを保持。
- **ACL レイヤー**: サービス境界（gRPC / REST Controller, Event Producer/Consumer）に ACL を配置し、Rosetta / CDM JSON オブジェクトと内部ドメインモデルの相互変換を隠蔽。

```
[ Internal Service Domain ] 
           ^
           | (Mapping via ACL)
           v
[ Anti-Corruption Layer (ACL) ]
           ^
           | (CDM JSON / Rosetta Java API)
           v
[ External / Inter-Service Kafka / gRPC ]
```

### 3.3 CQRS (Command Query Responsibility Segregation) パターン
- **Command Side (Trade Booking Service)**: 取引確定 (`Create_Execution`) と `TradeState` の状態変更トランザクションを一元管理。Transactional Outbox パターンを用いて信頼性の高いイベント送信を担保。
- **Query Side (Indication & Position Service)**: 読取専用のポジションビューや価格試算キャッシュを分離・保持し、超高速な検索・試算レスポンスを提供。

---

## 4. 今後の展開と CDM の発展的活用

1. **FpML / ISO20022 との相互変換**: `ingest-fpml-` モジュールを活用し、外部コンファーメーションネットワーク（DTCC, MarkitWire 等）との双方向変換ロジックを Trade Confirmation Service の ACL に統合可能。
2. **自動 Qualification ルーチンの適用**: 取引が完了した際、`cdm.product.qualification` および `cdm.event.qualification` の Rosetta 関数（`isQualifyingProduct`, `isQualifyingEvent`）を呼び出し、規制レポート（EMIR/MiFID II 等）用の商品・イベント区分の自動分類を実施。

---
- **関連ドキュメント**:
  - [cdm_architecture.md](../overview/cdm_architecture.md)
  - [product_modeling.md](product_modeling.md)
  - [event_lifecycle.md](event_lifecycle.md)
