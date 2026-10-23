# -*- coding: utf-8 -*-
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.demand_page import DemandPage


@allure.feature("产业需求字体一致性")
class TestDemandPageFonts(BasePageTest):
    page_name = "产业需求"
    page_fixture_name = "demand_page"

    @allure.story("字体一致性")
    @allure.title("产业需求描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_desc_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        desc_texts = ["住宅配套系列，含专票卸车。", "毛坯房配套全系列、含专票13%含运费卸车。", "住宅配套全系列、含专票13%，含运费卸车。"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个需求描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "需求描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("demand_desc_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业需求金额字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_amount_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        amount_texts = ["150万元", "19万元", "15万元", "22万元"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in amount_texts:
            el = self.page_obj.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个需求金额" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "需求金额 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("demand_amount_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业需求大号金额字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_big_amount_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        amount_texts = ["150万", "19万", "15万", "22万"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in amount_texts:
            el = self.page_obj.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个大号金额" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "大号金额 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("demand_big_amount_font", "info")
