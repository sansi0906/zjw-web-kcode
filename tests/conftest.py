"""
全局 Fixtures 和 Hooks

提供：
- 配置加载
- 页面对象 Fixtures（POM）
- 浏览器 Fixtures
- 截图 Hooks
- 测试数据
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import allure
import pytest
import yaml
from playwright.sync_api import Browser, Page, sync_playwright

from config.settings import settings
from utils.browser_helpers import wait_for_network_idle

sys.stdout.reconfigure(encoding="utf-8")

# ==================== 页面对象导入 ====================

from pages.base_page import BasePage  # noqa: E402
from pages.home_page import HomePage  # noqa: E402
from pages.industry_demand_page import IndustryDemandPage  # noqa: E402
from pages.industry_news_page import IndustryNewsPage  # noqa: E402
from pages.key_project_page import KeyProjectsPage  # noqa: E402
from pages.supply_hall_page import SupplyHallPage  # noqa: E402
from pages.all_products_page import AllProductsPage  # noqa: E402
from pages.intelligent_construction_page import IntelligentConstructionPage  # noqa: E402
from pages.industry_policy_page import IndustryPolicyPage  # noqa: E402
from pages.industry_association_page import IndustryAssociationPage  # noqa: E402
from pages.achievement_transformation_page import AchievementTransformationPage  # noqa: E402
from pages.cloud_service_page import CloudServicePage  # noqa: E402
from pages.supply_chain_map_page import SupplyChainMapPage  # noqa: E402
from pages.industrial_service_page import IndustrialServicePage  # noqa: E402

# ==================== 测试数据加载 ====================


def load_test_data() -> dict:
    """加载 YAML 测试数据"""
    data_file = Path(__file__).parent.parent / "data" / "test_data.yaml"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


TEST_DATA = load_test_data()

# ==================== 目录初始化 ====================


def init_directories() -> None:
    """初始化报告、截图、日志目录"""
    for dir_path in [
        settings.reports_dir,
        settings.screenshots_dir,
        settings.logs_dir,
    ]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


init_directories()

# ==================== Pytest 命令行参数 ====================


def pytest_addoption(parser: pytest.Parser) -> None:
    """添加自定义命令行参数"""
    parser.addoption("--env", action="store", default="dev",
                     choices=["dev", "staging", "prod"],
                     help="测试环境: dev / staging / prod")
    parser.addoption("--tester", action="store", default="",
                     help="测试人员姓名")
    parser.addoption("--remark", action="store", default="",
                     help="测试备注")
    parser.addoption("--screenshot-all", action="store_true", default=False,
                     help="对所有测试截图（包括通过的测试）")
    parser.addoption("--viewport-width", type=int, default=1920,
                     help="浏览器视口宽度")
    parser.addoption("--viewport-height", type=int, default=1080,
                     help="浏览器视口高度")
    parser.addoption("--test-url", action="store", default="",
                     help="测试地址（覆盖环境配置）")
    parser.addoption("--headless", action="store_true", default=False,
                     help="无头模式运行")


# ==================== Pytest 配置初始化 ====================


def pytest_configure(config: pytest.Config) -> None:
    """pytest 配置初始化"""
    env_name = config.getoption("--env")
    test_url = config.getoption("--test-url")
    headless = config.getoption("--headless")

    # 更新全局配置
    settings.env_name = env_name
    settings.browser_headless = headless
    settings.base_url = test_url or settings.env_config.base_url
    settings.tester = config.getoption("--tester") or "未指定"
    settings.remark = config.getoption("--remark") or "无"

    # 写入 Allure 环境信息
    env_file = Path(settings.reports_dir) / "allure-results" / "environment.properties"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"环境={settings.env_name}\n")
        f.write(f"测试地址={settings.base_url}\n")
        f.write(f"浏览器={settings.browser_config.browser_type}\n")
        f.write(f"无头模式={settings.browser_headless}\n")
        f.write(f"视口={settings.viewport_width}x{settings.viewport_height}\n")
        f.write(f"测试人员={settings.tester}\n")
        f.write(f"备注={settings.remark}\n")


# ==================== 浏览器 Fixtures ====================


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Session 级 Browser"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=settings.browser_config.headless,
            slow_mo=settings.browser_config.slow_mo,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    """
    Function 级 Page
    自动打开测试地址，测试结束后自动关闭
    """
    viewport_width = request.config.getoption("--viewport-width")
    viewport_height = request.config.getoption("--viewport-height")

    page = browser.new_page(
        viewport={"width": viewport_width, "height": viewport_height}
    )
    page.goto(settings.base_url, timeout=settings.browser_config.timeout)
    wait_for_network_idle(page)

    yield page
    page.close()


@pytest.fixture(scope="module")
def shared_page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    """
    Module 级共享 Page
    整个测试模块只创建一次页面，适合单页快速遍历场景
    注意：使用此 fixture 的测试用例需要自行维护页面状态（跳转后回首页）
    """
    viewport_width = request.config.getoption("--viewport-width")
    viewport_height = request.config.getoption("--viewport-height")

    page = browser.new_page(
        viewport={"width": viewport_width, "height": viewport_height}
    )
    page.goto(settings.base_url, timeout=settings.browser_config.timeout)
    wait_for_network_idle(page)

    # 关闭首次加载弹窗
    try:
        dialog = page.locator(".construction-application-dialog").first
        if dialog.is_visible(timeout=3000):
            close_btn = dialog.locator(
                ".n-dialog__close, .n-modal__close, "
                "button[aria-label*='关闭'], [class*='close']:visible"
            ).first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
            else:
                page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
    except Exception:
        pass

    yield page
    page.close()


# ==================== 页面对象 Fixtures ====================

# 使用工厂函数减少重复代码
# 格式: (fixture_name, page_class, scope, depends_on)
# depends_on: 依赖的 page fixture 名称，默认 "page"
_PAGE_FIXTURES = [
    ("home_page", HomePage, "function", "page"),
    ("home_page_shared", HomePage, "module", "shared_page"),
    ("supply_hall_page", SupplyHallPage, "function", "page"),
    ("industry_demand_page", IndustryDemandPage, "function", "page"),
    ("key_projects_page", KeyProjectsPage, "function", "page"),
    ("industry_news_page", IndustryNewsPage, "function", "page"),
    ("all_products_page", AllProductsPage, "function", "page"),
    ("intelligent_construction_page", IntelligentConstructionPage, "function", "page"),
    ("key_project_page", KeyProjectsPage, "function", "page"),
    ("industry_policy_page", IndustryPolicyPage, "function", "page"),
    ("industry_association_page", IndustryAssociationPage, "function", "page"),
    ("achievement_transformation_page", AchievementTransformationPage, "function", "page"),
    ("cloud_service_page", CloudServicePage, "function", "page"),
    ("industrial_service_page", IndustrialServicePage, "function", "page"),
    ("supply_chain_map_page", SupplyChainMapPage, "function", "page"),
]


def _create_page_fixture(name: str, page_class, scope: str, depends_on: str = "page"):
    """创建页面对象 fixture 的工厂函数"""
    @pytest.fixture(scope=scope)
    def _fixture(request: pytest.FixtureRequest):
        page_obj = request.getfixturevalue(depends_on)
        return page_class(page_obj)
    _fixture.__name__ = name
    _fixture.__qualname__ = name
    return _fixture


# 动态注册页面 fixtures
for fixture_name, page_class, scope, depends_on in _PAGE_FIXTURES:
    globals()[fixture_name] = _create_page_fixture(fixture_name, page_class, scope, depends_on)


# ==================== 截图 Hooks ====================


def _take_screenshot(page: Page, item: pytest.Item, status: str) -> str:
    """截图并附加到 Allure"""
    try:
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace("::", "_").replace(".", "_")
        prefix = "通过" if status == "passed" else "失败"
        filename = f"{prefix}_{test_name}_{timestamp}.png"

        screenshot_dir = os.environ.get("SCREENSHOT_DIR", settings.screenshots_dir)
        path = Path(screenshot_dir) / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        # 优先截取最新标签页
        target_page = page.context.pages[-1] if len(page.context.pages) > 1 else page
        target_page.screenshot(path=str(path), full_page=True)

        with open(path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"{prefix}截图",
                attachment_type=allure.attachment_type.PNG,
            )
        return str(path)
    except Exception as e:
        print(f"截图失败: {e}")
        return ""


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """测试执行后生成报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page_obj = getattr(item, "page", None)
        if page_obj:
            screenshot_all = item.config.getoption("--screenshot-all", default=False)
            if report.failed and settings.screenshot_on_failure:
                _take_screenshot(page_obj, item, "failed")
            elif screenshot_all or settings.screenshot_on_pass:
                _take_screenshot(page_obj, item, "passed")

        # 附加执行时长
        duration = call.duration if hasattr(call, "duration") else 0
        allure.attach(
            f"{duration:.2f}秒",
            name="执行时长",
            attachment_type=allure.attachment_type.TEXT,
        )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    """测试开始前记录模块信息"""
    module_name = item.module.__name__ if hasattr(item, "module") else "未知模块"
    feature = module_name.replace("test_", "").replace("_", " ")
    allure.dynamic.feature(feature.title())

    if hasattr(item, "function") and item.function.__doc__:
        allure.dynamic.description(item.function.__doc__)


# ==================== 测试用例执行顺序 ====================

TEST_ORDER = [
    "test_homepage_full.py",      # 单页快速模式，必须第一个执行
    "test_key_projects.py",
    "test_industry_news.py",
    "test_industry_demand.py",
    "test_achievement_transformation.py",
    "test_cloud_service.py",
    "test_all_products.py",
    "test_supply_hall.py",
]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """自定义测试用例执行顺序"""
    def get_order(item: pytest.Item) -> int:
        filename = os.path.basename(item.location[0])
        if filename in TEST_ORDER:
            return TEST_ORDER.index(filename)
        return len(TEST_ORDER)

    items.sort(key=get_order)


# ==================== 测试结束汇总 ====================


def pytest_terminal_summary(
    terminalreporter: object,
    exitstatus: int,
    config: pytest.Config,
) -> None:
    """测试结束汇总"""
    print("\n" + "=" * 60)
    print(f"Allure 结果目录: {settings.reports_dir}/allure-results")
    print(f"截图目录: {settings.screenshots_dir}")
    print(f"日志目录: {settings.logs_dir}")
    print("=" * 60)