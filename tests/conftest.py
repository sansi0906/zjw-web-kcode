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

from config.settings import ENV_CHOICES, settings

sys.stdout.reconfigure(encoding="utf-8")

# ==================== 页面对象导入 ====================

from pages.base_page import BasePage  # noqa: E402
from pages.home_page import HomePage  # noqa: E402
from pages.industry_demand_page import IndustryDemandPage  # noqa: E402
from pages.industry_news_page import IndustryNewsPage  # noqa: E402
from pages.key_project_page import KeyProjectsPage  # noqa: E402
from pages.supply_hall_page import SupplyHallPage  # noqa: E402
from pages.demand_page import DemandPage  # noqa: E402
from pages.intelligent_construction_page import IntelligentConstructionPage  # noqa: E402
from pages.industry_policy_page import IndustryPolicyPage  # noqa: E402
from pages.industry_association_page import IndustryAssociationPage  # noqa: E402
from pages.achievement_transformation_page import AchievementTransformationPage  # noqa: E402
from pages.cloud_service_page import CloudServicePage  # noqa: E402
from pages.industrial_service_page import IndustrialServicePage  # noqa: E402

# Playwright 内置设备字典（用于 --device-name 参数）
with sync_playwright() as _pw:
    PLAYWRIGHT_DEVICES = _pw.devices

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
    """添加自定义命令行参数

    所有可覆盖配置项的默认值均为 None，含义是「不覆盖，沿用 .env / 配置默认值」。
    这样环境变量才能真正生效。
    """
    parser.addoption("--env", action="store", default=None,
                     choices=list(ENV_CHOICES),
                     help=f"测试环境: {' / '.join(ENV_CHOICES)}（默认取 TEST_ENV）")
    parser.addoption("--tester", action="store", default=None,
                     help="测试人员姓名")
    parser.addoption("--remark", action="store", default=None,
                     help="测试备注")
    parser.addoption("--screenshot-all", action="store_true", default=False,
                     help="对所有测试截图（包括通过的测试）")
    parser.addoption("--viewport-width", type=int, default=None,
                     help="浏览器视口宽度（默认取 VIEWPORT_WIDTH）")
    parser.addoption("--viewport-height", type=int, default=None,
                     help="浏览器视口高度（默认取 VIEWPORT_HEIGHT）")
    parser.addoption("--test-url", action="store", default=None,
                     help="测试地址（覆盖环境配置）")
    parser.addoption("--headless", action="store_true", default=None,
                     help="无头模式运行（覆盖 BROWSER_HEADLESS）")
    parser.addoption("--no-headless", action="store_true", default=False,
                     help="有头模式运行（覆盖 BROWSER_HEADLESS）")
    parser.addoption("--platform", action="store", default=None,
                     choices=["web", "h5", "mobile"],
                     help="运行平台: web / h5 / mobile（默认取 PLATFORM）")
    parser.addoption("--device-name", action="store", default=None,
                     help="Playwright 设备名称（如 'iPhone 12', 'iPhone 12 Pro', 'Pixel 5', 'iPad', 'Samsung Galaxy S10'）")
    parser.addoption("--mobile", action="store_true", default=False,
                     help="等价于 --platform h5（快捷参数）")


# ==================== Pytest 配置初始化 ====================


