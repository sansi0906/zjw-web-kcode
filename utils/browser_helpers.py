"""
浏览器辅助函数
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page, Locator

if TYPE_CHECKING:
    from pages.base_page import BasePage


def click_and_wait_for_new_page(
    page: Page, locator: Locator, timeout: int = 30000
) -> Page:
    """
    点击元素并等待新页面（新标签页或当前页面跳转）
    :param page: Playwright page 对象
    :param locator: 要点击的元素定位器
    :param timeout: 超时时间（毫秒）
    :return: 跳转后的页面对象（可能是原页面或新标签页）
    """
    with page.expect_popup(timeout=timeout) as popup_info:
        locator.click()

    try:
        new_page = popup_info.value
        new_page.wait_for_load_state("networkidle", timeout=timeout)
        return new_page
    except Exception:
        # 如果没有新标签页打开，可能是当前页面跳转
        page.wait_for_load_state("networkidle", timeout=timeout)
        return page


def safe_click(page: Page, selector: str, timeout: int = None) -> bool:
    """
    安全点击，处理元素不可见等异常
    :return: 是否点击成功
    """
    try:
        locator = page.locator(selector).first
        if locator.is_visible(timeout=timeout or 5000):
            locator.click()
            return True
    except Exception:
        pass
    return False


def wait_for_network_idle(page: Page, timeout: int = 15000) -> None:
    """等待网络空闲"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except Exception:
        pass
