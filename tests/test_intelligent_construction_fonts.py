# -*- coding: utf-8 -*-
"""
智能建造页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.intelligent_construction_page import IntelligentConstructionPage


@allure.feature("智能建造字体一致性")
class TestIntelligentConstructionFonts(BasePageTest):
    """智能建造页面字体一致性测试"""

    page_name = "智能建造"
    page_fixture_name = "intelligent_construction_page"

    @allure.story("字体一致性")
    @allure.title("智能建造示范项目标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ic_demo_project_title_font_consistency(self) -> None:
        """验证智能建造示范项目标题字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = ["智能建造示范项目", "智能建造新技术新产品", "智能建造标准"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"div.section-title:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个示范项目标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "示范项目 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ic_demo_project_font", "info")

    @allure.story("字体一致性")
    @allure.title("智能建造项目卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ic_project_card_title_font_consistency(self) -> None:
        """验证智能建造项目卡片标题字体样式一致"""
        card_texts = ["柳林城更地块智汇中心大厦", "海油发展天津海洋装备智能制造基地", "天津市第三中心医院（东丽院区）"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in card_texts:
            el = self.page_obj.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个项目卡片标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "项目卡片 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ic_project_card_font", "info")

    @allure.story("字体一致性")
    @allure.title("智能建造标准名称字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_ic_standard_name_font_consistency(self) -> None:
        """验证智能建造标准名称字体样式一致"""
        std_texts = ["住建部智能建造技术导则", "住建部智能建造技术导则（试行）", "天津市智慧工地建设技术标准", "京津冀智能建造技术规程"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in std_texts:
            el = self.page_obj.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个标准名称" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "标准名称 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("ic_standard_font", "info")

