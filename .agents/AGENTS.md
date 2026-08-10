# CDM ワークスペース エージェントルール & ハーネス指示書

## 1. CDM ソース探索ルール
- `common-domain-model/` 内のソースコードおよび DSL ファイル（Rosetta `.rosetta` DSL および手動・自動生成 Java コード）を探索・分析する際、エージェントは必ず [CDM_INDEX.md](../cdm_wiki/CDM_INDEX.md) を一次ナビゲーションインデックスおよび探索ガイドとして使用しなければならない。
- サフィックス（`-type`, `-func`, `-enum`, `-desc`）およびドメインプレフィックス（`base-`, `product-`, `event-`, `legaldocumentation-`, `observable-`, `ingest-fpml-`, `margin-schedule-`）に応じて、該当する Rosetta DSL ファイルを特定するには `CDM_INDEX.md` のセクション3（目的別検索ガイド）を参照すること。

## 2. CDM LLM-Wiki 操作ハーネス
- `cdm_wiki/` 内の CDM LLM-Wiki を操作する際（一次情報の取り込み、質問回答、または整合性チェックの実行時）、エージェントは事前に以下のドキュメントを読み、指示に従わなければならない：
  1. [README.md](../cdm_wiki/README.md)
  2. [SCHEMA.md](../cdm_wiki/SCHEMA.md)
- 質問回答（Query）時の自動Wiki還元をはじめ、すべての操作は [SCHEMA.md](../cdm_wiki/SCHEMA.md) 3.2 節（Query ワークフロー）等の規定に従って即座に反映・保存し、[index.md](../cdm_wiki/index.md) および [log.md](../cdm_wiki/log.md) を更新すること。

## 3. ローカルファイル探索・参照範囲の制限ルール
- エージェントはローカルファイルの探索・閲覧・操作を行う際、`cdm_wiki` および `common-domain-model` の2つのディレクトリ（およびその配下）のみを参照・操作対象としなければならない。それら以外の外部ディレクトリや上位ディレクトリへのアクセスおよび探索を一切行ってはならない。

