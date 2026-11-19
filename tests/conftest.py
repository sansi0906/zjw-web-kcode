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

# 统一 UTF-8 输出，减少 Windows 终端乱码
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import allure
import pytest
import yaml
from playwright.sync_api import Browser, Page, sync_playwright

from config.settings import ENV_CHOICES, settings

# ==================== 页面对象导入 ====================

from pages.base_page import BasePage  # noqa: E402
from pages.home_page import HomePage  # noqa: E402
from pages.industry_news_page import IndustryNewsPage  # noqa: E402
from pages.key_project_page import KeyProjectsPage  # noqa: E402
from pages.supply_hall_page import SupplyHallPage  # noqa: E402
from pages.supply_hall_search_result_page import SupplyHallSearchResultPage  # noqa: E402
from pages.demand_page import DemandPage  # noqa: E402
from pages.exhibition_page import ExhibitionPage  # noqa: E402
from pages.intelligent_construction_page import IntelligentConstructionPage  # noqa: E402
from pages.industry_association_page import IndustryAssociationPage  # noqa: E402
from pages.achievement_transformation_page import AchievementTransformationPage  # noqa: E402
from pages.cloud_service_page import CloudServicePage  # noqa: E402
from pages.industrial_service_page import IndustrialServicePage  # noqa: E402
from pages.finance_page import FinancePage  # noqa: E402

# Playwright 内置设备字典（用于 --device-name 参数）
with sync_playwright() as _pw:
    PLAYWRIGHT_DEVICES = _pw.devices

# ==================== 测试数据加载 ====================


REQUIRED_TOP_LEVEL_KEYS = {
    "environments",
    "page_titles",
    "font_tests",
    "navigation",
    "filter_tabs",
    "search_keywords",
    "page_assertions",
}
ALLOWED_STYLE_KEYS = {"fontFamily", "fontSize", "fontWeight", "color", "lineHeight", "letterSpacing"}
KNOWN_PAGE_FIXTURES = {
    "home_page",
    "supply_hall_page",
    "demand_page",
    "key_project_page",
    "key_projects_page",
    "industry_news_page",
    "intelligent_construction_page",
    "industry_association_page",
    "achievement_transformation_page",
    "cloud_service_page",
    "industrial_service_page",
    "supply_hall_search_result_page",
    "h5_supply_hall_search_result_page",
    "exhibition_page",
    "finance_page",
}


