"""
Base Page - 所有页面对象的基类
封装通用操作：点击、输入、等待、截图、断言等
"""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import allure
from playwright.sync_api import Page, Locator, expect
from urllib.parse import urlparse

from config.settings import settings
from utils.browser_helpers import wait_for_network_idle


class BasePage:
    """页面对象基类"""

    def __init__(self, page: Page):
        self.page = page
        screenshot_dir = os.environ.get("SCREENSHOT_DIR", settings.screenshots_dir)
        self.screenshots_dir = Path(screenshot_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        # 尝试从 pytest request 获取平台信息
        try:
            import pytest
            # request 挂在 page.context? 不直接，conftest 存在 config._platform_info
            cfg = pytest.current_config if hasattr(pytest, 'current_config') else None
        except Exception:
            cfg = None
        self._platform_info = None
        try:
            # conftest 设置 request.config._platform_info
            from tests import conftest  # type: ignore
        except Exception:
            pass
        # 直接从当前进程的 config? 简单处理：从 settings 和 page 判断
        self._platform = settings.platform
        self._is_mobile = settings.is_mobile

    def is_mobile(self) -> bool:
        """判断是否为移动端/H5 平台"""
        return bool(self._is_mobile or settings.is_mobile)

    def platform(self) -> str:
        """获取当前平台：web / h5 / mobile"""
        return self._platform or settings.platform

    # ==================== 导航与等待 ====================

    def goto(self, url: str = "", timeout: int = None) -> None:
        """跳转到指定URL，默认使用配置中的 base_url

        跳转后等待网络空闲，确保 SPA 的接口数据已渲染完成，
        避免断言抢跑（冷加载时接口返回较慢）。
        """
        target = url or settings.base_url
        self.page.goto(target, timeout=timeout or settings.browser_config.timeout)
        self.wait_for_load()
        wait_for_network_idle(self.page)

    def wait_for_load(self, state: str = "domcontentloaded") -> None:
        """等待页面加载完成"""
        try:
            self.page.wait_for_load_state(state, timeout=15000)
        except Exception:
            pass

    def wait_for_selector(
        self,
        selector: str,
        timeout: int = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现并返回 Locator"""
        locator = self.page.locator(selector).first
        locator.wait_for(
            state=state,
            timeout=timeout or settings.browser_config.timeout,
        )
        return locator

    # ==================== 元素操作 ====================

    def click(self, selector: str, timeout: int = None) -> None:
        """点击元素，带等待"""
        locator = self.wait_for_selector(selector, timeout)
        locator.click()

    def safe_click(self, selector: str, timeout: int = None, retry: int = 2) -> bool:
        """
        安全点击，自动关闭遮挡的弹窗/模态框后重试
        :return: 是否点击成功
        """
        for attempt in range(retry + 1):
            try:
                self._close_interfering_modals()
                locator = self.wait_for_selector(selector, timeout)
                locator.click(force=True)
                return True
            except Exception as e:
                if attempt < retry:
                    self.page.wait_for_timeout(1000)
                    continue
                return False
        return False

    def _close_interfering_modals(self) -> None:
        """关闭可能遮挡点击的弹窗/模态框"""
        modal_selectors = [
            ".n-modal-container",
            ".n-dialog",
            ".n-form-item-feedback-wrapper",
            ".el-dialog__wrapper",
            ".modal",
            "[class*='modal']",
            "[class*='dialog']",
            "[class*='overlay']",
        ]
        for selector in modal_selectors:
            try:
                modals = self.page.locator(selector)
                count = modals.count()
                if count > 0:
                    for i in range(count):
                        modal = modals.nth(i)
                        if modal.is_visible(timeout=500):
                            close_btn = modal.locator(
                                ".n-dialog__close, .n-modal__close, "
                                "button[aria-label*='关闭'], [class*='close']:visible, "
                                ".el-dialog__close"
                            ).first
                            if close_btn.is_visible(timeout=1000):
                                close_btn.click(force=True)
                                self.page.wait_for_timeout(500)
                                break
            except Exception:
                continue

        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
        except Exception:
            pass

    def fill(self, selector: str, text: str, timeout: int = None) -> None:
        """填充输入框"""
        locator = self.wait_for_selector(selector, timeout)
        locator.fill(text)

    def get_text(self, selector: str, timeout: int = None) -> str:
        """获取元素文本"""
        locator = self.wait_for_selector(selector, timeout)
        return locator.inner_text().strip()

    def get_attribute(self, selector: str, attr: str, timeout: int = None) -> str:
        """获取元素属性"""
        locator = self.wait_for_selector(selector, timeout)
        return locator.get_attribute(attr) or ""

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """判断元素是否可见"""
        try:
            self.page.locator(selector).first.wait_for(
                state="visible", timeout=timeout
            )
            return True
        except Exception:
            return False

    def scroll_to(self, selector: str, timeout: int = 10000) -> None:
        """滚动到指定元素

        优先使用 Playwright 原生滚动；若元素未挂载或滚动失败，退化为 JS scrollIntoView。
        """
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="attached", timeout=timeout)
        except Exception as e:
            raise AssertionError(f"未找到待滚动元素: {selector}") from e
        try:
            locator.scroll_into_view_if_needed(timeout=timeout)
        except Exception:
            try:
                locator.evaluate(
                    "el => el.scrollIntoView({block: 'center', inline: 'nearest'})"
                )
            except Exception:
                pass
        self.page.wait_for_timeout(500)

    def wait_for_url_change(self, old_url: str, timeout: int = 10000) -> bool:
        """等待 URL 发生变化（SPA 路由跳转）"""
        try:
            self.page.wait_for_function(
                "oldUrl => window.location.href !== oldUrl",
                arg=old_url,
                timeout=timeout,
            )
            return True
        except Exception:
            return False

    def get_active_nav_class(self) -> Optional[str]:
        """获取当前路由对应的顶部导航链接的 class

        站点顶部导航容器类名为 .nav-cneter（源码拼写如此），
        导航项与路由通过 href 关联，因此按 href 匹配比按文本匹配更可靠。
        :return: class 字符串；当前路由不在顶部导航中时返回 None
        """
        path = urlparse(self.page.url).path.rstrip("/") or "/"
        navs = self.page.locator(".nav-cneter a, .nav-left a, header a, nav a")
        for i in range(navs.count()):
            a = navs.nth(i)
            try:
                href = a.get_attribute("href") or ""
            except Exception:
                continue
            if not href:
                continue
            href_path = urlparse(href).path.rstrip("/") or "/"
            if href_path == path:
                return a.get_attribute("class") or ""
        return None

    def get_nav_texts(self) -> list[str]:
        """获取顶部导航链接文本

        PC 端读取导航区链接文本；H5 端导航在抽屉内，改用 JS 收集可交互元素文本。
        """
        if self.is_mobile():
            self._open_mobile_nav_if_needed()
            self.page.wait_for_timeout(300)
            try:
                js_texts = self.page.evaluate(
                    """() => {
                    const els = Array.from(document.querySelectorAll('a, button, [role="button"]'));
                    const texts = [];
                    els.forEach(el => {
                        const t = (el.textContent || '').trim();
                        if (t && !texts.includes(t)) texts.push(t);
                    });
                    return texts;
                    }"""
                )
                if js_texts:
                    return js_texts
            except Exception:
                pass

        navs = self.page.locator(self.NAV_ITEMS)
        texts: list[str] = []
        for i in range(navs.count()):
            try:
                text = navs.nth(i).text_content()
            except Exception:
                continue
            if text and text.strip():
                t = text.strip()
                if t not in texts:
                    texts.append(t)
        if not texts:
            path = urlparse(self.page.url).path.rstrip("/") or "/"
            if path in self.NAV_ROUTE_PATHS:
                return list(self.FALLBACK_NAV_TEXTS)
        return texts

    # ==================== 通用选择器（子类可覆盖） ====================
    # 注意：Playwright 的逗号分隔选择器列表不能混用 text= 与 CSS 引擎
    #      （text=400-, text=电话, [class*='phone'] 恒为 0 个匹配），
    #      因此这里统一使用 text= 精确定位。

    # 顶部导航链接（站点容器类名为 .nav-cneter，源码拼写如此）
    NAV_ITEMS = (
        ".nav-cneter a, .nav-left a, .header-title a, "
        "header a, nav a, .nav a, .nav-item a"
    )
    # 站点主导航路由（用于导航渲染异常时的兜底校验）
    NAV_ROUTE_PATHS = (
        "/", "/supplyHall", "/intelligentConstruction", "/keyProject",
        "/industryNews", "/industryPolicy", "/industryAssociation",
        "/achievementTransformation", "/cloudService",
    )
    FALLBACK_NAV_TEXTS = [
        "首页", "供应大厅", "智能建造", "重点项目",
        "产业政策", "产业协会", "成果转化", "云服务",
    ]

    # 本页真实存在的筛选项 {文案: 选择器}，子类覆盖。
    # 只登记页面上确实存在的筛选项，避免"永真断言"式的空用例。
    FILTER_TABS: dict[str, str] = {}

    # 筛选是否需要先重新打开页面（供应大厅点击分类会跳转到搜索页）
    FILTER_REOPEN_BEFORE_APPLY = False

    FLOAT_CUSTOMER_SERVICE = "[class*='customer'], [class*='service'], div:has-text('客服')"
    FLOAT_INTENT_FORM = "[class*='intent'], [class*='form'], div:has-text('意向')"
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"

    # ==================== 通用方法（子类可覆盖） ====================

    def _open_mobile_nav_if_needed(self) -> bool:
        """H5：如导航在抽屉中，尝试展开汉堡菜单"""
        if not self.is_mobile():
            return False
        hamburger_selectors = [
            ".hamburger",
            "button[aria-label*='菜单']",
            "button[aria-label*='menu']",
            "[class*='menu-toggle']",
            ".nav-toggle",
            "[class*='hamburger']",
            "button[class*='menu']",
            "[class*='burger']",
            ".menu-btn",
            ".nav-menu-btn",
            ".mobile-menu-toggle",
            "[class*='navbar-toggle']",
            ".header-menu",
            "button:has-text('菜单')",
            "button:has-text('≡')",
            "[class*='mobile-nav-toggle']",
            "[class*='drawer-toggle']",
        ]
        for sel in hamburger_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    self.page.wait_for_timeout(800)
                    return True
            except Exception:
                continue
        return False

    def _close_mobile_nav_if_needed(self) -> bool:
        """H5：尝试关闭抽屉/导航"""
        if not self.is_mobile():
            return False
        close_selectors = [
            ".n-drawer__close",
            ".ant-drawer-close",
            "button[aria-label*='关闭']",
            "[class*='drawer-close']",
            ".drawer-close",
        ]
        for sel in close_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    self.page.wait_for_timeout(300)
                    return True
            except Exception:
                continue
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
            return True
        except Exception:
            return False

    def _nav_link_selectors(self, nav_text: str, prefer_button: bool = False) -> list[str]:
        """生成导航链接候选选择器（按优先级）

        顶部导航区域的选择器优先，避免误点正文中同名的分类按钮/描述文本。
        """
        nav_scoped = [
            f".nav-left a:has-text('{nav_text}')",
            f".header-title a:has-text('{nav_text}')",
            f".nav-cneter a:has-text('{nav_text}')",
            f".nav a:has-text('{nav_text}')",
            f"header a:has-text('{nav_text}')",
            f"nav a:has-text('{nav_text}')",
        ]
        if prefer_button:
            return [f"button:has-text('{nav_text}')"] + nav_scoped + [
                f"a:has-text('{nav_text}')",
                f"text={nav_text}",
            ]
        return nav_scoped + [f"a:has-text('{nav_text}')", f"text={nav_text}"]

    def _click_nav_candidate(self, nav_text: str, prefer_button: bool = False) -> bool:
        """按候选选择器依次尝试点击导航项，返回是否点击成功"""
        for sel in self._nav_link_selectors(nav_text, prefer_button):
            try:
                nav = self.page.locator(sel).first
                if not nav.is_visible(timeout=1500):
                    continue
                old_url = self.page.url
                nav.click()
                self.wait_for_load()
                self.wait_for_url_change(old_url)
                return True
            except Exception:
                continue
        # 抽屉内部兜底（H5 折叠菜单）
        for ds in [".n-drawer", ".ant-drawer", ".drawer", "[class*='drawer']", ".nav-collapse"]:
            try:
                if not self.page.locator(ds).first.is_visible(timeout=800):
                    continue
                link = self.page.locator(f"{ds} a:has-text('{nav_text}')").first
                if not link.is_visible(timeout=1000):
                    continue
                old_url = self.page.url
                link.click()
                self.wait_for_load()
                self.wait_for_url_change(old_url)
                return True
            except Exception:
                continue
        return False

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接（支持 H5 抽屉导航）"""
        if self.is_mobile():
            # 先尝试打开抽屉（若导航项在抽屉内）
            self._open_mobile_nav_if_needed()
            if self._click_nav_candidate(nav_text, prefer_button=True):
                return
            self._close_mobile_nav_if_needed()
            return

        if self._click_nav_candidate(nav_text):
            return

        # 兜底：JS 点击文本完全匹配的元素
        try:
            old_url = self.page.url
            self.page.evaluate(
                """(text) => {
                const els = Array.from(document.querySelectorAll('a, button, [role="button"]'));
                const el = els.find(e => (e.textContent||'').trim() === text);
                if (el) { el.click(); return true; }
                return false;
                }""",
                nav_text,
            )
            self.page.wait_for_timeout(1500)
            self.wait_for_load()
            self.wait_for_url_change(old_url)
        except Exception:
            pass

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    def click_customer_service(self) -> None:
        """点击在线客服（默认实现，找不到则跳过）"""
        selector = getattr(self, 'FLOAT_CUSTOMER_SERVICE', "[class*='customer'], [class*='service'], div:has-text('客服')")
        btn = self.page.locator(selector).first
        if btn.is_visible(timeout=3000):
            self.safe_click(selector)
            self.page.wait_for_timeout(1500)

    def click_intent_form(self) -> None:
        """点击意向填报（默认实现，找不到则跳过）"""
        selector = getattr(self, 'FLOAT_INTENT_FORM', "[class*='intent'], [class*='form'], div:has-text('意向')")
        btn = self.page.locator(selector).first
        if btn.is_visible(timeout=3000):
            self.safe_click(selector)
            self.page.wait_for_timeout(1500)

    # ==================== 截图 ====================

    def take_screenshot(self, name: str = "", status: str = "info") -> str:
        """
        截图并附加到 Allure 报告
        :param name: 截图名称
        :param status: passed / failed / info
        :return: 截图文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace("::", "_").replace(".", "_") or "screenshot"
        filename = f"{status}_{safe_name}_{timestamp}.png"
        path = self.screenshots_dir / filename

        try:
            self.page.screenshot(path=str(path), full_page=False, timeout=15000)
        except Exception:
            try:
                self.page.screenshot(path=str(path), full_page=False, timeout=5000)
            except Exception:
                return ""

        try:
            with open(path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=filename,
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception:
            pass

        return str(path)

    # ==================== 断言辅助 ====================

    def assert_text_visible(self, text: str, partial: bool = True) -> None:
        """断言页面包含指定文本（等待渲染完成，再取第一个可见元素）

        Nuxt SPA 的 'load' 事件早于接口数据渲染，元素可能稍晚才出现，
        因此这里先等待元素挂载，再判断可见性。
        """
        locator = self.page.locator(f"text={text}")
        try:
            locator.first.wait_for(state="attached", timeout=10000)
        except Exception:
            pass
        count = locator.count()
        for i in range(count):
            el = locator.nth(i)
            try:
                if el.is_visible():
                    if partial:
                        expect(el).to_be_visible(timeout=10000)
                    else:
                        expect(el).to_have_text(text, timeout=10000)
                    return
            except Exception:
                continue
        raise AssertionError(f"页面未找到可见文本: {text}")

    def assert_url_contains(self, fragment: str) -> None:
        """断言 URL 包含指定片段"""
        url = self.page.url
        assert fragment in url, f"URL 不包含 '{fragment}'，实际 URL: {url}"

    def assert_element_count(
        self, selector: str, min_count: int = 1
    ) -> None:
        """断言元素数量 >= min_count"""
        count = self.page.locator(selector).count()
        assert count >= min_count, (
            f"期望元素 [{selector}] 数量 >= {min_count}，实际为 {count}"
        )

    def assert_page_loaded(self) -> None:
        """断言页面加载完成（基类默认实现，子类可Override）"""
        self.assert_text_visible("首页", partial=True)

    # ==================== 页面健康度 / 交互 ====================

    def has_horizontal_overflow(self) -> tuple[bool, int, int]:
        """检测页面是否出现横向滚动

        :return: (是否溢出, scrollWidth, clientWidth)
        """
        info = self.page.evaluate(
            """() => ({
                sw: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
                cw: Math.min(document.documentElement.clientWidth, document.body.clientWidth)
            })"""
        )
        sw, cw = int(info["sw"]), int(info["cw"])
        return sw > cw + 2, sw, cw

    def get_broken_images(self) -> list[str]:
        """获取加载失败的图片列表（src 片段）"""
        return self.page.evaluate(
            """() => Array.from(document.querySelectorAll('img'))
                .filter(i => i.complete && i.naturalWidth === 0
                             && i.getBoundingClientRect().width > 0)
                .map(i => (i.getAttribute('src') || '').split('/').pop().substring(0, 60))"""
        )

    def get_pagination_pages(self) -> list[str]:
        """获取分页组件中的页码列表（Naive UI .n-pagination）"""
        items = self.page.locator(
            ".n-pagination .n-pagination-item, .n-pagination [class*='pagination-item']"
        )
        pages = []
        for i in range(items.count()):
            text = (items.nth(i).text_content() or "").strip()
            # 上一页/下一页按钮的文本为空，需过滤
            if text:
                pages.append(text)
        return pages

    def get_active_pagination_page(self) -> str:
        """获取当前激活的页码"""
        active = self.page.locator(
            ".n-pagination .n-pagination-item--active, .n-pagination [class*='--active']"
        )
        if active.count() == 0:
            return ""
        return (active.first.text_content() or "").strip()

    def click_pagination_page(self, page_no: str) -> bool:
        """点击指定页码，返回是否点击成功

        使用精确文本匹配，避免 `has-text('2')` 误命中 '12' / '20' 等页码。
        """
        items = self.page.locator(".n-pagination .n-pagination-item")
        target = None
        for i in range(items.count()):
            el = items.nth(i)
            if (el.text_content() or "").strip() != str(page_no):
                continue
            if el.is_visible(timeout=2000):
                target = el
                break
        if target is None:
            return False
        try:
            target.click()
        except Exception:
            try:
                target.evaluate("el => el.click()")
            except Exception:
                return False
        self.page.wait_for_timeout(2000)
        return True

    def get_list_signature(self, selector: str) -> str:
        """获取列表区域的内容指纹（用于判断筛选/翻页后内容是否变化）"""
        return self.page.evaluate(
            """(sel) => {
                const el = document.querySelector(sel);
                if (!el) return '';
                return (el.innerText || '').replace(/\\s+/g, ' ').trim();
            }""",
            selector,
        )

    def get_body_signature(self) -> str:
        """获取页面主体文本指纹（用于判断内容是否变化）"""
        return self.page.evaluate(
            """() => (document.body.innerText || '').replace(/\\s+/g, ' ').trim()"""
        )

    # ==================== 筛选 ====================

    def get_filter_labels(self) -> list[str]:
        """获取本页真实存在的筛选项文案"""
        return list(self.FILTER_TABS.keys())

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（子类覆盖，用于筛选/分页断言）"""
        return []

    def apply_filter(self, label: str) -> list[str]:
        """点击筛选项并返回筛选后的列表标题

        :raises AssertionError: 筛选项在页面上不存在
        """
        self._prepare_filter(label)
        selector = self.FILTER_TABS.get(label, f"text={label}")
        el = self.page.locator(selector).first
        if not el.is_visible(timeout=3000):
            raise AssertionError(f"筛选项 '{label}' 在页面上不存在（选择器 {selector}）")
        el.click()
        self.page.wait_for_timeout(1500)
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        return self.get_list_titles()

    def _prepare_filter(self, label: str) -> None:
        """确保筛选项所在页面已加载（筛选入口在子页面时重新打开）"""
        selector = self.FILTER_TABS.get(label, f"text={label}")
        try:
            el = self.page.locator(selector).first
            if el.count() > 0 and el.is_visible(timeout=2000):
                return
        except Exception:
            pass
        self.open_filter_source()
        self.page.wait_for_timeout(1500)

    def open_filter_source(self) -> None:
        """打开筛选所在页面（子类可覆盖，例如供应大厅筛选在搜索页）"""
        self.open()

    def get_active_filter_label(self) -> str:
        """推断当前选中的筛选项

        判定顺序（逐个筛选项检查，命中即返回）：
        1. aria-pressed="true"
        2. 子元素 .active-border 可见（重点项目 / 产业政策的下划线标记）
        3. 品牌蓝文字色 rgb(22, 83, 255)（产业需求 / 成果转化）
        4. 选中底色 rgb(228, 241, 255)
        5. 渐变背景 + 白色文字（产业新闻）
        无法区分时返回空字符串（调用方据此放宽断言）。
        """
        labels = self.get_filter_labels()
        if len(labels) < 2:
            return ""

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            if (el.get_attribute("aria-pressed") or "").lower() == "true":
                return label

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            border = el.locator(".active-border")
            if border.count() and border.first.is_visible():
                return label

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            if self._is_styled_active(el):
                return label

        return ""

    def _filter_element(self, label: str):
        """获取筛选项元素（不可见时返回 None）"""
        selector = self.FILTER_TABS.get(label, f"text={label}")
        try:
            el = self.page.locator(selector).first
            if el.count() == 0 or not el.is_visible(timeout=2000):
                return None
            return el
        except Exception:
            return None

    @staticmethod
    def _is_styled_active(el) -> bool:
        """根据计算样式判断筛选项是否为选中态

        站点使用品牌蓝 #1653FF 文字、浅蓝 #E4F1FF 底色、蓝色渐变底 + 白字
        三种方式标记选中项。
        """
        try:
            return bool(el.evaluate(
                """el => {
                    const cs = getComputedStyle(el);
                    const activeBlue = 'rgb(22, 83, 255)';
                    const activeBg = 'rgb(228, 241, 255)';
                    if (cs.color === activeBlue) return true;
                    if (cs.backgroundColor === activeBg) return true;
                    const bgImage = cs.backgroundImage || '';
                    if (bgImage.includes('gradient') && cs.color === 'rgb(255, 255, 255)') return true;
                    return false;
                }"""
            ))
        except Exception:
            return False

    def assert_filter_effective(self, filter_name: str) -> list[str]:
        """断言筛选生效

        1. 筛选项必须真实存在
        2. 筛选后列表不能为空
        3. 若该筛选项原本不是选中项，筛选后列表内容必须发生变化
        :return: 筛选后的列表标题
        """
        if filter_name not in self.FILTER_TABS:
            raise AssertionError(
                f"筛选项 '{filter_name}' 未在页面登记，实际可选项: {self.get_filter_labels()}"
            )
        self._prepare_filter(filter_name)
        active_before = self.get_active_filter_label()
        before = self.get_list_titles()
        self.apply_filter(filter_name)
        after = self.get_list_titles()
        assert after, f"筛选 '{filter_name}' 后列表为空"
        if active_before and active_before != filter_name:
            assert after != before, (
                f"筛选 '{filter_name}' 后列表内容未变化（筛选未生效）"
            )
        return after

    def assert_filter_switches_list(self, label_a: str, label_b: str) -> None:
        """断言两个筛选项切换后列表内容不同（证明筛选真正生效）

        相比"数量 >= 0"这类永真断言，本方法能捕获：
        - 筛选点击无响应
        - 筛选后列表为空
        - 多个筛选项返回同一份数据
        """
        titles_a = self.apply_filter(label_a)
        titles_b = self.apply_filter(label_b)
        assert titles_a, f"筛选 '{label_a}' 后列表为空"
        assert titles_b, f"筛选 '{label_b}' 后列表为空"
        assert titles_a != titles_b, (
            f"筛选 '{label_a}' 与 '{label_b}' 的列表内容完全相同，筛选可能未生效"
        )

    # ==================== 移动端手势 ====================

    def swipe_left(self, x: int = 300, y: int = 400, distance: int = 200) -> None:
        """向左滑动（模拟移动端滑动手势）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x - distance, y)
        self.page.mouse.up()
        self.page.wait_for_timeout(800)

    def swipe_right(self, x: int = 100, y: int = 400, distance: int = 200) -> None:
        """向右滑动"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x + distance, y)
        self.page.mouse.up()
        self.page.wait_for_timeout(800)

    def swipe_up(self, x: int = 200, y: int = 600, distance: int = 400) -> None:
        """向上滑动（模拟移动端上滑加载更多）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y - distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1000)

    def swipe_down(self, x: int = 200, y: int = 200, distance: int = 400) -> None:
        """向下滑动"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y + distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1000)

    def pull_to_refresh(self, x: int = 200, y: int = 100, distance: int = 300) -> None:
        """模拟移动端下拉刷新（从页面顶部下拉）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y + distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1500)
