# -*- coding: utf-8 -*-
"""
重点项目页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.key_project_page import KeyProjectsPage


@allure.feature("重点项目字体一致性")
class TestKeyProjectFonts(BasePageTest):
    """重点项目页面字体一致性测试"""

    page_name = "重点项目"
    page_fixture_name = "key_project_page"

    @allure.story("字体一致性")
    @allure.title("重点项目标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_kp_project_title_font_consistency(self) -> None:
        """验证重点项目标题字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = ["胡家园学校校舍修缮工程施工", "天津外国语大学蓟州外国语学校项目弱电智能化工程", "幸福里住宅小区电力配套EPC工程", "天津南开学校教育集团新建高中项目监理"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个项目标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "项目标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("kp_project_title_font", "info")

    @allure.story("字体一致性")
    @allure.title("重点项目筛选Tab字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_kp_filter_tab_font_consistency(self) -> None:
        """验证重点项目筛选Tab字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        tab_texts = ["房建项目", "市政项目", "其他项目"]
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
        self.page_obj.take_screenshot("kp_filter_tab_font", "info")

    @allure.story("字体一致性")
    @allure.title("重点项目描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_kp_desc_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        desc_texts = ["招标施工天津市", "天津市", "胡家园学校校舍修缮工程施工招标施工天津市"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个项目描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "项目描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("kp_desc_font", "info")
