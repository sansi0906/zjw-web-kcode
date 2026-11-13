# -*- coding: utf-8 -*-
"""CI/本地预检：YAML schema + pytest collect-only。"""
from __future__ import annotations
import argparse, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

def run(cmd, label):
    print(f"\n==> {label}: {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(ROOT))
    print("[OK]" if r.returncode == 0 else f"[FAIL] exit={r.returncode}", label)
    return r.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    rc = 0
    rc |= run([sys.executable, "scripts/validate_test_data.py"], "validate_test_data")
    rc |= run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:rerunfailures"], "collect-only")
    if not args.quick:
        rc |= run([sys.executable, "-m", "compileall", "-q", "tests", "pages", "utils", "config"], "compileall")
    print("\n==> precheck", "PASSED" if rc == 0 else "FAILED")
    return 1 if rc else 0

if __name__ == "__main__":
    raise SystemExit(main())
