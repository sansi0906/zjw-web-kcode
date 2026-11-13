# -*- coding: utf-8 -*-
"""CI/本地前置校验：验证 data/test_data.yaml 结构。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.conftest import load_test_data  # noqa: E402


def main() -> int:
    try:
        data = load_test_data()
    except Exception as e:
        print(f"test_data 校验失败: {e}")
        return 1
    pages = len(data.get("font_tests", {}))
    print(
        f"test_data 校验通过: {pages} 个 font_tests 页面, {len(data.keys())} 个顶层 key"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
