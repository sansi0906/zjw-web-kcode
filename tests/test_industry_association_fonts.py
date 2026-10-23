# -*- coding: utf-8 -*-
"""
产业协会页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_association_page import IndustryAssociationPage


@allure.feature("产业协会字体一致性")
class TestIndustryAssociationFonts(BasePageTest):
    """产业协会页面字体一致性测试"""

    page_name = "产业协会"
    page_fixture_name = "industry_association_page"

    @allure.story("字体一致性")
    @allure.title("产业协会名称字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ia_association_name_font_consistency(self) -> None:
        """验证产业协会名称字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        name_texts = ["天津市建筑业协会", "天津市钢结构幕墙和门窗协会", "天津市勘察设计协会", "天津市环境装饰协会", "天津市建材业协会"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in name_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个协会名称" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "协会名称 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ia_association_name_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业协会示范企业标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ia_demo_news_title_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = [
            "【津造未来】天津市智能建造示范企业经验推广——天津住宅建设发展集团有限公司",
            "【津造未来】天津市智能建造示范企业经验推广——中集建造（天津）有限公司",
            "【津造未来】天津市智能建造示范企业经验推广——中交天津航道局有限公司",
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

        assert len(styles) >= 2, "仅找到 %d 个示范企业标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "示范企业标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ia_demo_news_title_font", "info")