def _validate_test_data(data: dict) -> None:
    """校验 test_data.yaml 关键结构；对已存在顶层 key 做严格校验，缺失不阻断加载以兼容旧数据。"""
    if not isinstance(data, dict):
        raise ValueError("test_data.yaml 根节点必须是字典")
    if "font_tests" in data:
        if not isinstance(data["font_tests"], dict):
            raise ValueError("test_data.yaml.font_tests 必须是字典")
        for page_name, modules in data["font_tests"].items():
            if not isinstance(modules, dict):
                raise ValueError(f"test_data.yaml.font_tests.{page_name} 必须是字典")
            for mod_name, cfg in modules.items():
                for field in ("texts", "selector", "style_keys"):
                    if field not in cfg:
                        raise ValueError(
                            f"test_data.yaml.font_tests.{page_name}.{mod_name} 缺少必填字段: {field}"
                        )
                if not isinstance(cfg["texts"], list) or len(cfg["texts"]) < 1:
                    raise ValueError(
                        f"test_data.yaml.font_tests.{page_name}.{mod_name}.texts 必须是非空列表"
                    )
                if not isinstance(cfg["style_keys"], list) or len(cfg["style_keys"]) < 1:
                    raise ValueError(
                        f"test_data.yaml.font_tests.{page_name}.{mod_name}.style_keys 必须是非空列表"
                    )
                selector = cfg["selector"]
                if not isinstance(selector, str) or not selector:
                    raise ValueError(
                        f"test_data.yaml.font_tests.{page_name}.{mod_name}.selector 必须是非空字符串"
                    )
                if "{text}" not in selector and any("{text}" in t for t in cfg["texts"] if isinstance(t, str)):
                    raise ValueError(
                        f"test_data.yaml.font_tests.{page_name}.{mod_name}.selector 缺少 {{text}} 占位符"
                    )
                bad_keys = [k for k in cfg["style_keys"] if k not in ALLOWED_STYLE_KEYS]
                if bad_keys:
                    raise ValueError(
                        f"test_data.yaml.font_tests.{page_name}.{mod_name}.style_keys 包含不支持的键: {bad_keys}；允许: {sorted(ALLOWED_STYLE_KEYS)}"
                    )
                for opt in ("min_visible",):
                    if opt in cfg and (not isinstance(cfg[opt], int) or cfg[opt] < 1):
                        raise ValueError(f"test_data.yaml.font_tests.{page_name}.{mod_name}.{opt} 必须是 >=1 的整数")
                for opt in ("scroll_into_view", "optional"):
                    if opt in cfg and not isinstance(cfg[opt], bool):
                        raise ValueError(f"test_data.yaml.font_tests.{page_name}.{mod_name}.{opt} 必须是布尔值")
    for key in ("filter_switch_pairs", "pagination_pages"):
        if key in data:
            if not isinstance(data[key], list):
                raise ValueError(f"test_data.yaml.{key} 必须是列表")
            for i, item in enumerate(data[key]):
                if not isinstance(item, dict):
                    raise ValueError(f"test_data.yaml.{key}[{i}] 必须是字典")
                fx = item.get("fixture")
                if fx and fx not in KNOWN_PAGE_FIXTURES:
                    raise ValueError(f"test_data.yaml.{key}[{i}].fixture 引用了未知 fixture: {fx}")
                if key == "filter_switch_pairs":
                    for req in ("page", "fixture", "a", "b"):
                        if req not in item:
                            raise ValueError(f"test_data.yaml.{key}[{i}] 缺少字段: {req}")
                if key == "pagination_pages":
                    for req in ("page", "fixture"):
                        if req not in item:
                            raise ValueError(f"test_data.yaml.{key}[{i}] 缺少字段: {req}")
    nav = data.get("navigation")
    if nav is not None and not isinstance(nav, dict):
        raise ValueError("test_data.yaml.navigation 必须是字典")
    if isinstance(nav, dict):
        home_nav = (nav.get("home_page") or {}).get("nav_links")
        if home_nav is not None:
            if not isinstance(home_nav, list):
                raise ValueError("test_data.yaml.navigation.home_page.nav_links 必须是列表")
            for i, link in enumerate(home_nav):
                for req in ("text", "url_fragment"):
                    if not isinstance(link, dict) or req not in link:
                        raise ValueError(f"test_data.yaml.navigation.home_page.nav_links[{i}] 缺少字段: {req}")
    if "search_keywords" in data and not isinstance(data["search_keywords"], dict):
        raise ValueError("test_data.yaml.search_keywords 必须是字典")


def load_test_data() -> dict:
    """加载 YAML 测试数据"""
    data_file = Path(__file__).parent.parent / "data" / "test_data.yaml"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        _validate_test_data(data)
        return data
    return {}


TEST_DATA = load_test_data()


@pytest.fixture(scope="session")
def test_data() -> dict:
    """统一的 YAML 测试数据 fixture，供数据驱动测试注入。"""
    return TEST_DATA


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
    parser.addoption("--visual", action="store_true", default=False,
                     help="启用视觉回归对比（默认关闭，需先生成基线）")
    parser.addoption("--visual-baseline", action="store", default="reports/visual/baseline",
                     help="视觉回归基线目录")
    parser.addoption("--visual-threshold", type=float, default=0.01,
                     help="视觉差异容忍比例（0~1，默认 1%%）")


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

    # xdist 并行安全：默认策略为“隔离子集可并行”。共享 module-scope 页面与有状态用例必须显式标记 serial，
    # 使用 -n 时请排除：`pytest -n auto -m "not serial"`；或仅对 function-scope/无状态用例子集并行。
    if getattr(config.option, "numprocesses", None) not in (None, 0, 1):
        if not config.option.markexpr:
            print(
                "\n[警告] 检测到 pytest-xdist 并行执行且未指定 -m。"
                "存在 serial 共享页面/有状态用例，建议使用: pytest -n auto -m \"not serial\"\n"
            )

    # 写入 Allure 环境信息（便于报告可观测性）
    env_file = Path(settings.reports_dir) / "allure-results" / "environment.properties"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    numproc = getattr(config.option, "numprocesses", None)
    marker_expr = getattr(config.option, "markexpr", "") or ""
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
        f.write(f"xdist_workers={numproc if numproc is not None else 'off'}\n")
        f.write(f"marker_expr={marker_expr or '(none)'}\n")


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


