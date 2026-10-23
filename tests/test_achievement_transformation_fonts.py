# -*- coding: utf-8 -*-
"""
成果转化页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.achievement_transformation_page import AchievementTransformationPage


@allure.feature("成果转化字体一致性")
class TestAchievementTransformationFonts(BasePageTest):
    """成果转化页面字体一致性测试"""

    page_name = "成果转化"
    page_fixture_name = "achievement_transformation_page"

    @allure.story("字体一致性")
    @allure.title("成果转化项目标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_at_project_title_font_consistency(self) -> None:
        """验证成果转化项目标题字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = ["复杂环境下适应性深基坑智能建造技术的研发与应用", "轨道交通装配式连续梁产业化关键技术研究"]
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
        self.page_obj.take_screenshot("at_project_title_font", "info")

    @allure.story("字体一致性")
    @allure.title("成果转化机构名称字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_at_institution_name_font_consistency(self) -> None:
        """验证成果转化机构名称字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        name_texts = ["天津城建大学", "天津大学", "国土学院", "河北工业大学"]
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

        assert len(styles) >= 2, "仅找到 %d 个机构名称" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "机构名称 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("at_institution_name_font", "info")

    @allure.story("字体一致性")
    @allure.title("成果转化研发单位字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_at_company_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        name_texts = [
            "中国建筑第六工程局有限公司",
            "中国铁建大桥局集团有限公司",
            "中铁十八局集团有限公司",
            "中国天辰工程有限公司",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in name_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个研发单位" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "研发单位 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("at_company_font", "info")

    @allure.story("字体一致性")
    @allure.title("成果转化技术方向标签字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_at_tech_tag_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        tag_texts = [
            "装配式建筑智能BIM设计与优化",
            "建筑智能数字化设计",
            "智能施工平台",
            "建筑信息建模（BIM）",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in tag_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个技术方向标签" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "技术方向标签 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("at_tech_tag_font", "info")
