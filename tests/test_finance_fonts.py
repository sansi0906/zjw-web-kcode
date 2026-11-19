# -*- coding: utf-8 -*-
"""
产业金融页面字体一致性测试
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.finance_page import FinancePage

pytestmark = [pytest.mark.fonts, pytest.mark.regression]


@allure.feature("产业金融字体一致性")
class TestFinanceFonts(BasePageTest):
    """产业金融页面字体一致性测试"""

    page_name = "产业金融"
    page_fixture_name = "finance_page"

    @allure.story("字体一致性")
    @allure.title("产业金融卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_finance_title_font_consistency(self) -> None:
        self.page_obj.open()
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        titles = self.page_obj.page.evaluate(
            """() => Array.from(document.querySelectorAll('.finance-card h3, .finance-card h2, [class*="finance-card"] h3, [class*="finance-card"] h2'))
                .map(e => (e.textContent||'').trim().slice(0,40))
                .filter(t => t)"""
        )
        if len(titles) < 2:
            pytest.skip("当前环境未找到足够金融卡片标题（<2），无法验证字体一致性")
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in titles:
            el = self.page_obj.page.locator(f"h3:has-text('{text}'), h2:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style
        assert len(styles) >= 2, "仅找到 %d 个金融标题" % len(styles)
        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "金融标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("finance_title_font", "info")