@pytest.fixture(scope="function")
def h5_page(browser: Browser) -> Page:
    """Function 级 H5 Page（强制移动端设备仿真，用于 @pytest.mark.h5 用例）"""
    device_name = "iPhone 12" if "iPhone 12" in PLAYWRIGHT_DEVICES else ""
    if device_name:
        device = PLAYWRIGHT_DEVICES.get(device_name)
        if device:
            page = browser.new_page(**device)
        else:
            page = browser.new_page(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
    else:
        page = browser.new_page(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
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
            try:
                dialog.wait_for(state="hidden", timeout=3000)
            except Exception:
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=2000)
                except Exception:
                    pass
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
    ("h5_home_page", HomePage, "function", "h5_page"),
    ("home_page_shared", HomePage, "module", "shared_page"),
    ("supply_hall_page", SupplyHallPage, "function", "page"),
    ("supply_hall_search_result_page", SupplyHallSearchResultPage, "function", "page"),
    ("h5_supply_hall_search_result_page", SupplyHallSearchResultPage, "function", "h5_page"),
    ("demand_page", DemandPage, "function", "page"),
    ("exhibition_page", ExhibitionPage, "function", "page"),
    ("key_projects_page", KeyProjectsPage, "function", "page"),
    ("industry_news_page", IndustryNewsPage, "function", "page"),
    ("intelligent_construction_page", IntelligentConstructionPage, "function", "page"),
    ("key_project_page", KeyProjectsPage, "function", "page"),
    ("industry_association_page", IndustryAssociationPage, "function", "page"),
    ("achievement_transformation_page", AchievementTransformationPage, "function", "page"),
    ("cloud_service_page", CloudServicePage, "function", "page"),
    ("industrial_service_page", IndustrialServicePage, "function", "page"),
    ("finance_page", FinancePage, "function", "page"),
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
        if not page_obj:
            try:
                page_obj = item.funcargs.get("page") or item.funcargs.get("shared_page")
            except Exception:
                page_obj = None
        if page_obj:
            screenshot_all = item.config.getoption("--screenshot-all", default=False)
            if report.failed and settings.screenshot_on_failure:
                _take_screenshot(page_obj, item, "failed")
                try:
                    allure.attach(
                        str(getattr(page_obj, "url", "")),
                        name="失败时URL",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                except Exception:
                    pass
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

_H5_PAGE_FIXTURES = [
    ("h5_supply_hall_page", SupplyHallPage, "h5_page"),
    ("h5_key_project_page", KeyProjectsPage, "h5_page"),
    ("h5_industry_news_page", IndustryNewsPage, "h5_page"),
    ("h5_demand_page", DemandPage, "h5_page"),
    ("h5_exhibition_page", ExhibitionPage, "h5_page"),
    ("h5_achievement_transformation_page", AchievementTransformationPage, "h5_page"),
    ("h5_industry_association_page", IndustryAssociationPage, "h5_page"),
    ("h5_cloud_service_page", CloudServicePage, "h5_page"),
    ("h5_intelligent_construction_page", IntelligentConstructionPage, "h5_page"),
    ("h5_industrial_service_page", IndustrialServicePage, "h5_page"),
    ("h5_finance_page", FinancePage, "h5_page"),
]


def _make_h5_page_fixture(name: str, cls: type, page_fixture: str):
    @pytest.fixture(scope="function")
    def _fixture(request):
        po = cls(request.getfixturevalue(page_fixture))
        po.open()
        return po
    _fixture.__name__ = name
    return _fixture


for _name, _cls, _page in _H5_PAGE_FIXTURES:
    globals()[_name] = _make_h5_page_fixture(_name, _cls, _page)
    KNOWN_PAGE_FIXTURES.add(_name)


TEST_ORDER = [
    "test_homepage_full.py",      # 单页快速模式，必须第一个执行
    "test_key_projects.py",
    "test_industry_news.py",
    "test_achievement_transformation.py",
    "test_cloud_service.py",
    "test_supply_hall.py",
]


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """自定义测试用例执行顺序，并移除不适用的通用用例"""
    selected: list[pytest.Item] = []
    for item in items:
        if (
            item.name == "test_nav_active_state"
            and getattr(getattr(item, "cls", None), "NAV_ACTIVE_STATE_APPLICABLE", True) is False
        ):
            continue
        selected.append(item)
    items[:] = selected

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
