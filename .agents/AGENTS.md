# CDM ワークスペース エージェントルール & ハーネス指示書

本ファイルは、本ワークスペース（CDM LLM-Wiki & FINOS CDM コードベース）におけるエージェントの基本行動規範およびハーネス規定を定義します。

---

## 1. ローカルファイル探索・参照範囲の制限（厳格ルール）
- エージェントはローカルファイルの探索・閲覧・操作を行う際、`cdm_wiki` および `common-domain-model`、および `.agents` のディレクトリ（およびその配下）のみを参照・操作対象としなければならない。
- それら以外の外部ディレクトリや上位ディレクトリへのアクセスおよび探索を一切行ってはならない。
- `common-domain-model/` 内のソースコードおよび DSL ファイルは**読み取り専用（一次情報）**であり、直接編集してはならない。

---

## 2. 外部 URL 事前接続確認の義務（絶対ルール）
- **Wiki に掲載・追加する外部 URL（HTTP/HTTPS）は、必ず事前に HTTP 接続テスト（ステータス 200 OK）を行い、実在性と疎通性を検証しなければならない。**
- 推測や未検証の URL、リンク切れの URL を掲載することは厳格に禁止する。
- 編集後は必ず付属のリンタースクリプト（外部 URL 接続確認機能付き）を実行し、エラー 0 件であることを確認すること：
  ```bash
  python .agents/skills/cdm-wiki-manager/scripts/validate_wiki.py
  ```

---

## 3. CDM ソースコード・DSL 探索ハーネス
- `common-domain-model/` 内の Rosetta DSL（`.rosetta`）および Java コードを探索する際は、必ず [CDM_INDEX.md](../cdm_wiki/CDM_INDEX.md) を一次インデックスとして使用する。
- 探索・分析の詳細手順やファイルプレフィックス・サフィックス早見表については、ワークスペーススキル [cdm-navigator](skills/cdm-navigator/SKILL.md) を活用すること。

---

## 4. CDM LLM-Wiki 運用 & 自動還元ハーネス
- `cdm_wiki/` 内の操作（一次情報取り込み、質問回答、整合性チェック）を行う際は、以下の規定を遵守する：
  1. **自動 Wiki 還元の徹底**: 質問回答（Query）によって新しい知見・マッピング・構造比較が得られた場合、回答と同時に必ず `cdm_wiki/`（`concepts/` や `entities/` 等）へ即座に反映・保存すること。
  2. **カタログ & ログ同期**: ページの作成・更新後は [index.md](../cdm_wiki/index.md) および [log.md](../cdm_wiki/log.md) を即座に更新すること。
  3. **自動バリデーション実行**: 編集後はリンタースクリプト `validate_wiki.py` を実行してエラー 0 件を確認すること。
  4. 詳細手順・規約については、ワークスペーススキル [cdm-wiki-manager](skills/cdm-wiki-manager/SKILL.md) および [SCHEMA.md](../cdm_wiki/SCHEMA.md) を参照すること。
