# -*- coding: utf-8 -*-
"""首页字体一致性测试 - 数据驱动（从 font_tests.homepage_full 读取）。"""
from __future__ import annotations

import allure
import pytest

from pages.home_page import HomePage
from utils.font_assert import run_font_check

pytestmark = [pytest.mark.fonts, pytest.mark.homepage, pytest.mark.regression]


@allure.feature("首页")
@allure.story("字体一致性")
class TestHomePageFonts:
    """首页字体一致性测试 - YAML 数据驱动"""

    @pytest.fixture(autouse=True)
    def _goto_home(self, home_page: HomePage) -> None:
        home_page.goto()
        try:
            home_page.page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass

    def _run(
        self,
        home_page: HomePage,
        test_data: dict,
        module_key: str,
        label: str,
        screenshot: str,
    ) -> None:
        run_font_check(
            home_page.page, test_data, "homepage_full", module_key, label
        )
        home_page.take_screenshot(screenshot, "info")

    @allure.title("首页区块标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_section_title_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "section_title", "区块标题", "font_consistency")

    @allure.title("首页服务卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_service_card_title_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "service_card_title", "服务卡片标题", "service_card_font_consistency")

    @allure.title("首页按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_button_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "tab_button", "Tab按钮", "button_font_consistency")

    @allure.title("首页描述文字字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_body_desc_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "body_desc", "描述文字", "body_desc_font_consistency")

    @allure.title("首页页脚导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_nav_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "footer_nav", "页脚导航", "footer_nav_font_consistency")

    @allure.title("热搜词字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_hot_search_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "hot_search", "热搜词", "hot_search_font_consistency")

    @allure.title("新闻标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_title_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "news_title", "新闻标题", "news_title_font_consistency")

    @allure.title("供应品目字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_item_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "supply_item", "供应品目", "supply_item_font_consistency")

    @allure.title("页脚服务链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_service_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "footer_service", "页脚服务", "footer_service_font_consistency")

    @allure.title("津筑云商Tab字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_jzys_tab_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "jzys_tab", "津筑云商Tab", "jzys_tab_font_consistency")

    @allure.title("首页顶部导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_nav_link_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "nav_link", "导航链接", "nav_link_font_consistency")

    @allure.title("首页会展信息字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_exhibition_info_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "exhibition_info", "会展信息", "exhibition_info_font_consistency")

    @allure.title("首页产业需求联系人字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_contact_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "demand_contact", "联系人", "demand_contact_font_consistency")

    @allure.title("首页产业需求数量字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_count_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "demand_count", "需求数量", "demand_count_font_consistency")

    @allure.title("首页新闻日期字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_date_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "news_date", "新闻日期", "news_date_font_consistency")

    @allure.title("首页新闻描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_desc_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "news_desc", "新闻描述", "news_desc_font_consistency")

    @allure.title("首页悬浮按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_float_button_font_consistency(self, home_page: HomePage, test_data) -> None:
        self._run(home_page, test_data, "float_button", "悬浮按钮", "float_button_font_consistency")
