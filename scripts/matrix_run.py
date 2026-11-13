# -*- coding: utf-8 -*-
"""设备/浏览器矩阵执行器

对“无状态冒烟子集”（-m "smoke and not serial"）在多组设备/视口下执行，
输出汇总到 reports/matrix/matrix_<timestamp>.md。

用法：
    python scripts/matrix_run.py --list
    python scripts/matrix_run.py --quick            # 仅 Web 1920 + iPhone 12
    python scripts/matrix_run.py --full             # 全部矩阵
    python scripts/matrix_run.py --matrix web_1366,ipad
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# (名称, 平台, 设备名, 视口宽, 视口高)
MATRIX = [
    ("web_1920", "web", "", 1920, 1080),
    ("web_1366", "web", "", 1366, 768),
    ("ipad", "h5", "iPad", 0, 0),
    ("pixel5", "h5", "Pixel 5", 0, 0),
    ("iphone12", "h5", "iPhone 12", 0, 0),
]
QUICK = {"web_1920", "iphone12"}


def _run_one(item) -> dict:
    name, platform, device, width, height = item
    cmd = [
        sys.executable, "-m", "pytest",
        "-m", "smoke and not serial",
        "-q", "-p", "no:rerunfailures",
        "--platform", platform,
        f"--junitxml=reports/matrix/{name}.xml",
    ]
    if device:
        cmd += ["--device-name", device]
    if width:
        cmd += ["--viewport-width", str(width), "--viewport-height", str(height)]
    print(f"\n==> matrix {name}: {' '.join(cmd)}")
    started = time.time()
    proc = subprocess.run(cmd, cwd=str(ROOT))
    elapsed = round(time.time() - started, 1)
    print(f"[{'OK' if proc.returncode == 0 else 'FAIL'}] {name} ({elapsed}s)")
    return {"name": name, "platform": platform, "device": device or "default",
            "viewport": f"{width}x{height}" if width else "device-default",
            "exit_code": proc.returncode, "elapsed_s": elapsed}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--matrix", action="store", default="", help="逗号分隔的矩阵名称")
    args = ap.parse_args()

    if args.list:
        for item in MATRIX:
            print(f"{item[0]:10s} platform={item[1]:4s} device={item[2] or '-':10s} viewport={item[3]}x{item[4]}")
        return 0

    if args.matrix:
        selected = {n.strip() for n in args.matrix.split(",") if n.strip()}
        items = [i for i in MATRIX if i[0] in selected]
        unknown = selected - {i[0] for i in MATRIX}
        if unknown:
            print(f"未知矩阵名称: {sorted(unknown)}；可用: {[i[0] for i in MATRIX]}")
            return 2
    elif args.full:
        items = MATRIX
    else:
        items = [i for i in MATRIX if i[0] in QUICK]

    out_dir = ROOT / "reports" / "matrix"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = [_run_one(i) for i in items]
    stamp = time.strftime("%Y%m%d_%H%M%S")
    summary = out_dir / f"matrix_{stamp}.md"
    lines = [
        f"# 设备/浏览器矩阵报告 {stamp}",
        "",
        "| 矩阵 | 平台 | 设备 | 视口 | 结果 | 耗时(s) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        verdict = "PASS" if r["exit_code"] == 0 else f"FAIL({r['exit_code']})"
        lines.append(f"| {r['name']} | {r['platform']} | {r['device']} | {r['viewport']} | {verdict} | {r['elapsed_s']} |")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / f"matrix_{stamp}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n==> 矩阵汇总: {summary}")
    print("\n".join(lines))
    return 0 if all(r["exit_code"] == 0 for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())