# -*- coding: utf-8 -*-
"""
产业政策页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_policy_page import IndustryPolicyPage


@allure.feature("产业政策字体一致性")
class TestIndustryPolicyFonts(BasePageTest):
    """产业政策页面字体一致性测试"""

    page_name = "产业政策"
    page_fixture_name = "industry_policy_page"

    @allure.story("字体一致性")
    @allure.title("产业政策筛选Tab字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ip_filter_tab_font_consistency(self) -> None:
        """验证产业政策筛选Tab字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        tab_texts = ["政策资讯", "政策解读", "行业动态"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in tab_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个筛选Tab" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "筛选Tab '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ip_filter_tab_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业政策列表标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ip_policy_title_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = [
            "中共中央办公厅 国务院办公厅关于推进新型城市基础设施建设打造韧性城市的意见",
            "市住房城乡建设委关于我市公共租赁住房轮候管理有关工作的通知",
            "市住房城乡建设委关于发布《天津市智慧工地建设技术标准》的通知",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个政策标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "政策标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ip_policy_title_font", "info")
