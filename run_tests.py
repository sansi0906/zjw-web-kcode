"""
运行测试并生成报告的主脚本
用法:
    python run_tests.py --tester "测试人员姓名" --remark "测试备注"
    python run_tests.py --env staging --headless
    python run_tests.py --screenshot-all
    python run_tests.py --parallel 4
"""
from __future__ import annotations

import os
import sys
import subprocess
import argparse
import shutil
import datetime
from pathlib import Path

from config.settings import settings


def clean_reports(reports_dir: str, run_dir: str) -> None:
    """清理旧的报告文件（仅清理当前运行目录）"""
    print(f"准备报告目录: {run_dir}")

    allure_results = os.path.join(run_dir, "allure-results")
    os.makedirs(allure_results, exist_ok=True)

    html_dir = os.path.join(run_dir, "html")
    os.makedirs(html_dir, exist_ok=True)


def clean_all(reports_dir: str, keep_days: int = 7) -> None:
    """清理超过 keep_days 天的旧运行目录、截图、日志和 BUG 清单"""
    import time

    cutoff = time.time() - (keep_days * 24 * 3600)
    cleaned = 0

    # 清理 reports/ 下的旧运行目录
    if os.path.isdir(reports_dir):
        for name in os.listdir(reports_dir):
            path = os.path.join(reports_dir, name)
            if os.path.isdir(path) and name.startswith("run_"):
                try:
                    mtime = os.path.getmtime(path)
                    if mtime < cutoff:
                        shutil.rmtree(path)
                        cleaned += 1
                        print(f"  清理旧运行目录: {path}")
                except Exception as e:
                    print(f"  清理失败 {path}: {e}")

    # 清理旧截图（按时间戳子目录）
    screenshots_dir = os.path.join(reports_dir, "screenshots")
    if os.path.isdir(screenshots_dir):
        for name in os.listdir(screenshots_dir):
            path = os.path.join(screenshots_dir, name)
            if os.path.isdir(path) and name.startswith("run_"):
                try:
                    mtime = os.path.getmtime(path)
                    if mtime < cutoff:
                        shutil.rmtree(path)
                        cleaned += 1
                        print(f"  清理旧截图目录: {path}")
                except Exception as e:
                    print(f"  清理失败 {path}: {e}")

    # 清理旧日志
    logs_dir = os.path.join(os.path.dirname(reports_dir), "logs")
    if os.path.isdir(logs_dir):
        for name in os.listdir(logs_dir):
            path = os.path.join(logs_dir, name)
            if os.path.isfile(path):
                try:
                    mtime = os.path.getmtime(path)
                    if mtime < cutoff:
                        os.remove(path)
                        cleaned += 1
                        print(f"  清理旧日志: {path}")
                except Exception as e:
                    print(f"  清理失败 {path}: {e}")

    # 清理旧 BUG 清单
    bugs_dir = os.path.join(os.path.dirname(reports_dir), "bugs")
    if os.path.isdir(bugs_dir):
        for name in os.listdir(bugs_dir):
            path = os.path.join(bugs_dir, name)
            if os.path.isfile(path):
                try:
                    mtime = os.path.getmtime(path)
                    if mtime < cutoff:
                        os.remove(path)
                        cleaned += 1
                        print(f"  清理旧 BUG 清单: {path}")
                except Exception as e:
                    print(f"  清理失败 {path}: {e}")

    print(f"共清理 {cleaned} 个旧文件/目录（保留 {keep_days} 天内）")


def run_tests(
    tester: str = "",
    remark: str = "",
    screenshot_all: bool = False,
    reports_dir: str = "",
    viewport_width: int = 1920,
    viewport_height: int = 1080,
    test_url: str = "",
    env_name: str = "dev",
    headless: bool = False,
    parallel: int = 1,
    run_dir: str = "",
) -> tuple[int, str]:
    """运行测试，返回 (exit_code, run_dir)"""
    print("\n" + "=" * 60)
    print("开始运行测试...")
    print(f"环境: {env_name}")
    print(f"测试地址: {test_url or settings.env_config.base_url}")
    print(f"视口: {viewport_width}x{viewport_height}")
    print(f"无头模式: {headless}")
    print(f"并行数: {parallel}")
    if screenshot_all:
        print("截图模式: 全部测试截图")
    print("=" * 60 + "\n")

    # 生成唯一运行目录
    if not run_dir:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = f"run_{timestamp}"
        run_dir = os.path.join(reports_dir, run_name)

    # 设置环境变量
    env = os.environ.copy()
    env["REPORT_NAME"] = os.path.basename(run_dir)
    env["SCREENSHOT_DIR"] = os.path.join(reports_dir, "screenshots", os.path.basename(run_dir))
    env["ALLURE_RESULTS_DIR"] = os.path.join(run_dir, "allure-results")

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--alluredir", os.path.join(run_dir, "allure-results"),
        "--viewport-width", str(viewport_width),
        "--viewport-height", str(viewport_height),
        "--env", env_name,
    ]

    if tester:
        cmd.extend(["--tester", tester])
    if remark:
        cmd.extend(["--remark", remark])
    if screenshot_all:
        cmd.append("--screenshot-all")
    if test_url:
        cmd.extend(["--test-url", test_url])
    if headless:
        cmd.append("--headless")
    if parallel > 1:
        cmd.extend(["-n", str(parallel)])

    # 运行测试
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__), env=env)
    return result.returncode, run_dir


