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

from config.settings import ENV_CHOICES, settings


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
    viewport_width: int | None = None,
    viewport_height: int | None = None,
    test_url: str = "",
    env_name: str | None = None,
    headless: bool | None = None,
    headed: bool = False,
    parallel: int | None = None,
    run_dir: str = "",
    platform: str | None = None,
    device_name: str = "",
    mobile: bool = False,
) -> tuple[int, str]:
    """运行测试，返回 (exit_code, run_dir)"""
    if mobile:
        platform = "h5"

    viewport_width = viewport_width or settings.viewport_width
    viewport_height = viewport_height or settings.viewport_height
    parallel = parallel if parallel is not None else settings.parallel_workers
    reports_dir = reports_dir or settings.reports_dir

    if platform in ("h5", "mobile"):
        viewport_width = 375
        viewport_height = 812
        # H5/mobile 未指定设备时，自动使用默认移动设备进行真正设备仿真
        if not device_name:
            device_name = "iPhone 12"

    print("\n" + "=" * 60)
    print("开始运行测试...")
    print(f"环境: {env_name or settings.env_name}")
    print(f"测试地址: {test_url or settings.base_url}")
    if device_name:
        print(f"设备: {device_name} (platform={platform or settings.platform})")
    else:
        print(f"视口: {viewport_width}x{viewport_height}")
    print(f"无头模式: {settings.browser_config.headless}")
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

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--alluredir", os.path.join(run_dir, "allure-results"),
        "--viewport-width", str(viewport_width),
        "--viewport-height", str(viewport_height),
    ]

    if env_name:
        cmd.extend(["--env", env_name])
    if tester:
        cmd.extend(["--tester", tester])
    if remark:
        cmd.extend(["--remark", remark])
    if screenshot_all:
        cmd.append("--screenshot-all")
    if test_url:
        cmd.extend(["--test-url", test_url])
    if headed:
        cmd.append("--no-headless")
    elif headless:
        cmd.append("--headless")
    if parallel > 1:
        cmd.extend(["-n", str(parallel)])
    if platform:
        cmd.extend(["--platform", platform])
    if device_name:
        cmd.extend(["--device-name", device_name])
    if mobile:
        cmd.append("--mobile")

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
        print(f"Allure HTML 报告已生成: {output_file}")

    # 合并 generate_report.py 的自定义 HTML 渲染（全局统计 / 用例明细 / 失败截图 / 分类筛选）
    try:
        generator = TestReportGenerator(run_dir)
        generator.screenshots_dir = os.environ.get(
            "SCREENSHOT_DIR", os.path.join(os.path.dirname(run_dir), "screenshots", os.path.basename(run_dir))
        )
        generator.parse_allure_results()
        custom_output = generator.generate_html_report(
            tester=tester, remark=remark,
            output_file=os.path.join(run_dir, "custom_report.html"),
        )
        if custom_output:
            print(f"自定义 HTML 报告已生成: {custom_output}")
    except Exception as e:
        print(f"自定义 HTML 报告生成失败: {e}")

    return output_file if os.path.exists(output_file) else ""


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


def open_report(run_dir: str) -> None:
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


"""
测试报告生成器
生成包含全局统计、用例明细、失败截图、分类筛选的自定义 HTML 报告
"""
import os
import json
import base64
import datetime
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional


