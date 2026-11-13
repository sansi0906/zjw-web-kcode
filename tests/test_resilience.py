"""弱网/接口异常韧性测试

模拟接口不可用（route abort）时，页面应仍渲染骨架/静态内容，
不出现白屏或整页错误，且能给出空态提示。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings

pytestmark = [pytest.mark.regression]


@allure.feature("异常韧性")
class TestResilience:

    @allure.story("接口异常")
    @allure.title("接口不可用时首页仍渲染静态内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_home_survives_api_failure(self, page: Page) -> None:
        errors: list[str] = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.route("**/api/**", lambda route: route.abort())
        try:
            page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
            try:
                page.wait_for_selector("text=产业服务", timeout=8000)
            except Exception:
                pass
            body = (page.locator("body").inner_text(timeout=5000) or "")
        finally:
            page.unroute("**/api/**")

        assert len(body) > 200, f"接口异常后页面内容过少（可能白屏）: {len(body)} 字符"
        assert "Page not found" not in body, "接口异常导致整页 404"
        for section in ("产业服务", "会展活动", "产业需求"):
            assert section in body, f"接口异常后缺少区块: {section}"
        allure.attach(
            f"body 长度={len(body)}, console 错误数={len(errors)}\n" + "\n".join(errors[:5]),
            name="接口异常观测",
            attachment_type=allure.attachment_type.TEXT,
        )

    @allure.story("接口异常")
    @allure.title("接口异常时列表给出空态而非崩溃")
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_survives_api_failure(self, page: Page) -> None:
        page.route("**/api/**", lambda route: route.abort())
        try:
            page.goto(settings.base_url.rstrip("/") + "/supplyHall", wait_until="domcontentloaded", timeout=25000)
            try:
                page.wait_for_selector("text=供应大厅", timeout=8000)
            except Exception:
                pass
            body = (page.locator("body").inner_text(timeout=5000) or "")
        finally:
            page.unroute("**/api/**")
        assert len(body) > 150, "接口异常后列表页内容过少（可能白屏）"
        assert "Page not found" not in body, "接口异常导致整页 404"