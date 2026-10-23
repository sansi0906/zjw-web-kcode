# -*- coding: utf-8 -*-
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_news_page import IndustryNewsPage


@allure.feature("产业新闻字体一致性")
class TestIndustryNewsFonts(BasePageTest):
    page_name = "产业新闻"
    page_fixture_name = "industry_news_page"

    @allure.story("字体一致性")
    @allure.title("产业新闻卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_title_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        title_texts = ["饿飞飞飞我分为", "测试新增", "开幕！2025第五届国际工程建设供应链博览会！"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"h2:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("news_title_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业新闻描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_desc_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        desc_texts = ["微风范围分为访问范围", "范围分为访问范围", "时代大厦是的是的是多少打撒"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"p:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("news_desc_font", "info")

    @allure.story("字体一致性")
    @allure.title("产业新闻发布时间字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_time_font_consistency(self) -> None:
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        time_texts = ["2026-10-10", "2026-10-08", "2025-09-23"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in time_texts:
            el = self.page_obj.page.locator(f"time:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个发布时间" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "发布时间 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("news_time_font", "info")
