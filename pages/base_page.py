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

from config.settings import settings


class BasePage:
    """页面对象基类"""

    def __init__(self, page: Page):
        self.page = page
        screenshot_dir = os.environ.get("SCREENSHOT_DIR", settings.screenshots_dir)
        self.screenshots_dir = Path(screenshot_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    # ==================== 导航与等待 ====================

    def goto(self, url: str = "", timeout: int = None) -> None:
        """跳转到指定URL，默认使用配置中的 base_url"""
        target = url or settings.env_config.base_url
        self.page.goto(target, timeout=timeout or settings.browser_config.timeout)
        self.wait_for_load()

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

    def scroll_to(self, selector: str) -> None:
        """滚动到指定元素"""
        self.page.locator(selector).first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

    # ==================== 通用选择器（子类可覆盖） ====================

    FLOAT_CUSTOMER_SERVICE = "[class*='customer'], [class*='service'], div:has-text('客服')"
    FLOAT_INTENT_FORM = "[class*='intent'], [class*='form'], div:has-text('意向')"
    FOOTER_SERVICE_PHONE = "text=400-, text=电话, [class*='phone']"
    FOOTER_ICP = "text=ICP, text=备案, text=京ICP, text=津ICP"

    # ==================== 通用方法（子类可覆盖） ====================

    def get_nav_texts(self) -> list[str]:
        """获取导航链接文本（默认实现）"""
        navs = self.page.locator("nav a, header a, .nav a")
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

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
        """断言页面包含指定文本"""
        locator = self.page.locator(f"text={text}")
        if partial:
            expect(locator.first).to_be_visible(timeout=10000)
        else:
            expect(locator.first).to_have_text(text, timeout=10000)

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
