#!/usr/bin/env python3
"""
extract_git_diff_symbols.py - 一次ソース更新差分シンボル抽出 & 同期状態管理スクリプト

common-domain-model リポジトリの変更差分を解析し、
新規追加・削除された Type, Function, Enum を自動抽出して表示します。

デフォルト動作:
    cdm_wiki/.source_sync.json から前回の同期コミット（last_synced_commit）を読み込み、
    <last_synced_commit>..HEAD の差分を自動解析します（引数指定不要）。

使用法:
    # 1. 差分の自動解析 (前回同期コミット .. HEAD)
    python extract_git_diff_symbols.py

    # 2. 任意の範囲を指定して解析
    python extract_git_diff_symbols.py --range 7.0.0..HEAD

    # 3. 同期完了時: 現在の HEAD 状態を cdm_wiki/.source_sync.json に保存
    python extract_git_diff_symbols.py --save-state
"""

import sys
import os
import json
import subprocess
import re
import argparse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_sync_state_file(workspace_root: Path) -> Path:
    return workspace_root / "cdm_wiki" / ".source_sync.json"


def load_last_synced_commit(state_file: Path) -> str:
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            return data.get("last_synced_commit")
        except Exception as e:
            print(f"Warning: {state_file} の読み込みに失敗しました: {e}")
    return None


def save_current_sync_state(cdm_repo_dir: Path, state_file: Path):
    """現在の HEAD コミット・タグ・ブランチを .source_sync.json に保存する"""
    try:
        commit_short = subprocess.check_output(
            ["git", "-C", str(cdm_repo_dir), "rev-parse", "--short", "HEAD"],
            text=True, encoding="utf-8"
        ).strip()
        commit_full = subprocess.check_output(
            ["git", "-C", str(cdm_repo_dir), "rev-parse", "HEAD"],
            text=True, encoding="utf-8"
        ).strip()
    except Exception as e:
        print(f"Error: コミットハッシュの取得に失敗しました: {e}")
        return False

    # タグの取得（直近タグ）
    try:
        tag = subprocess.check_output(
            ["git", "-C", str(cdm_repo_dir), "describe", "--tags", "--abbrev=0"],
            text=True, encoding="utf-8"
        ).strip()
    except Exception:
        tag = "unknown"

    # ブランチの取得
    try:
        branch = subprocess.check_output(
            ["git", "-C", str(cdm_repo_dir), "branch", "--show-current"],
            text=True, encoding="utf-8"
        ).strip()
    except Exception:
        branch = "HEAD"

    now_date = datetime.now().strftime("%Y-%m-%d")

    data = {
        "last_synced_commit": commit_short,
        "last_synced_commit_full": commit_full,
        "last_synced_tag": tag,
        "last_synced_branch": branch,
        "last_synced_at": now_date
    }

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ 同期状態を保存しました: {state_file}")
    print(f"   Commit : {commit_short} ({commit_full})")
    print(f"   Tag    : {tag}")
    print(f"   Branch : {branch}")
    print(f"   Date   : {now_date}")
    return True


