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


from pages.mixins.assertion_mixin import AssertionMixin
from pages.mixins.filter_mixin import FilterMixin
from pages.mixins.navigation_mixin import NavigationMixin
from pages.mixins.pagination_mixin import PaginationMixin
from pages.mixins.swipe_mixin import SwipeMixin


class BasePage(AssertionMixin, NavigationMixin, FilterMixin, PaginationMixin, SwipeMixin):
    """页面对象基类"""

    def __init__(self, page: Page):
        self.page = page
        screenshot_dir = os.environ.get("SCREENSHOT_DIR", settings.screenshots_dir)
        self.screenshots_dir = Path(screenshot_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._platform_info = None
        self._platform = settings.platform
        self._is_mobile = self._detect_mobile(page)

    @staticmethod
    def _detect_mobile(page: Page) -> bool:
        """优先按实际页面/上下文能力判断移动端，避免并行或夹具场景下 settings 串台"""
        try:
            vp = page.viewport_size or {}
            width = int(vp.get("width") or 0)
            if width and width <= 900:
                return True
        except Exception:
            pass
        try:
            ua = ""
            ctx = getattr(page, "context", None)
            browser = getattr(ctx, "browser", None) if ctx else None
            ua = getattr(browser, "user_agent", "") or ""
            if not ua and ctx and hasattr(ctx, "_impl_obj"):
                ua = getattr(getattr(ctx, "_impl_obj", None), "_options", {}).get("userAgent", "") or ""
            # 设备上下文常见 UA 关键词兜底
            ua_l = ua.lower()
            if any(k in ua_l for k in ("mobile", "iphone", "android", "ipad")):
                return True
        except Exception:
            pass
        return bool(settings.is_mobile)

    def is_mobile(self) -> bool:
        """判断是否为移动端/H5 平台"""
        return bool(self._is_mobile)

    def platform(self) -> str:
        """获取当前平台：web / h5 / mobile"""
        if self._is_mobile and self._platform in ("web", "", None):
            return "h5"
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
                    try:
                        self.page.wait_for_load_state("domcontentloaded", timeout=1500)
                    except Exception:
                        pass
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
                                try:
                                    self.page.wait_for_load_state("domcontentloaded", timeout=1500)
                                except Exception:
                                    pass
                                break
            except Exception:
                continue

        try:
            self.page.keyboard.press("Escape")
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=1500)
            except Exception:
                pass
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

    def first_visible(self, selector: str, timeout: int = 500):
        """返回第一个可见匹配元素；无可见元素时返回 None"""
        loc = self.page.locator(selector)
        for i in range(min(loc.count(), 20)):
            el = loc.nth(i)
            try:
                if el.is_visible(timeout=timeout):
                    return el
            except Exception:
                continue
        return None

    def visible_locator(self, selector: str, timeout: int = 500):
        """返回可见元素优先的定位器（兼容 Web/H5 隐藏重复节点）"""
        el = self.first_visible(selector, timeout=timeout)
        return el if el is not None else self.page.locator(selector).first

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
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=1500)
        except Exception:
            pass

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

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=3000)
        except Exception:
            pass

    def click_customer_service(self) -> None:
        """点击在线客服（默认实现，找不到则跳过）"""
        selector = getattr(self, 'FLOAT_CUSTOMER_SERVICE', "[class*='customer'], [class*='service'], div:has-text('客服')")
        btn = self.page.locator(selector).first
        if btn.is_visible(timeout=3000):
            self.safe_click(selector)
            try:
                self.page.wait_for_load_state("networkidle", timeout=3000)
            except Exception:
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=1500)
                except Exception:
                    pass

    def click_intent_form(self) -> None:
        """点击意向填报（默认实现，找不到则跳过）"""
        selector = getattr(self, 'FLOAT_INTENT_FORM', "[class*='intent'], [class*='form'], div:has-text('意向')")
        btn = self.page.locator(selector).first
        if btn.is_visible(timeout=3000):
            self.safe_click(selector)
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=2000)
                except Exception:
                    pass

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

    def _broken_image_allowlist(self) -> list[str]:
        """破损图片白名单（子串匹配 src，配置驱动，默认空）"""
        try:
            import yaml
            from pathlib import Path
            from utils.ui_quality import DEFAULT_UI_QUALITY, _deep_merge
            data_file = Path(__file__).resolve().parent.parent / "data" / "test_data.yaml"
            root = {}
            if data_file.exists():
                with open(data_file, "r", encoding="utf-8") as f:
                    root = (yaml.safe_load(f) or {}).get("ui_quality") or {}
            cfg = _deep_merge(DEFAULT_UI_QUALITY, root.get("default"))
            items = (cfg.get("broken_images") or {}).get("allow_src_substrings") or []
            return [str(s) for s in items if str(s).strip()]
        except Exception:
            return []

    def assert_no_broken_images(self) -> None:
        """断言页面无加载失败的图片（白名单内的已知破损图跳过）"""
        broken = self.get_broken_images()
        allow = self._broken_image_allowlist()
        unknown = [b for b in broken if not any(a in b for a in allow)]
        assert not unknown, f"发现加载失败的图片: {unknown}"

    # ==================== 页面状态 ====================

    def is_not_found_page(self) -> bool:
        """检测当前页是否为 404/未找到页面（Nuxt/通用兜底）"""
        try:
            title = (self.page.title() or "").lower()
            body = ""
            try:
                body = (self.page.locator("body").inner_text(timeout=1500) or "").lower()
            except Exception:
                try:
                    body = (self.page.content() or "").lower()
                except Exception:
                    body = ""
            url = (self.page.url or "").lower()
            markers = [
                "404 - page not found",
                "page not found",
                "404 not found",
                "页面不存在",
                "未找到页面",
            ]
            if any(m in title for m in markers):
                return True
            if "404" in body and ("not found" in body or "page not found" in body):
                return True
            if "/404" in url:
                return True
        except Exception:
            return False
        return False


