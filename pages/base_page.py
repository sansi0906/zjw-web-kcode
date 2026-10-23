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



    def assert_no_broken_images(self) -> None:
        """断言页面无加载失败的图片"""
        broken = self.get_broken_images()
        assert not broken, f"发现加载失败的图片: {broken}"