def generate_html_report(tester: str = "", remark: str = "", run_dir: str = "") -> str:
    """生成 Allure HTML 报告到运行目录"""
    print("\n" + "=" * 60)
    print("生成测试报告...")
    print("=" * 60 + "\n")

    if not run_dir:
        print("警告: 未指定运行目录，跳过 HTML 报告生成")
        return ""

    allure_results = os.path.join(run_dir, "allure-results")
    report_dir = os.path.join(run_dir, "html")

    if not os.path.exists(allure_results) or not os.listdir(allure_results):
        print(f"警告: Allure 结果目录为空: {allure_results}")
        print("跳过 HTML 报告生成")
        return ""

    cmd = [
        "allure", "generate",
        allure_results,
        "-o", report_dir,
        "--clean",
    ]

    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__), check=False, shell=True)
        if result.returncode != 0:
            print(f"Allure 报告生成返回码: {result.returncode}")
    except FileNotFoundError:
        print("错误: 未找到 allure 命令，请确保 Allure 已安装并在 PATH 中")
        print(f"当前 PATH: {os.environ.get('PATH', '')[:500]}")
        return ""

    output_file = os.path.join(report_dir, "index.html")
    if os.path.exists(output_file):
        print(f"HTML 报告已生成: {output_file}")
        return output_file
    return ""


