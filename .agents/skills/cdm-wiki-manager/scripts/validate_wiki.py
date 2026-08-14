#!/usr/bin/env python3
"""
validate_wiki.py - CDM LLM-Wiki 整合性・リンター検証スクリプト

CDM LLM-Wiki の構造規約、YAML Frontmatter、Markdown リンクの健全性、
index.md 登録状況、log.md フォーマットを自動検証します。
標準ライブラリのみで動作します。

使用法:
    python validate_wiki.py [--wiki-dir <path>]
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set

# Windows コンソールでの文字化け・エンコーディングエラー防止
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VALID_CATEGORIES = {"sources", "overview", "concepts", "entities", "functions"}
MANAGEMENT_FILES = {"CDM_INDEX.md", "README.md", "SCHEMA.md", "index.md", "log.md"}
VALID_LOG_ACTIONS = {"setup", "ingest", "query", "refactor", "lint", "update"}


class WikiValidator:
    def __init__(self, wiki_dir: Path, workspace_root: Path):
        self.wiki_dir = wiki_dir.resolve()
        self.workspace_root = workspace_root.resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checked_files_count = 0
        self.checked_links_count = 0

    def log_error(self, file_path: Path, msg: str):
        rel_path = file_path.relative_to(self.workspace_root) if file_path.is_relative_to(self.workspace_root) else file_path
        self.errors.append(f"❌ [ERROR] {rel_path}: {msg}")

    def log_warning(self, file_path: Path, msg: str):
        rel_path = file_path.relative_to(self.workspace_root) if file_path.is_relative_to(self.workspace_root) else file_path
        self.warnings.append(f"⚠️  [WARN]  {rel_path}: {msg}")

    def parse_frontmatter(self, file_path: Path, content: str) -> Dict[str, str]:
        """YAML frontmatter を簡易パースして辞書化する"""
        if not content.startswith("---"):
            self.log_error(file_path, "YAML Frontmatter が見つかりません（ファイルの先頭に '---' が必要です）。")
            return {}

        parts = content.split("---", 2)
        if len(parts) < 3:
            self.log_error(file_path, "YAML Frontmatter の終了タグ '---' が見つかりません。")
            return {}

        fm_text = parts[1].strip()
        data = {}
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                data[key.strip()] = val.strip()

        return data

    def validate_content_frontmatter(self, file_path: Path, content: str):
        """コンテンツページ（sources, concepts等）の Frontmatter を詳細検証"""
        fm = self.parse_frontmatter(file_path, content)
        if not fm:
            return

        # 必須フィールド
        for req in ["title", "category", "sources", "last_updated", "tags"]:
            if req not in fm:
                self.log_error(file_path, f"Frontmatter に必須キー '{req}' が不足しています。")

        # カテゴリ整合性
        cat = fm.get("category", "").strip("\"'")
        expected_cat = file_path.parent.name
        if cat not in VALID_CATEGORIES:
            self.log_error(file_path, f"category '{cat}' は無効です。有効値: {VALID_CATEGORIES}")
        elif cat != expected_cat:
            self.log_error(file_path, f"category '{cat}' が親ディレクトリ名 '{expected_cat}' と一致しません。")

        # 日付フォーマット
        last_updated = fm.get("last_updated", "").strip("\"'")
        if last_updated and not re.match(r"^\d{4}-\d{2}-\d{2}$", last_updated):
            self.log_error(file_path, f"last_updated '{last_updated}' が YYYY-MM-DD 形式ではありません。")

    def extract_markdown_links(self, content: str) -> List[Tuple[str, str]]:
        """Markdown リンク [text](url) を抽出する（コードブロック内は除外）"""
        # コードブロックをマスク
        no_code = re.sub(r"```[\s\S]*?```", "", content)
        no_code = re.sub(r"`[^`]*`", "", no_code)

        # Markdown リンクパターン: [text](link)
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        return re.findall(pattern, no_code)

    def validate_links_in_file(self, file_path: Path, content: str):
        """ファイル内の全 Markdown 相対リンクの実在性を検証"""
        links = self.extract_markdown_links(content)
        for text, link in links:
            link = link.strip()
            self.checked_links_count += 1

            # 外部 URL やメールリンクはスキップ
            if link.startswith(("http://", "https://", "mailto:", "ftp://")):
                continue

            # アンカーリンクのみ (#header) の場合
            if link.startswith("#"):
                continue

            # パスとアンカーの分離
            target_path_str = link.split("#")[0]
            if not target_path_str:
                continue

            # 相対パスを解決
            target_path = (file_path.parent / target_path_str).resolve()
            if not target_path.exists():
                self.log_error(
                    file_path,
                    f"リンク切れを検出: '{link}' (テキスト: '{text}') -> 解決先: {target_path}"
                )

    def validate_index_catalog(self, content_files: List[Path]):
        """index.md に全コンテンツページが登録されているかを検証"""
        index_file = self.wiki_dir / "index.md"
        if not index_file.exists():
            self.log_error(index_file, "index.md が存在しません。")
            return

        content = index_file.read_text(encoding="utf-8")
        indexed_links = self.extract_markdown_links(content)
        indexed_targets = set()
        for _, link in indexed_links:
            target_str = link.split("#")[0]
            if target_str and not target_str.startswith(("http://", "https://")):
                resolved = (index_file.parent / target_str).resolve()
                indexed_targets.add(resolved)

        for c_file in content_files:
            resolved_c_file = c_file.resolve()
            if resolved_c_file not in indexed_targets:
                self.log_error(
                    index_file,
                    f"孤立ページ検出: '{c_file.relative_to(self.wiki_dir)}' が index.md にリンクされていません。"
                )

    def validate_log_format(self):
        """log.md のフォーマットおよび構文を検証"""
        log_file = self.wiki_dir / "log.md"
        if not log_file.exists():
            self.log_error(log_file, "log.md が存在しません。")
            return

        content = log_file.read_text(encoding="utf-8")
        header_pattern = re.compile(r"^##\s+\[(\d{4}-\d{2}-\d{2})\]\s+([a-zA-Z0-9_-]+)\s+\|\s+(.+)$", re.MULTILINE)
        matches = header_pattern.findall(content)

        if not matches:
            self.log_warning(log_file, "## [YYYY-MM-DD] action | title 形式のログエントリが見つかりません。")
            return

        for date_str, action, title in matches:
            if action.lower() not in VALID_LOG_ACTIONS:
                self.log_warning(
                    log_file,
                    f"未知のログアクション種別 '{action}' (推奨: {sorted(list(VALID_LOG_ACTIONS))})"
                )

    def run(self) -> bool:
        print(f"🔍 CDM LLM-Wiki の整合性検証を開始: {self.wiki_dir}")
        print("-" * 60)

        # 全 .md ファイルを走査
        all_md_files = list(self.wiki_dir.glob("**/*.md"))
        content_files = []

        for md_file in all_md_files:
            self.checked_files_count += 1
            rel = md_file.relative_to(self.wiki_dir)
            content = md_file.read_text(encoding="utf-8")

            # リンク検証
            self.validate_links_in_file(md_file, content)

            # コンテンツページ判定
            if md_file.name in MANAGEMENT_FILES:
                continue

            if md_file.parent.name in VALID_CATEGORIES:
                content_files.append(md_file)
                self.validate_content_frontmatter(md_file, content)
            else:
                self.log_warning(md_file, f"未定義のサブディレクトリ '{md_file.parent.name}' に配置されています。")

        # index.md カタログ整合性検証
        self.validate_index_catalog(content_files)

        # log.md フォーマット検証
        self.validate_log_format()

        # 結果サマリー
        print(f"📊 検証完了: {self.checked_files_count} ファイル, {self.checked_links_count} リンクを検査しました。")
        print(f"   コンテンツページ数: {len(content_files)}")
        print("-" * 60)

        if self.warnings:
            print(f"⚠️  警告 ({len(self.warnings)} 件):")
            for w in self.warnings:
                print(f"  {w}")
            print("-" * 60)

        if self.errors:
            print(f"❌ エラー ({len(self.errors)} 件):")
            for e in self.errors:
                print(f"  {e}")
            print("-" * 60)
            print("🚫 Wiki 検証に失敗しました。上記のエラーを修正してください。")
            return False

        print("✅ すべての整合性チェックに合格しました！（Error: 0）")
        return True


def main():
    parser = argparse.ArgumentParser(description="CDM LLM-Wiki 整合性・リンター検証ツール")
    parser.add_argument(
        "--wiki-dir",
        type=str,
        default=None,
        help="cdm_wiki ディレクトリへのパス (デフォルト: 自動検出)"
    )
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    # .agents/skills/cdm-wiki-manager/scripts/validate_wiki.py -> parents[4] is workspace root
    workspace_root = script_path.parents[4]

    if args.wiki_dir:
        wiki_dir = Path(args.wiki_dir).resolve()
    else:
        # ワークスペース直下またはカレントディレクトリ直下の cdm_wiki を探す
        candidate1 = workspace_root / "cdm_wiki"
        candidate2 = Path.cwd() / "cdm_wiki"
        if candidate1.exists():
            wiki_dir = candidate1
        elif candidate2.exists():
            wiki_dir = candidate2
            workspace_root = Path.cwd()
        else:
            wiki_dir = candidate1

    if not wiki_dir.exists():
        print(f"Error: cdm_wiki ディレクトリが見つかりません: {wiki_dir}")
        sys.exit(1)

    validator = WikiValidator(wiki_dir=wiki_dir, workspace_root=workspace_root)
    success = validator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
