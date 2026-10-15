#!/usr/bin/env python3
"""
CDM WorkflowStep Validation Dispatcher
CDM 7.x (v7.5.0) and CDM 6.x (v6.29.0) dual-engine automated probing runner.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JAR_V7 = BASE_DIR / "target" / "cdm-validator-v7.jar"
JAR_V6 = BASE_DIR / "target" / "cdm-validator-v6.jar"


def run_validator(jar_path: Path, json_file: str):
    """Run a specific validator jar and return (exit_code, output)."""
    cmd = ["java", "-jar", str(jar_path), json_file]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = proc.stdout.strip()
        if not output and proc.stderr:
            output = proc.stderr.strip()
        return proc.returncode, output
    except Exception as e:
        return 1, f"STATUS   : FAIL (Exit Code: 1)\nFAILURES :\n[1] Type  : EXECUTION_ERROR\n    Reason: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="CDM WorkflowStep Dual-Engine Validator")
    parser.add_argument("json_file", help="Path to WorkflowStep JSON file")
    parser.add_argument(
        "--version",
        "-v",
        choices=["6", "7"],
        default=None,
        help="Explicitly specify CDM model version (6 or 7). If omitted, auto-probes.",
    )

    args = parser.parse_args()
    json_path = os.path.abspath(args.json_file)

    if not os.path.exists(json_path):
        print("STATUS   : FAIL (Exit Code: 1)")
        print("FAILURES :")
        print(f"[1] Type  : FILE_NOT_FOUND\n    Reason: File not found: {args.json_file}")
        sys.exit(1)

    if not JAR_V7.exists() or not JAR_V6.exists():
        print("STATUS   : FAIL (Exit Code: 1)")
        print("FAILURES :")
        print("[1] Type  : VALIDATOR_JAR_MISSING")
        print(f"    Reason: Missing jar(s) in {BASE_DIR / 'target'}. Run 'mvn package -DskipTests' first.")
        sys.exit(1)

    # 1. Explicit version mode
    if args.version == "7":
        code, out = run_validator(JAR_V7, json_path)
        print(out)
        sys.exit(code)
    elif args.version == "6":
        code, out = run_validator(JAR_V6, json_path)
        print(out)
        sys.exit(code)

    # 2. Automated Probing Mode (Default)
    # Step A: Probe with CDM 7.x (Standard)
    code_v7, out_v7 = run_validator(JAR_V7, json_path)
    if code_v7 == 0:
        print(out_v7)
        sys.exit(0)

    # Step B: Probe with CDM 6.x
    code_v6, out_v6 = run_validator(JAR_V6, json_path)
    if code_v6 == 0:
        print(out_v6)
        sys.exit(0)

    # Step C: Both failed. Diagnose which model is the intended/closer fit.
    v7_is_deser_err = "DESERIALIZATION_ERROR" in out_v7
    v6_is_deser_err = "DESERIALIZATION_ERROR" in out_v6

    if v7_is_deser_err and not v6_is_deser_err:
        # CDM 6.x deserialized successfully, but 7.x failed to deserialize -> Intended model is CDM 6.x
        print(out_v6)
        sys.exit(1)
    elif v6_is_deser_err and not v7_is_deser_err:
        # CDM 7.x deserialized successfully, but 6.x failed to deserialize -> Intended model is CDM 7.x
        print(out_v7)
        sys.exit(1)
    else:
        # Count failures in output
        failures_v7 = out_v7.count("\n[") + (1 if out_v7.startswith("[") else 0)
        failures_v6 = out_v6.count("\n[") + (1 if out_v6.startswith("[") else 0)

        if failures_v6 > 0 and failures_v6 < failures_v7:
            print(out_v6)
        else:
            # Default to standard v7
            print(out_v7)
        sys.exit(1)


if __name__ == "__main__":
    main()