def extract_diff_symbols(cdm_repo_dir: Path, rev_range: str):
    print(f"🔍 Git 差分解析を実行中: {rev_range} (リポジトリ: {cdm_repo_dir})")
    print("-" * 70)

    # 1. diff --stat の取得
    stat_cmd = ["git", "-C", str(cdm_repo_dir), "diff", "--stat", rev_range, "--", "rosetta-source/src"]
    res_stat = subprocess.run(stat_cmd, capture_output=True, text=True, encoding="utf-8")
    if res_stat.returncode != 0:
        print(f"Error: git diff --stat に失敗しました: {res_stat.stderr}")
        sys.exit(1)

    stat_lines = [l for l in res_stat.stdout.splitlines() if l.strip()]
    if stat_lines:
        print(f"📈 変更概要: {stat_lines[-1]}")
    else:
        print("ℹ️  差分はありません（一次ソースは同一リビジョンです）。")
        return
    print("-" * 70)

    # 2. rosetta-source/src/main/rosetta のシンボル差分抽出
    diff_cmd = ["git", "-C", str(cdm_repo_dir), "diff", rev_range, "--", "rosetta-source/src/main/rosetta"]
    res_diff = subprocess.run(diff_cmd, capture_output=True, text=True, encoding="utf-8")
    if res_diff.returncode != 0:
        print(f"Error: git diff に失敗しました: {res_diff.stderr}")
        sys.exit(1)

    added_types = []
    added_funcs = []
    added_enums = []
    deleted_types = []
    deleted_funcs = []
    deleted_enums = []

    current_file = ""
    for line in res_diff.stdout.splitlines():
        if line.startswith("diff --git"):
            m = re.search(r'b/rosetta-source/src/main/rosetta/(.+)$', line)
            if m:
                current_file = m.group(1)
        elif line.startswith("+") and not line.startswith("+++"):
            clean = line[1:].strip()
            if clean.startswith("//") or clean.startswith("/*"):
                continue
            mt = re.match(r'^(?:type|choice)\s+([A-Za-z0-9_]+)', clean)
            if mt:
                added_types.append((current_file, mt.group(1)))
            mf = re.match(r'^func\s+([A-Za-z0-9_]+)', clean)
            if mf:
                added_funcs.append((current_file, mf.group(1)))
            me = re.match(r'^enum\s+([A-Za-z0-9_]+)', clean)
            if me:
                added_enums.append((current_file, me.group(1)))
        elif line.startswith("-") and not line.startswith("---"):
            clean = line[1:].strip()
            if clean.startswith("//") or clean.startswith("/*"):
                continue
            mt = re.match(r'^(?:type|choice)\s+([A-Za-z0-9_]+)', clean)
            if mt:
                deleted_types.append((current_file, mt.group(1)))
            mf = re.match(r'^func\s+([A-Za-z0-9_]+)', clean)
            if mf:
                deleted_funcs.append((current_file, mf.group(1)))
            me = re.match(r'^enum\s+([A-Za-z0-9_]+)', clean)
            if me:
                deleted_enums.append((current_file, me.group(1)))

    print(f"✨ 新規追加 Type ({len(added_types)} 件):")
    for f, name in added_types:
        print(f"  + [Type] {name:<40} ({f})")

    print(f"\n✨ 新規追加 Function ({len(added_funcs)} 件):")
    for f, name in added_funcs:
        print(f"  + [Func] {name:<40} ({f})")

    print(f"\n✨ 新規追加 Enum ({len(added_enums)} 件):")
    for f, name in added_enums:
        print(f"  + [Enum] {name:<40} ({f})")

    if deleted_types or deleted_funcs or deleted_enums:
        print("\n" + "=" * 70)
        print("⚠️  削除・リファクタリング対象シンボル:")
        for f, name in deleted_types:
            print(f"  - [Type] {name:<40} ({f})")
        for f, name in deleted_funcs:
            print(f"  - [Func] {name:<40} ({f})")
        for f, name in deleted_enums:
            print(f"  - [Enum] {name:<40} ({f})")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="一次ソース差分シンボル抽出 & 同期状態管理スクリプト")
    parser.add_argument("--range", type=str, default=None, help="Git 範囲 (例: 7.0.0..HEAD)。省略時は .source_sync.json を自動参照")
    parser.add_argument("--repo-dir", type=str, default=None, help="common-domain-model リポジトリパス")
    parser.add_argument("--save-state", action="store_true", help="現在の HEAD コミットを cdm_wiki/.source_sync.json に保存する")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[4]

    if args.repo_dir:
        repo_dir = Path(args.repo_dir).resolve()
    else:
        repo_dir = workspace_root / "common-domain-model"

    state_file = get_sync_state_file(workspace_root)

    if args.save_state:
        success = save_current_sync_state(repo_dir, state_file)
        sys.exit(0 if success else 1)

    rev_range = args.range
    if not rev_range:
        last_commit = load_last_synced_commit(state_file)
        if last_commit:
            rev_range = f"{last_commit}..HEAD"
            print(f"📌 {state_file.name} より前回同期コミット '{last_commit}' を検出しました。")
        else:
            print(f"Warning: {state_file} が見つからないため、デフォルト '7.0.0..HEAD' を使用します。")
            rev_range = "7.0.0..HEAD"

    extract_diff_symbols(repo_dir, rev_range)


if __name__ == "__main__":
    main()
