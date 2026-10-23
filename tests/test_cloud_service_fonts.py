# -*- coding: utf-8 -*-
"""
云服务页面字体一致性测试
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.cloud_service_page import CloudServicePage


@allure.feature("云服务字体一致性")
class TestCloudServiceFonts(BasePageTest):
    """云服务页面字体一致性测试"""

    page_name = "云服务"
    page_fixture_name = "cloud_service_page"

    @allure.story("字体一致性")
    @allure.title("云服务名称字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_cs_service_name_font_consistency(self) -> None:
        """验证云服务名称字体样式一致"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        name_texts = ["项目管理", "设计生产协同", "智慧工地系统", "建筑劳务用工", "智慧运维平台"]
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in name_texts:
            el = self.page_obj.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个云服务名称" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "云服务名称 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("cs_service_name_font", "info")

    @allure.story("字体一致性")
    @allure.title("云服务服务描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_cs_service_desc_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        desc_texts = [
            "经营数据可视化，动态监控项目经营",
            "业务在线化辅助实现管理制度标准化的有效落地",
            "量价入手，可松可紧，精准管控核心材料",
            "商务、技术、生产三线融合，抓住每一个二次经营点",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"li:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个服务描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "服务描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("cs_service_desc_font", "info")
