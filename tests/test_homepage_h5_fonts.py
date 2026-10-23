# -*- coding: utf-8 -*-
"""
首页 H5 移动端字体一致性测试

使用移动端 viewport (390x844) 验证首页各文本元素组的字体一致性。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from config.settings import settings


def _get_style(page: Page, selector: str) -> dict:
    """获取元素的计算样式"""
    el = page.locator(selector).first
    if el.is_visible():
        return el.evaluate(
            "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
        )
    return {}


@allure.feature("首页 H5 字体一致性")
class TestHomePageH5Fonts:
    """首页 H5 移动端字体一致性测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """设置移动端 viewport 并打开首页"""
        page.set_viewport_size({"width": 390, "height": 844})
        base = settings.base_url.rstrip("/")
        page.goto(base, timeout=30000)
        page.wait_for_timeout(3000)
        self.page = page
        yield

    @allure.story("字体一致性")
    @allure.title("H5 区块标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_section_title_font_consistency(self):
        """验证 H5 首页区块标题字体样式一致

        产业服务、津筑云商、会展活动等 H2 标题
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        section_texts = ["产业服务", "津筑云商", "会展活动"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in section_texts:
            el = self.page.locator(f"h2:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个区块标题: %s" % (len(styles), list(styles.keys()))

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "区块 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 服务卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_service_card_title_font_consistency(self):
        """验证 H5 服务卡片标题字体样式一致"""
        card_titles = ["劳务对接", "AI+工具集", "金融服务", "建筑机器人", "智慧工地"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for title in card_titles:
            el = self.page.locator(f"h3:has-text('{title}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[title] = style

        assert len(styles) >= 2, "仅找到 %d 个服务卡片标题" % len(styles)

        first_title = list(styles.keys())[0]
        first_style = styles[first_title]
        for title, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "服务卡片 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (title, key, style[key], first_title, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 描述文字字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_body_desc_font_consistency(self):
        """验证 H5 描述文字字体样式一致"""
        desc_texts = ["全方位服务产业链", "平台优质企业，精准商务对接", "聚焦建筑行业各类活动"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page.locator(f"p:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个描述文字" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 页脚导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_footer_nav_font_consistency(self):
        """验证 H5 页脚导航链接字体样式一致"""
        nav_texts = ["供应大厅", "产业政策", "智能建造", "重点项目"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in nav_texts:
            el = self.page.locator("footer").locator("text=" + text).first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个页脚导航链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "页脚导航 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 热搜词字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_hot_search_font_consistency(self):
        """验证 H5 热搜词字体样式一致"""
        hot_texts = ["热搜词名称一", "热搜词名称二", "热搜词名称三", "热搜词名称四", "热搜词名称五", "热搜词名称六"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in hot_texts:
            el = self.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个热搜词" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "热搜词 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 新闻标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_news_title_font_consistency(self):
        """验证 H5 新闻标题字体样式一致"""
        news_texts = ["云南石材建材产业发展峰会", "绿色建筑新浪潮来袭！2027广州住博会！"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in news_texts:
            el = self.page.locator(f"text={text}").first
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

    @allure.story("字体一致性")
    @allure.title("H5 供应品目字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_supply_item_font_consistency(self):
        """验证 H5 供应品目字体样式一致"""
        item_texts = ["施工电梯", "配电箱", "灯具、开关面板", "PVC管材、管件", "门窗工程"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in item_texts:
            el = self.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个供应品目" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "供应品目 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 页脚服务链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_footer_service_font_consistency(self):
        """验证 H5 页脚服务链接字体样式一致"""
        svc_texts = ["建材出售", "建材出租", "设备出售", "设备出租", "劳务用工", "产业需求"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in svc_texts:
            el = self.page.locator("footer").locator("text=" + text).first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个页脚服务链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "页脚服务 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 顶部导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_nav_link_font_consistency(self):
        """验证 H5 首页顶部导航链接字体样式一致"""
        nav_texts = ["供应大厅", "智能建造", "重点项目", "产业政策"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in nav_texts:
            el = self.page.locator(f"a:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个导航链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "导航链接 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 会展信息字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_exhibition_info_font_consistency(self):
        """验证 H5 首页会展活动时间/地点字体样式一致"""
        info_texts = [
            "2026-10-06—2026-10-27",
            "昆明世纪城国际会议中心",
            "2026-10-01—2026-11-10",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in info_texts:
            el = self.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个会展信息" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "会展信息 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 产业需求联系人字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_demand_contact_font_consistency(self):
        """验证 H5 首页产业需求联系人姓名字体样式一致"""
        contact_texts = ["董经理", "刘经理"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in contact_texts:
            el = self.page.locator(f"strong:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个联系人" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "联系人 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 产业需求数量字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_demand_count_font_consistency(self):
        """验证 H5 首页产业需求数量字体样式一致"""
        count_texts = ["150", "195", "170"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in count_texts:
            el = self.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个需求数量" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "需求数量 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 新闻日期字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_news_date_font_consistency(self):
        """验证 H5 首页新闻日期字体样式一致"""
        date_texts = ["2026-10-10", "2026-10-08"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in date_texts:
            el = self.page.locator(f"time:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻日期" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻日期 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("H5 新闻描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_news_desc_font_consistency(self):
        """验证 H5 首页新闻描述字体样式一致"""
        desc_texts = ["微风范围分为访问范围", "范围分为访问范围", "时代大厦是的是的是多少打撒"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page.locator(f"p:has-text('{text}')").first
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

    @allure.story("字体一致性")
    @allure.title("H5 悬浮按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_float_button_font_consistency(self):
        """验证 H5 首页悬浮按钮（在线客服/意向填报）字体样式一致"""
        btn_texts = ["在线客服", "意向填报"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in btn_texts:
            el = self.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个悬浮按钮" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "悬浮按钮 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
