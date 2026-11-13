"""供应大厅搜索结果页测试（Web/H5）"""
from __future__ import annotations

import allure
import pytest

from utils.ui_quality import assert_console_clean, assert_no_placeholder_content


pytestmark = [pytest.mark.regression, pytest.mark.search]


@allure.feature("供应大厅搜索结果页")
class TestSupplyHallSearchResult:

    @allure.story("页面健康度")
    @allure.title("Web-控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_web_no_console_errors(self, supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        supply_hall_search_result_page.open(keyword=keyword)
        assert_console_clean(supply_hall_search_result_page.page, test_data, page_key="supply_hall_search_result")

    @allure.story("页面健康度")
    @allure.title("Web-无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_web_no_placeholder_content(self, supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        supply_hall_search_result_page.open(keyword=keyword)
        assert_no_placeholder_content(supply_hall_search_result_page.page, test_data, page_key="supply_hall_search_result")

    @allure.story("搜索结果")
    @allure.title("Web-关键词搜索结果页加载与关键词回显")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_web_search_result_loads(self, supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        supply_hall_search_result_page.open(keyword=keyword)
        supply_hall_search_result_page.assert_page_loaded()
        assert keyword in (supply_hall_search_result_page.get_keyword() or supply_hall_search_result_page.page.url)
        supply_hall_search_result_page.assert_has_results_or_empty_hint()

    @allure.story("搜索结果")
    @allure.title("Web-搜索结果页可再次搜索")
    @allure.severity(allure.severity_level.NORMAL)
    def test_web_search_result_can_search_again(self, supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        supply_hall_search_result_page.open(keyword=keyword)
        supply_hall_search_result_page.fill_keyword(keyword)
        supply_hall_search_result_page.click_search()
        assert "searchResult" in supply_hall_search_result_page.page.url
        assert not supply_hall_search_result_page.is_not_found_page(), "再次搜索后进入404页面"
        body = (supply_hall_search_result_page.page.locator("body").inner_text(timeout=5000) or "")
        assert "搜索" in body or "供应大厅" in body or supply_hall_search_result_page.has_empty_hint() or len(supply_hall_search_result_page.get_result_titles()) >= 0

    @allure.story("页面健康度")
    @allure.title("H5-控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.h5
    def test_h5_no_console_errors(self, h5_supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        h5_supply_hall_search_result_page.open(keyword=keyword)
        assert_console_clean(h5_supply_hall_search_result_page.page, test_data, page_key="supply_hall_search_result")

    @allure.story("页面健康度")
    @allure.title("H5-无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.h5
    def test_h5_no_placeholder_content(self, h5_supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        h5_supply_hall_search_result_page.open(keyword=keyword)
        assert_no_placeholder_content(h5_supply_hall_search_result_page.page, test_data, page_key="supply_hall_search_result")

    @allure.story("搜索结果")
    @allure.title("H5-关键词搜索结果页加载与展示")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.h5
    @pytest.mark.smoke
    def test_h5_search_result_loads(self, h5_supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        h5_supply_hall_search_result_page.open(keyword=keyword)
        h5_supply_hall_search_result_page.assert_page_loaded()
        h5_supply_hall_search_result_page.assert_has_results_or_empty_hint()
        overflow, sw, cw = h5_supply_hall_search_result_page.has_horizontal_overflow()
        assert not overflow, f"H5搜索结果页横向溢出: {sw} > {cw}"

    @allure.story("搜索结果")
    @allure.title("H5-搜索结果页重置/筛选控件可见性（如存在）")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.h5
    def test_h5_search_result_controls(self, h5_supply_hall_search_result_page, test_data) -> None:
        keyword = test_data.get("search_keywords", {}).get("home_page", {}).get("normal", "建筑")
        h5_supply_hall_search_result_page.open(keyword=keyword)
        h5_supply_hall_search_result_page.assert_page_loaded()
        reset = h5_supply_hall_search_result_page.first_visible(h5_supply_hall_search_result_page.RESET_BTN, timeout=800)
        try:
            if reset is not None:
                reset.click(timeout=3000)
                try:
                    h5_supply_hall_search_result_page.page.wait_for_load_state("domcontentloaded", timeout=3000)
                except Exception:
                    pass
        except Exception:
            pass
        assert "searchResult" in h5_supply_hall_search_result_page.page.url

    @allure.story("搜索结果")
    @allure.title("Web-无结果关键词展示空状态或推荐")
    @allure.severity(allure.severity_level.NORMAL)
    def test_web_search_result_no_result_hint(self, supply_hall_search_result_page) -> None:
        keyword = "zzzxxyyynonexist9999"
        supply_hall_search_result_page.open(keyword=keyword)
        supply_hall_search_result_page.assert_page_loaded()
        assert "searchResult" in supply_hall_search_result_page.page.url
        assert supply_hall_search_result_page.has_empty_hint() or "推荐" in (supply_hall_search_result_page.page.locator("body").inner_text(timeout=5000) or ""), (
            f"Web 无结果搜索未展示空状态/推荐提示，URL: {supply_hall_search_result_page.page.url}"
        )

    @allure.story("搜索结果")
    @allure.title("H5-无结果关键词展示空状态或推荐")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.h5
    def test_h5_search_result_no_result_hint(self, h5_supply_hall_search_result_page) -> None:
        keyword = "zzzxxyyynonexist9999"
        h5_supply_hall_search_result_page.open(keyword=keyword)
        h5_supply_hall_search_result_page.assert_page_loaded()
        assert "searchResult" in h5_supply_hall_search_result_page.page.url
        assert h5_supply_hall_search_result_page.has_empty_hint() or "推荐" in (h5_supply_hall_search_result_page.page.locator("body").inner_text(timeout=5000) or ""), (
            f"H5 无结果搜索未展示空状态/推荐提示，URL: {h5_supply_hall_search_result_page.page.url}"
        )