def generate_bug_list(run_dir: str, tester: str = "", remark: str = "") -> str:
    """从 Allure 结果生成 BUG 清单（Markdown）"""
    import json
    import xml.etree.ElementTree as ET

    allure_results = os.path.join(run_dir, "allure-results")
    bugs_dir = os.path.join(os.path.dirname(run_dir), "bugs")
    os.makedirs(bugs_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bug_file = os.path.join(bugs_dir, f"bugs_{timestamp}.md")

    failed_tests = []
    total = passed = failed = skipped = 0

    if os.path.isdir(allure_results):
        for fname in os.listdir(allure_results):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(allure_results, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            total += 1
            status = data.get("status", "")
            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
                failed_tests.append({
                    "name": data.get("name", ""),
                    "full_name": data.get("fullName", ""),
                    "status": status,
                    "status_message": data.get("statusDetails", {}).get("message", ""),
                    "trace": data.get("statusDetails", {}).get("trace", ""),
                    "duration": data.get("stop", 0) - data.get("start", 0) if data.get("start") else 0,
                    "labels": {l["name"]: l["value"] for l in data.get("labels", [])},
                })
            elif status == "skipped":
                skipped += 1

    with open(bug_file, "w", encoding="utf-8") as f:
        f.write(f"# BUG 清单\n\n")
        f.write(f"- **测试环境**: {os.environ.get('TEST_ENV', 'dev')}\n")
        f.write(f"- **测试地址**: {os.environ.get('TEST_BASE_URL', '')}\n")
        f.write(f"- **测试人员**: {tester or '未指定'}\n")
        f.write(f"- **测试备注**: {remark or '无'}\n")
        f.write(f"- **生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **运行目录**: {run_dir}\n\n")
        f.write(f"## 统计\n\n")
        f.write(f"| 指标 | 数值 |\n")
        f.write(f"|------|------|\n")
        f.write(f"| 总计 | {total} |\n")
        f.write(f"| 通过 | {passed} |\n")
        f.write(f"| 失败 | {failed} |\n")
        f.write(f"| 跳过 | {skipped} |\n\n")

        if failed_tests:
            f.write(f"## 失败用例详情\n\n")
            for i, bug in enumerate(failed_tests, 1):
                f.write(f"### {i}. {bug['name']}\n\n")
                f.write(f"- **全称**: `{bug['full_name']}`\n")
                f.write(f"- **状态**: {bug['status']}\n")
                if bug["status_message"]:
                    f.write(f"- **错误信息**: {bug['status_message']}\n")
                if bug["trace"]:
                    f.write(f"- **堆栈跟踪**:\n\n```\n{bug['trace'][:500]}\n```\n\n")
                if bug["labels"]:
                    f.write(f"- **标签**: {bug['labels']}\n")
                f.write(f"- **耗时**: {bug['duration']}ms\n\n")
        else:
            f.write(f"## 失败用例详情\n\n")
            f.write(f"无失败用例。\n\n")

    print(f"BUG 清单已生成: {bug_file}")
    return bug_file
    """使用 allure serve 打开报告"""
    import webbrowser
    import subprocess
    import time
    
    allure_results = os.path.join(run_dir, "allure-results")
    if not os.path.exists(allure_results):
        print("Allure 结果目录不存在，跳过打开报告")
        return
    
    print(f"\n正在启动 Allure 服务: {allure_results}")
    
    # 启动 allure serve
    try:
        proc = subprocess.Popen(
            ["allure", "serve", allure_results],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # 等待服务启动
        time.sleep(3)
        
        # 尝试打开浏览器
        webbrowser.open("http://localhost:8080")
        print(f"Allure 服务已启动，浏览器访问: http://localhost:8080")
        print(f"(进程 PID: {proc.pid})")
    except Exception as e:
        print(f"启动 Allure 服务失败: {e}")
        print("请手动运行: allure serve " + allure_results)


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="天津市建筑产业互联网平台 - Web UI 自动化测试运行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python run_tests.py
    python run_tests.py --tester "张三" --remark "冒烟测试"
    python run_tests.py --env staging --headless
    python run_tests.py --screenshot-all
    python run_tests.py --parallel 4
    python run_tests.py --test-url "http://172.16.1.165:3200/"
    python run_tests.py --clean-old --keep-days 7
        """,
    )

    parser.add_argument("--tester", default="", help="测试人员姓名")
    parser.add_argument("--remark", default="", help="测试备注信息")
    parser.add_argument("--screenshot-all", action="store_true", default=False,
                        help="对所有测试截图")
    parser.add_argument("--no-clean", action="store_true", help="不清理旧报告")
    parser.add_argument("--no-open", action="store_true", help="不自动打开报告")
    parser.add_argument("--clean-old", action="store_true", default=False,
                        help="清理超过7天的旧运行目录、截图、日志和BUG清单")
    parser.add_argument("--keep-days", type=int, default=7,
                        help="清理旧文件时保留的天数，默认7天")
    parser.add_argument("--reports-dir", default=None, help="报告目录")
    parser.add_argument("--viewport-width", type=int, default=1920,
                        help="浏览器视口宽度，默认1920")
    parser.add_argument("--viewport-height", type=int, default=1080,
                        help="浏览器视口高度，默认1080")
    parser.add_argument("--test-url", default="", help="测试地址（覆盖环境配置）")
    parser.add_argument("--env", default="dev", choices=["dev", "staging", "prod"],
                        help="测试环境，默认 dev")
    parser.add_argument("--headless", action="store_true", default=False,
                        help="无头模式运行")
    parser.add_argument("--parallel", type=int, default=1,
                        help="并行运行数，默认1（不并行）")

    args = parser.parse_args()

    script_dir = os.path.dirname(__file__)
    reports_dir = args.reports_dir or os.path.join(script_dir, "reports")

    # 每次运行使用独立目录，默认不清空历史报告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"run_{timestamp}"
    run_dir = os.path.join(reports_dir, run_name)

    # 仅清理当前运行目录，不影响历史记录
    clean_reports(reports_dir, run_dir)

    # 可选：清理超过 N 天的旧运行目录、截图、日志、BUG清单
    if args.clean_old:
        clean_all(reports_dir, keep_days=args.keep_days)

    exit_code, actual_run_dir = run_tests(
        tester=args.tester,
        remark=args.remark,
        screenshot_all=args.screenshot_all,
        reports_dir=reports_dir,
        viewport_width=args.viewport_width,
        viewport_height=args.viewport_height,
        test_url=args.test_url,
        env_name=args.env,
        headless=args.headless,
        parallel=args.parallel,
    )

    report_file = generate_html_report(
        tester=args.tester,
        remark=args.remark,
        run_dir=actual_run_dir,
    )

    # 生成 BUG 清单
    bug_file = generate_bug_list(
        run_dir=actual_run_dir,
        tester=args.tester,
        remark=args.remark,
    )

    if not args.no_open and report_file and os.path.exists(report_file):
        open_report(actual_run_dir)

    print("\n" + "=" * 60)
    print("测试完成!")
    if report_file:
        print(f"Allure HTML 报告: {report_file}")
    if bug_file:
        print(f"BUG 清单: {bug_file}")
    print(f"运行目录: {actual_run_dir}")
    print(f"Allure 结果目录: {os.path.join(actual_run_dir, 'allure-results')}")
    print(f"截图目录: {os.environ.get('SCREENSHOT_DIR', os.path.join(reports_dir, 'screenshots', run_name))}")
    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
