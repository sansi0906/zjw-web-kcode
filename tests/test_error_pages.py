"""404 / 异常路由测试

站点为 Nuxt SPA：未匹配路由返回 404 页面（Page not found + Go back home）。
404 属于“路由未上线/路径错误”，页面对象应能识别并按前提跳过，而不是误报元素缺陷。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage

pytestmark = [pytest.mark.regression]

MISSING_PATH = "/__not_exist_xyz__"


def _assert_404(page: Page) -> None:
    body = (page.locator("body").inner_text(timeout=8000) or "")
    assert "404" in body or "Page not found" in body, f"未识别到 404 页面: {body[:120]!r}"
    assert "Go back home" in body, f"404 页面缺少返回首页入口: {body[:120]!r}"


@allure.feature("异常路由")
class TestErrorPages:

    @allure.story("404")
    @allure.title("Web 未匹配路由显示 404 并可返回首页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_web_not_found_page(self, page: Page) -> None:
        page.goto(settings.base_url.rstrip("/") + MISSING_PATH, wait_until="domcontentloaded", timeout=25000)
        _assert_404(page)
        back = page.locator("a:has-text('Go back home'), a:has-text('返回首页')").first
        if back.count() > 0 and back.is_visible(timeout=2000):
            back.click()
            try:
                page.wait_for_url(lambda u: MISSING_PATH not in u, timeout=8000)
            except Exception:
                pass
            assert MISSING_PATH not in page.url, f"点击返回首页后仍停留在 404: {page.url}"

    @allure.story("404")
    @allure.title("页面对象可识别 404 路由")
    @allure.severity(allure.severity_level.NORMAL)
    def test_not_found_detection(self, page: Page) -> None:
        page.goto(settings.base_url.rstrip("/") + MISSING_PATH, wait_until="domcontentloaded", timeout=25000)
        assert BasePage(page).is_not_found_page(), "BasePage.is_not_found_page() 未识别 404 页面"

    @allure.story("404")
    @allure.title("H5 未匹配路由显示 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.h5
    def test_h5_not_found_page(self, h5_page: Page) -> None:
        h5_page.goto(settings.base_url.rstrip("/") + MISSING_PATH, wait_until="domcontentloaded", timeout=25000)
        _assert_404(h5_page)
        assert BasePage(h5_page).is_not_found_page(), "H5 404 未被页面对象识别"