class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, reports_dir: str = None):
        self.reports_dir = reports_dir or os.path.join(os.path.dirname(__file__), "reports")
        self.screenshots_dir = os.path.join(self.reports_dir, "screenshots")
        self.allure_results_dir = os.path.join(self.reports_dir, "allure-results")
        self.html_output_dir = os.path.join(self.reports_dir, "html")
        
        # 确保输出目录存在
        os.makedirs(self.html_output_dir, exist_ok=True)
        
        # 测试结果数据
        self.test_results: List[Dict[str, Any]] = []
        self.summary: Dict[str, Any] = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "error": 0,
            "duration": 0.0,
            "pass_rate": 0.0
        }
        
        # 测试环境信息
        self.environment: Dict[str, str] = {}
        
    def parse_allure_results(self) -> None:
        """解析 Allure 结果文件"""
        if not os.path.exists(self.allure_results_dir):
            print(f"Allure 结果目录不存在: {self.allure_results_dir}")
            return
            
        # 解析环境信息
        env_file = os.path.join(self.allure_results_dir, "environment.properties")
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        self.environment[key] = value
        
        # 解析测试结果 JSON 文件
        for filename in os.listdir(self.allure_results_dir):
            if filename.endswith("-result.json"):
                filepath = os.path.join(self.allure_results_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        result = json.load(f)
                        self._process_test_result(result)
                except Exception as e:
                    print(f"解析文件失败 {filename}: {e}")
    
    def _process_test_result(self, result: Dict[str, Any]) -> None:
        """处理单个测试结果"""
        test_info = {
            "uuid": result.get("uuid", ""),
            "name": result.get("name", "未知测试"),
            "status": result.get("status", "unknown"),
            "stage": result.get("stage", ""),
            "start": result.get("start", 0),
            "stop": result.get("stop", 0),
            "duration": 0.0,
            "feature": "",
            "description": "",
            "error_message": "",
            "error_trace": "",
            "screenshot": "",
            "screenshot_base64": ""
        }
        
        # 计算执行时长
        if test_info["start"] and test_info["stop"]:
            test_info["duration"] = (test_info["stop"] - test_info["start"]) / 1000.0
        
        # 获取功能模块
        labels = result.get("labels", [])
        for label in labels:
            if label.get("name") == "feature":
                test_info["feature"] = label.get("value", "")
        
        # 获取描述
        test_info["description"] = result.get("description", "")
        
        # 获取错误信息
        status_details = result.get("statusDetails", {})
        if status_details:
            test_info["error_message"] = status_details.get("message", "")
            test_info["error_trace"] = status_details.get("trace", "")
        
        # 查找截图
        attachments = result.get("attachments", [])
        for attachment in attachments:
            attachment_name = attachment.get("name", "")
            # 支持失败截图和通过截图
            if "截图" in attachment_name or "screenshot" in attachment_name.lower():
                screenshot_name = attachment.get("source", "")
                if screenshot_name:
                    screenshot_path = os.path.join(self.allure_results_dir, screenshot_name)
                    if os.path.exists(screenshot_path):
                        test_info["screenshot"] = screenshot_path
                        test_info["screenshot_name"] = attachment_name
                        # 读取并转换为 base64
                        with open(screenshot_path, "rb") as f:
                            test_info["screenshot_base64"] = base64.b64encode(f.read()).decode("utf-8")
                        break  # 只取第一个截图
        
        # 如果 Allure 附件中没有截图，尝试从截图目录查找
        if not test_info["screenshot_base64"]:
            screenshot_base64 = self.find_screenshot_for_test(test_info["name"])
            if screenshot_base64:
                test_info["screenshot_base64"] = screenshot_base64
                test_info["screenshot_name"] = "测试截图"
        
        self.test_results.append(test_info)
        
        # 更新统计
        self.summary["total"] += 1
        self.summary["duration"] += test_info["duration"]
        
        status = test_info["status"]
        if status == "passed":
            self.summary["passed"] += 1
        elif status == "failed":
            self.summary["failed"] += 1
        elif status == "skipped":
            self.summary["skipped"] += 1
        elif status == "broken":
            self.summary["error"] += 1
        
        # 计算通过率
        if self.summary["total"] > 0:
            self.summary["pass_rate"] = (self.summary["passed"] / self.summary["total"]) * 100
    
    def find_screenshot_for_test(self, test_name: str) -> Optional[str]:
        """为测试查找截图文件（支持在子文件夹中查找）"""
        if not os.path.exists(self.screenshots_dir):
            return None
            
        # 首先尝试在子文件夹中查找（以报告名称命名的文件夹）
        for folder_name in os.listdir(self.screenshots_dir):
            folder_path = os.path.join(self.screenshots_dir, folder_name)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    if test_name.replace("::", "_").replace(".", "_") in filename:
                        filepath = os.path.join(folder_path, filename)
                        with open(filepath, "rb") as f:
                            return base64.b64encode(f.read()).decode("utf-8")
        
        # 如果子文件夹中没有找到，尝试在根目录查找
        for filename in os.listdir(self.screenshots_dir):
            filepath = os.path.join(self.screenshots_dir, filename)
            if os.path.isfile(filepath) and test_name.replace("::", "_").replace(".", "_") in filename:
                with open(filepath, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
        
        return None
    
    def generate_html_report(self, output_file: str = None, 
                            tester: str = "", remark: str = "") -> str:
        """生成 HTML 报告"""
        if not output_file:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.html_output_dir, f"test_report_{timestamp}.html")
        
        # 更新环境信息
        if tester:
            self.environment["测试人员"] = tester
        if remark:
            self.environment["备注"] = remark
        
        html_content = self._generate_html_content()
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"HTML 报告已生成: {output_file}")
        return output_file
    
    def _generate_html_content(self) -> str:
        """生成 HTML 内容"""
        # 生成测试结果表格行
        test_rows = self._generate_test_rows()
        
        # 生成模块筛选选项
        module_options = self._generate_module_options()
        
        # 生成环境信息
        env_info = self._generate_env_info()
        
        # 生成统计卡片
        stats_cards = self._generate_stats_cards()
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - 天津市建筑产业互联网平台</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #1a1a2e;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 14px;
        }}
        .stat-card.total .number {{ color: #3b82f6; }}
        .stat-card.passed .number {{ color: #10b981; }}
        .stat-card.failed .number {{ color: #ef4444; }}
        .stat-card.skipped .number {{ color: #f59e0b; }}
        .stat-card.error .number {{ color: #8b5cf6; }}
        .stat-card.rate .number {{ color: #06b6d4; }}
        .stat-card.duration .number {{ color: #ec4899; }}
        
        .env-section {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .env-section h2 {{
            color: #1a1a2e;
            font-size: 18px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}
        .env-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        .env-item {{
            display: flex;
            align-items: center;
            padding: 12px 15px;
            background: #f8fafc;
            border-radius: 8px;
        }}
        .env-item .key {{
            color: #64748b;
            min-width: 80px;
            font-size: 14px;
        }}
        .env-item .value {{
            color: #1e293b;
            font-weight: 500;
        }}
        
        .filter-section {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .filter-section label {{
            color: #374151;
            font-weight: 500;
        }}
        .filter-section select, .filter-section input {{
            padding: 10px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }}
        .filter-section select:focus, .filter-section input:focus {{
            border-color: #3b82f6;
        }}
        .filter-btn {{
            padding: 10px 20px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s;
        }}
        .filter-btn:hover {{
            background: #2563eb;
        }}
        .reset-btn {{
            padding: 10px 20px;
            background: #6b7280;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s;
        }}
        .reset-btn:hover {{
            background: #4b5563;
        }}
        
        .results-section {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .results-section h2 {{
            color: #1a1a2e;
            font-size: 18px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}
        .results-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .results-table th {{
            background: #f8fafc;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #374151;
            border-bottom: 2px solid #e5e7eb;
        }}
        .results-table td {{
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
            vertical-align: top;
        }}
        .results-table tr:hover {{
            background: #f8fafc;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status-passed {{ background: #d1fae5; color: #065f46; }}
        .status-failed {{ background: #fee2e2; color: #991b1b; }}
        .status-skipped {{ background: #fef3c7; color: #92400e; }}
        .status-broken {{ background: #ede9fe; color: #5b21b6; }}
        .status-unknown {{ background: #e5e7eb; color: #374151; }}
        
        .error-details {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
            color: #991b1b;
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 200px;
            overflow-y: auto;
        }}
        .screenshot-container {{
            margin-top: 10px;
        }}
        .screenshot-container img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.3s;
        }}
        .screenshot-container img:hover {{
            transform: scale(1.02);
        }}
        .screenshot-toggle {{
            background: #3b82f6;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            margin-bottom: 10px;
        }}
        .screenshot-toggle:hover {{
            background: #2563eb;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}
        .modal.active {{
            display: flex;
        }}
        .modal img {{
            max-width: 95%;
            max-height: 95%;
            border-radius: 8px;
        }}
        .modal-close {{
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            cursor: pointer;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: rgba(255,255,255,0.8);
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .results-table {{
                font-size: 12px;
            }}
            .results-table th, .results-table td {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>测试报告</h1>
            <div class="subtitle">天津市建筑产业互联网平台 - 自动化测试报告</div>
            <div class="subtitle" style="margin-top: 10px;">生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
        
        <div class="stats-grid">
            {stats_cards}
        </div>
        
        <div class="env-section">
            <h2>测试环境</h2>
            <div class="env-grid">
                {env_info}
            </div>
        </div>
        
        <div class="filter-section">
            <label>模块筛选:</label>
            <select id="moduleFilter">
                <option value="">全部模块</option>
                {module_options}
            </select>
            
            <label>状态筛选:</label>
            <select id="statusFilter">
                <option value="">全部状态</option>
                <option value="passed">通过</option>
                <option value="failed">失败</option>
                <option value="skipped">跳过</option>
                <option value="broken">错误</option>
            </select>
            
            <label>搜索:</label>
            <input type="text" id="searchInput" placeholder="输入用例名称搜索...">
            
            <button class="filter-btn" onclick="applyFilter()">筛选</button>
            <button class="reset-btn" onclick="resetFilter()">重置</button>
        </div>
        
        <div class="results-section">
            <h2>用例明细</h2>
            <table class="results-table" id="resultsTable">
                <thead>
                    <tr>
                        <th style="width: 5%">#</th>
                        <th style="width: 15%">模块</th>
                        <th style="width: 30%">用例名称</th>
                        <th style="width: 10%">状态</th>
                        <th style="width: 10%">执行时长</th>
                        <th style="width: 30%">详情</th>
                    </tr>
                </thead>
                <tbody>
                    {test_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>测试报告由 Playwright + Pytest 自动生成</p>
        </div>
    </div>
    
    <div class="modal" id="imageModal" onclick="closeModal()">
        <span class="modal-close">&times;</span>
        <img id="modalImage" src="" alt="截图预览">
    </div>
    
    <script>
        function applyFilter() {{
            const moduleFilter = document.getElementById('moduleFilter').value;
            const statusFilter = document.getElementById('statusFilter').value;
            const searchText = document.getElementById('searchInput').value.toLowerCase();
            
            const rows = document.querySelectorAll('#resultsTable tbody tr');
            
            rows.forEach(row => {{
                const module = row.getAttribute('data-module') || '';
                const status = row.getAttribute('data-status') || '';
                const name = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
                
                let show = true;
                
                if (moduleFilter && module !== moduleFilter) show = false;
                if (statusFilter && status !== statusFilter) show = false;
                if (searchText && !name.includes(searchText)) show = false;
                
                row.style.display = show ? '' : 'none';
            }});
        }}
        
        function resetFilter() {{
            document.getElementById('moduleFilter').value = '';
            document.getElementById('statusFilter').value = '';
            document.getElementById('searchInput').value = '';
            
            const rows = document.querySelectorAll('#resultsTable tbody tr');
            rows.forEach(row => row.style.display = '');
        }}
        
        function toggleScreenshot(btn) {{
            const container = btn.nextElementSibling;
            if (container.style.display === 'none') {{
                container.style.display = 'block';
                btn.textContent = '隐藏截图';
            }} else {{
                container.style.display = 'none';
                btn.textContent = '查看截图';
            }}
        }}
        
        function openModal(imgSrc) {{
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            modalImg.src = imgSrc;
            modal.classList.add('active');
        }}
        
        function closeModal() {{
            document.getElementById('imageModal').classList.remove('active');
        }}
    </script>
</body>
</html>'''
    
    def _generate_stats_cards(self) -> str:
        """生成统计卡片"""
        return f'''
        <div class="stat-card total">
            <div class="number">{self.summary["total"]}</div>
            <div class="label">用例总数</div>
        </div>
        <div class="stat-card passed">
            <div class="number">{self.summary["passed"]}</div>
            <div class="label">通过</div>
        </div>
        <div class="stat-card failed">
            <div class="number">{self.summary["failed"]}</div>
            <div class="label">失败</div>
        </div>
        <div class="stat-card skipped">
            <div class="number">{self.summary["skipped"]}</div>
            <div class="label">跳过</div>
        </div>
        <div class="stat-card error">
            <div class="number">{self.summary["error"]}</div>
            <div class="label">错误</div>
        </div>
        <div class="stat-card rate">
            <div class="number">{self.summary["pass_rate"]:.1f}%</div>
            <div class="label">通过率</div>
        </div>
        <div class="stat-card duration">
            <div class="number">{self.summary["duration"]:.2f}s</div>
            <div class="label">总耗时</div>
        </div>'''
    
    def _generate_env_info(self) -> str:
        """生成环境信息"""
        default_env = {
            "测试环境": "生产环境",
            "测试地址": "https://www.tjjzcy.com/",
            "浏览器": "Chromium",
            "测试人员": "未指定",
            "备注": "无"
        }
        
        # 合并默认值和实际值
        env = {**default_env, **self.environment}
        
        items = []
        for key, value in env.items():
            items.append(f'''
            <div class="env-item">
                <span class="key">{key}:</span>
                <span class="value">{value}</span>
            </div>''')
        
        return "\n".join(items)
    
    def _generate_module_options(self) -> str:
        """生成模块筛选选项"""
        modules = set()
        for result in self.test_results:
            if result["feature"]:
                modules.add(result["feature"])
        
        options = []
        for module in sorted(modules):
            options.append(f'<option value="{module}">{module}</option>')
        
        return "\n".join(options)
    
    def _generate_test_rows(self) -> str:
        """生成测试结果表格行"""
        rows = []
        for i, result in enumerate(self.test_results, 1):
            status_class = f"status-{result['status']}"
            status_text = {
                "passed": "通过",
                "failed": "失败",
                "skipped": "跳过",
                "broken": "错误",
                "unknown": "未知"
            }.get(result["status"], result["status"])
            
            # 生成详情内容
            details = ""
            
            # 添加错误信息
            if result["error_message"]:
                details += f'''
                <div class="error-details">
                    <strong>错误信息:</strong>
                    {result["error_message"]}
                    
                    <strong style="margin-top: 10px; display: block;">堆栈跟踪:</strong>
                    {result["error_trace"]}
                </div>'''
            
            # 添加截图
            if result["screenshot_base64"]:
                details += f'''
                <div class="screenshot-container">
                    <button class="screenshot-toggle" onclick="toggleScreenshot(this)">查看截图</button>
                    <div style="display: none;">
                        <img src="data:image/png;base64,{result["screenshot_base64"]}" 
                             alt="失败截图" 
                             onclick="openModal(this.src)">
                    </div>
                </div>'''
            
            row = f'''
            <tr data-module="{result["feature"]}" data-status="{result["status"]}">
                <td>{i}</td>
                <td>{result["feature"]}</td>
                <td>{result["name"]}</td>
                <td><span class="status-badge {status_class}">{status_text}</span></td>
                <td>{result["duration"]:.2f}s</td>
                <td>{details}</td>
            </tr>'''
            
            rows.append(row)
        
        return "\n".join(rows)


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
    parser.add_argument("--reports-dir", default=None,
                        help="报告目录（默认取 REPORTS_DIR）")
    parser.add_argument("--viewport-width", type=int, default=None,
                        help="浏览器视口宽度（默认取 VIEWPORT_WIDTH）")
    parser.add_argument("--viewport-height", type=int, default=None,
                        help="浏览器视口高度（默认取 VIEWPORT_HEIGHT）")
    parser.add_argument("--test-url", default="", help="测试地址（覆盖环境配置）")
    parser.add_argument("--env", default=None, choices=list(ENV_CHOICES),
                        help="测试环境，默认取 TEST_ENV")
    parser.add_argument("--headless", action="store_true", default=None,
                        help="强制无头模式（覆盖 BROWSER_HEADLESS）")
    parser.add_argument("--no-headless", action="store_true", default=False,
                        help="强制有头模式（覆盖 BROWSER_HEADLESS）")
    parser.add_argument("--platform", default=None, choices=["web", "h5", "mobile"],
                        help="运行平台: web / h5 / mobile（默认取 PLATFORM）")
    parser.add_argument("--device-name", default="",
                        help="Playwright 设备名称（如 'iPhone 12', 'iPhone 12 Pro', 'Pixel 5'）")
    parser.add_argument("--mobile", action="store_true", help="等价于 --platform h5（快捷参数）")
    parser.add_argument("--parallel", type=int, default=None,
                        help="并行运行数（默认取 PARALLEL_WORKERS），1=不并行")

    args = parser.parse_args()

    reports_dir = args.reports_dir or settings.reports_dir

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
        headed=args.no_headless,
        parallel=args.parallel,
        platform=args.platform,
        device_name=args.device_name,
        mobile=args.mobile,
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
