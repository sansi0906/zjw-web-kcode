# -*- coding: utf-8 -*-
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.industry_news_page import IndustryNewsPage

pytestmark = [pytest.mark.fonts, pytest.mark.regression]



class TestIndustryNewsFonts(BasePageTest):
    page_name = "产业新闻"
    page_fixture_name = "industry_news_page"

    @allure.story("字体一致性")
    @allure.title("产业新闻卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_title_font_consistency(self) -> None:
        self.page_obj.open()
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        # 标题文本不硬编码：站点内容会变动，改为从页面抓取前 N 个 h2 标题做字体一致性对比
        titles = self.page_obj.page.evaluate(
            """() => Array.from(document.querySelectorAll('h2, h3, .title, [class*="title"]'))
                .map(e => (e.textContent||'').trim().slice(0,40))
                .filter(t => t && !t.includes('登录') && !t.includes('注册') && !t.includes('|'))"""
        )
        titles = titles[:8]
        if len(titles) < 2:
            pytest.skip("当前环境未找到足够新闻标题（<2），无法验证字体一致性")
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in titles:
            el = self.page_obj.page.locator(f"h2:has-text('{text}'), h3:has-text('{text}'), [class*='title']:has-text('{text}')").first
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
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        # 描述文本同样不硬编码：抓取前 N 个 p/li 描述做字体一致性对比
        desc_texts = self.page_obj.page.evaluate(
            """() => Array.from(document.querySelectorAll('p, li, .desc, [class*="desc"]'))
                .map(e => (e.textContent||'').trim().slice(0,40))
                .filter(t => t && !t.includes('登录') && !t.includes('注册') && !t.includes('|'))"""
        )
        desc_texts = desc_texts[:8]
        if len(desc_texts) < 2:
            pytest.skip("当前环境未找到足够新闻描述（<2），无法验证字体一致性")
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"p:has-text('{text}'), li:has-text('{text}'), [class*='desc']:has-text('{text}')").first
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
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
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