def pytest_configure(config: pytest.Config) -> None:
    """pytest 配置初始化 - 命令行参数按需覆盖配置"""
    env_name = config.getoption("--env")
    if env_name:
        settings.env_name = env_name

    test_url = config.getoption("--test-url")
    if test_url:
        settings.base_url_override = test_url

    if config.getoption("--no-headless"):
        settings.browser_headless = False
    else:
        headless = config.getoption("--headless")
        if headless is not None:
            settings.browser_headless = headless

    platform = config.getoption("--platform")
    if config.getoption("--mobile"):
        platform = "h5"
    if platform:
        settings.platform = platform

    device_name = config.getoption("--device-name")
    if device_name is not None:
        settings.device = device_name

    viewport_width = config.getoption("--viewport-width")
    if viewport_width:
        settings.viewport_width = viewport_width
    viewport_height = config.getoption("--viewport-height")
    if viewport_height:
        settings.viewport_height = viewport_height

    tester = config.getoption("--tester")
    if tester:
        settings.tester = tester
    remark = config.getoption("--remark")
    if remark:
        settings.remark = remark

    # 重试策略由配置驱动（pytest.ini 不再硬编码 --reruns）
    config.option.reruns = settings.reruns
    config.option.reruns_delay = settings.reruns_delay

    # 写入 Allure 环境信息
    env_file = Path(settings.reports_dir) / "allure-results" / "environment.properties"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"环境={settings.env_name}\n")
        f.write(f"测试地址={settings.base_url}\n")
        f.write(f"浏览器={settings.browser_config.browser_type}\n")
        f.write(f"无头模式={settings.browser_config.headless}\n")
        f.write(f"平台={settings.platform}\n")
        if settings.device:
            f.write(f"设备={settings.device}\n")
        f.write(f"视口={settings.viewport_width}x{settings.viewport_height}\n")
        f.write(f"测试人员={settings.tester or '未指定'}\n")
        f.write(f"备注={settings.remark or '无'}\n")


# ==================== 浏览器 Fixtures ====================


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Session 级 Browser - 内核由 BROWSER_TYPE 配置决定"""
    with sync_playwright() as p:
        browser_type = getattr(p, settings.browser_config.browser_type, p.chromium)
        browser = browser_type.launch(
            headless=settings.browser_config.headless,
            slow_mo=settings.browser_config.slow_mo,
        )
        yield browser
        browser.close()


def _new_page(request: pytest.FixtureRequest) -> Page:
    """按配置创建页面（视口 / 设备仿真）"""
    viewport_width = request.config.getoption("--viewport-width") or settings.viewport_width
    viewport_height = request.config.getoption("--viewport-height") or settings.viewport_height
    device_name = request.config.getoption("--device-name") or settings.device
    platform = request.config.getoption("--platform") or settings.platform
    if request.config.getoption("--mobile"):
        platform = "h5"

    # H5/mobile 平台未指定设备时，自动使用默认移动设备进行真正设备仿真
    # （仅设置 viewport 不会触发移动端布局，需 isMobile/hasTouch/UA 等）
    if platform in ("h5", "mobile") and not device_name:
        device_name = "iPhone 12" if "iPhone 12" in PLAYWRIGHT_DEVICES else ""

    browser: Browser = request.getfixturevalue("browser")
    if device_name:
        device = PLAYWRIGHT_DEVICES.get(device_name)
        if device:
            return browser.new_page(**device)

    return browser.new_page(
        viewport={"width": viewport_width, "height": viewport_height}
    )


@pytest.fixture(scope="function")
def page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    """
    Function 级 Page
    测试结束后自动关闭

    注意：此处不做初始导航，页面对象通过 `open()` 自行跳转，
    避免每个用例都多加载一次首页（可节省约 40% 全量耗时）。
    """
    page = _new_page(request)
    yield page
    page.close()


@pytest.fixture(scope="module")
def shared_page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    """
    Module 级共享 Page
    整个测试模块只创建一次页面，适合单页快速遍历场景
    注意：使用此 fixture 的测试用例需要自行维护页面状态（跳转后回首页）
    """
    page = _new_page(request)

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
    ("demand_page", DemandPage, "function", "page"),
    ("industry_demand_page", IndustryDemandPage, "function", "page"),
    ("key_projects_page", KeyProjectsPage, "function", "page"),
    ("industry_news_page", IndustryNewsPage, "function", "page"),
    ("intelligent_construction_page", IntelligentConstructionPage, "function", "page"),
    ("key_project_page", KeyProjectsPage, "function", "page"),
    ("industry_policy_page", IndustryPolicyPage, "function", "page"),
    ("industry_association_page", IndustryAssociationPage, "function", "page"),
    ("achievement_transformation_page", AchievementTransformationPage, "function", "page"),
    ("cloud_service_page", CloudServicePage, "function", "page"),
    ("industrial_service_page", IndustrialServicePage, "function", "page"),
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
            elif screenshot_all:
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

@pytest.fixture
def console_errors(page: Page):
    """收集页面 console error 消息"""
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    yield errors
