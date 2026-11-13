"""从 pytest 用例导出测试用例清单（Markdown / CSV / Excel）。

用法：
    python scripts/export_test_cases.py                     # 生成 md + csv + xlsx
    python scripts/export_test_cases.py --format md         # 仅 Markdown
    python scripts/export_test_cases.py --format csv        # 仅 CSV
    python scripts/export_test_cases.py --format xlsx       # 仅 Excel
    python scripts/export_test_cases.py --output-dir docs/test_cases

说明：用例信息来自 AST 解析（不导入测试模块，避免触发浏览器 fixture）。
"""
from __future__ import annotations

import argparse
import ast
import csv
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = ROOT / "tests"

# 测试文件名（不含 test_ 前缀）-> 中文页面/模块名
PAGE_NAME_MAP = {
    "achievement_transformation": "成果转化",
    "achievement_transformation_fonts": "成果转化",
    "industry_association": "产业协会",
    "industry_association_fonts": "产业协会",
    "industry_news": "产业资讯",
    "industry_news_fonts": "产业资讯",
    "intelligent_construction": "智能建造",
    "intelligent_construction_fonts": "智能建造",
    "cloud_service": "云服务",
    "cloud_service_fonts": "云服务",
    "industrial_service": "产业化服务",
    "demand_page": "产业需求",
    "demand_page_fonts": "产业需求",
    "exhibition": "会展活动",
    "key_projects": "重点项目",
    "key_project_fonts": "重点项目",
    "supply_hall": "供应大厅",
    "supply_hall_fonts": "供应大厅",
    "supply_hall_search_result": "供应大厅-搜索结果",
    "homepage_full": "首页",
    "homepage_fonts": "首页",
    "homepage_h5_fonts": "首页-H5",
    "homepage_h5_smoke": "首页-H5",
    "homepage_nav_search": "首页-导航与搜索",
    "h5_pages_smoke": "H5-列表页",
    "error_pages": "异常与404",
    "resilience": "异常与韧性",
    "a11y_basic": "可访问性",
    "visual_regression": "视觉回归",
    "login_flow": "登录",
    "register_validation": "注册",
    "page_interaction": "通用交互",
}

SEVERITY_MAP = {
    "BLOCKER": "阻塞",
    "CRITICAL": "严重",
    "NORMAL": "一般",
    "MINOR": "轻微",
    "TRIVIAL": "提示",
}

HEADERS = [
    "用例编号",
    "模块",
    "页面",
    "用例名称",
    "用例标题",
    "Feature",
    "Story",
    "严重程度",
    "测试类型",
    "前置条件",
    "测试步骤",
    "预期结果",
    "测试状态",
    "备注",
]


def _decorator_attr(node: ast.AST, name: str) -> str:
    """返回 @allure.xxx(...) 中的 name；非该装饰器返回空串。"""
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == name:
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            return node.args[0].value
    return ""


def _decorator_severity(node: ast.AST) -> str:
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "severity":
        if node.args and isinstance(node.args[0], ast.Attribute):
            return node.args[0].attr
    return ""


def _class_assigns(node: ast.ClassDef) -> dict:
    values = {}
    for item in node.body:
        if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name):
            if isinstance(item.value, ast.Constant):
                values[item.targets[0].id] = item.value.value
    return values


def _parse_module(path: Path) -> dict:
    """解析测试文件，返回 {类名: {方法名: meta}} 及类级 feature。"""
    classes: dict[str, dict] = {}
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    except SyntaxError:
        return classes
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        feature = next((_decorator_attr(d, "feature") for d in node.decorator_list if _decorator_attr(d, "feature")), "")
        methods: dict[str, dict] = {}
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) or not item.name.startswith("test_"):
                continue
            title = next((_decorator_attr(d, "title") for d in item.decorator_list if _decorator_attr(d, "title")), "")
            story = next((_decorator_attr(d, "story") for d in item.decorator_list if _decorator_attr(d, "story")), "")
            severity_raw = next((_decorator_severity(d) for d in item.decorator_list if _decorator_severity(d)), "")
            doc = (ast.get_docstring(item) or "").strip()
            methods[item.name] = {
                "feature": feature,
                "story": story,
                "title": title or (doc.splitlines()[0] if doc else item.name),
                "severity": SEVERITY_MAP.get(severity_raw.upper(), severity_raw) if severity_raw else "一般",
                "doc": doc.replace("\n", "; ") if doc else "见用例实现",
            }
        classes[node.name] = methods
    return classes


def _collect_nodeids() -> list[str]:
    """通过 pytest --collect-only 枚举真实用例 nodeid（含继承与参数化）。"""
    import re
    import subprocess

    proc = subprocess.run(
        ["python", "-m", "pytest", "--collect-only", "-q", "-q", "-p", "no:rerunfailures"],
        cwd=ROOT,
        capture_output=True,
    )
    out = proc.stdout.decode("utf-8", "replace")
    ids = []
    for line in out.splitlines():
        text = re.sub(r"\x1b\[[0-9;]*m", "", line).strip()
        if text.startswith("tests/") and "::" in text:
            ids.append(text)
    return ids


