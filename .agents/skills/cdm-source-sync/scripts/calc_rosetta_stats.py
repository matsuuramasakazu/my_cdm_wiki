#!/usr/bin/env python3
"""
calc_rosetta_stats.py - Rosetta DSL 定義メトリクス精密集計スクリプト

common-domain-model/rosetta-source/src/main/rosetta 配下の全 .rosetta ファイルを走査し、
Type（型定義・choice）、Function（関数定義）、Enum（列挙型）の総数および
7 つの主要ドメインプレフィックス別・名前空間別の内訳を集計して出力します。

使用法:
    python calc_rosetta_stats.py [--rosetta-dir <path>]
"""

import os
import sys
import glob
import re
import argparse
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def analyze_rosetta_files(rosetta_dir: Path):
    files = sorted(list(rosetta_dir.glob("*.rosetta")))
    if not files:
        print(f"Error: .rosetta ファイルが見つかりません: {rosetta_dir}")
        sys.exit(1)

    domain_stats = defaultdict(lambda: {"files": 0, "types": 0, "funcs": 0, "enums": 0})
    ns_types = defaultdict(int)
    ns_funcs = defaultdict(int)
    ns_enums = defaultdict(int)

    total_stats = {"files": 0, "types": 0, "funcs": 0, "enums": 0}

    # 主要ドメインの定義（表示順序を定義。プレフィックス判定時は長い順に自動ソートして評価）
    KNOWN_DOMAINS = [
        "ingest-fpml-",
        "product-",
        "legaldocumentation-",
        "base-",
        "event-",
        "observable-",
        "margin-schedule-",
    ]
    prefix_matching_order = sorted(KNOWN_DOMAINS, key=len, reverse=True)

    for f in files:
        fname = f.name
        domain = None
        for p in prefix_matching_order:
            if fname.startswith(p):
                domain = p
                break
        if not domain:
            if "-" in fname:
                domain = fname.split("-")[0] + "-"
            else:
                domain = f.stem + "-"

        content = f.read_text(encoding="utf-8")

        # 名前空間の抽出
        m_ns = re.search(r"^\s*namespace\s+([A-Za-z0-9_\.]+)", content, re.MULTILINE)
        ns = m_ns.group(1) if m_ns else "unknown"

        # コメントのマスク（/* ... */ および // ...）
        content_clean = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        content_clean = re.sub(r"//.*", "", content_clean)

        t = len(re.findall(r"^\s*(?:type|choice)\s+([A-Za-z0-9_]+)", content_clean, re.MULTILINE))
        fn = len(re.findall(r"^\s*func\s+([A-Za-z0-9_]+)", content_clean, re.MULTILINE))
        e = len(re.findall(r"^\s*enum\s+([A-Za-z0-9_]+)", content_clean, re.MULTILINE))

        domain_stats[domain]["files"] += 1
        domain_stats[domain]["types"] += t
        domain_stats[domain]["funcs"] += fn
        domain_stats[domain]["enums"] += e

        ns_types[ns] += t
        ns_funcs[ns] += fn
        ns_enums[ns] += e

        total_stats["files"] += 1
        total_stats["types"] += t
        total_stats["funcs"] += fn
        total_stats["enums"] += e

    print("=" * 70)
    print("📊 Rosetta DSL 定義メトリクス集計結果")
    print("=" * 70)
    print(f"総ファイル数 : {total_stats['files']:>5} ファイル")
    print(f"総 Type 数   : {total_stats['types']:>5} 型")
    print(f"総 Func 数   : {total_stats['funcs']:>5} 関数")
    print(f"総 Enum 数   : {total_stats['enums']:>5} 列挙型")
    print("-" * 70)
    print(f"{'ドメイン（プレフィックス）':<24} | {'Files':>5} | {'Types':>5} | {'Funcs':>5} | {'Enums':>5}")
    print("-" * 70)

    # 主要ドメインの表示順を維持しつつ、新設された未知のドメインも自動抽出して末尾に表示
    other_domains = sorted([d for d in domain_stats.keys() if d not in KNOWN_DOMAINS])
    all_domains_to_show = [d for d in KNOWN_DOMAINS if d in domain_stats] + other_domains

    for d in all_domains_to_show:
        s = domain_stats[d]
        print(f"{d:<24} | {s['files']:>5} | {s['types']:>5} | {s['funcs']:>5} | {s['enums']:>5}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Rosetta DSL 定義メトリクス精密集計スクリプト")
    parser.add_argument("--rosetta-dir", type=str, default=None, help="rosetta ソースディレクトリ")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[4]

    if args.rosetta_dir:
        rosetta_dir = Path(args.rosetta_dir).resolve()
    else:
        rosetta_dir = workspace_root / "common-domain-model" / "rosetta-source" / "src" / "main" / "rosetta"

    analyze_rosetta_files(rosetta_dir)


if __name__ == "__main__":
    main()