def collect_cases() -> list[dict]:
    """按 pytest 收集结果生成用例清单（同一方法的参数化用例合并为一条）。"""
    base_meta = {}
    for base in (TEST_DIR / "base_page_test.py",):
        if base.exists():
            for methods in _parse_module(base).values():
                base_meta.update(methods)

    module_ast: dict[str, dict] = {}
    for path in sorted(TEST_DIR.glob("test_*.py")):
        module_ast[path.stem] = _parse_module(path)

    nodeids = _collect_nodeids()
    seen: set[tuple[str, str, str]] = set()
    cases: list[dict] = []
    idx = 1

    for nodeid in nodeids:
        parts = nodeid.split("::")
        stem = parts[0].split("/")[-1][: -len(".py")]
        class_name = parts[1] if len(parts) > 2 else ""
        method = parts[-1].split("[")[0]
        key = (stem, class_name, method)
        if key in seen:
            continue
        seen.add(key)

        methods = module_ast.get(stem, {}).get(class_name, {})
        meta = methods.get(method) or base_meta.get(method) or {}
        page_key = stem[len("test_"):] if stem.startswith("test_") else stem
        module = PAGE_NAME_MAP.get(page_key, class_name or stem)
        doc = meta.get("doc") or "见用例实现"
        cases.append(
            {
                "用例编号": f"TC-{idx:03d}",
                "模块": module,
                "页面": module,
                "用例名称": f"{class_name}.{method}" if class_name else method,
                "用例标题": meta.get("title") or method,
                "Feature": meta.get("feature", ""),
                "Story": meta.get("story", ""),
                "严重程度": meta.get("severity") or "一般",
                "测试类型": "参数化" if "[" in parts[-1] else "功能",
                "前置条件": "已部署可访问的被测站点，测试数据见 data/test_data.yaml",
                "测试步骤": doc,
                "预期结果": "用例内断言全部通过（无未预期异常/元素缺失）",
                "测试状态": "",
                "备注": nodeid,
            }
        )
        idx += 1
    return cases


def _group(cases: list[dict]) -> "OrderedDict[str, list[dict]]":
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for case in cases:
        grouped.setdefault(case["模块"], []).append(case)
    return grouped


def write_markdown(cases: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# 测试用例清单")
    lines.append("")
    lines.append(f"- 用例总数：{len(cases)}")
    lines.append(f"- 模块数：{len(_group(cases))}")
    lines.append("- 生成方式：`python scripts/export_test_cases.py`（pytest --collect-only 枚举 + AST 解析元数据，不执行用例）")
    lines.append("")
    lines.append("## 模块统计")
    lines.append("")
    lines.append("| 模块 | 用例数 |")
    lines.append("|------|--------|")
    for module, items in _group(cases).items():
        lines.append(f"| {module} | {len(items)} |")
    lines.append("")
    lines.append("## 用例明细")
    lines.append("")
    for module, items in _group(cases).items():
        lines.append(f"### {module}（{len(items)}）")
        lines.append("")
        lines.append("| 编号 | 用例名称 | 用例标题 | 严重程度 |")
        lines.append("|------|----------|----------|----------|")
        for case in items:
            title = case["用例标题"].replace("|", "\\|")
            lines.append(f"| {case['用例编号']} | {case['用例名称']} | {title} | {case['严重程度']} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(cases: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(cases)


def write_xlsx(cases: list[dict], path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for col, header in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row_idx, case in enumerate(cases, 2):
        for col_idx, header in enumerate(HEADERS, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=case.get(header, ""))
            cell.alignment = Alignment(vertical="center", wrap_text=True)
    for i, width in enumerate([10, 18, 22, 26, 32, 18, 18, 10, 10, 30, 40, 32, 10, 44], 1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = width
    ws.freeze_panes = "A2"
    wb.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="导出测试用例清单")
    parser.add_argument("--format", choices=["md", "csv", "xlsx", "all"], default="all")
    parser.add_argument("--output-dir", default="docs/test_cases", help="输出目录（默认 docs/test_cases）")
    args = parser.parse_args()

    out_dir = (ROOT / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cases = collect_cases()
    if not cases:
        raise SystemExit("未收集到用例，请确认 tests/ 目录")

    written = []
    if args.format in ("md", "all"):
        target = out_dir / "test_cases.md"
        write_markdown(cases, target)
        written.append(target)
    if args.format in ("csv", "all"):
        target = out_dir / "test_cases.csv"
        write_csv(cases, target)
        written.append(target)
    if args.format in ("xlsx", "all"):
        target = out_dir / "test_cases.xlsx"
        write_xlsx(cases, target)
        written.append(target)

    severity = Counter(case["严重程度"] for case in cases)
    print(f"用例总数: {len(cases)}  模块数: {len(_group(cases))}")
    print("严重程度分布: " + ", ".join(f"{k}={v}" for k, v in severity.most_common()))
    for target in written:
        print(f"已生成: {target.relative_to(ROOT).as_posix()} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()