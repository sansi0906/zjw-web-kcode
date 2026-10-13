"""产业需求模块测试"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_demand_page import IndustryDemandPage


@allure.feature("产业需求页面")
class TestIndustryDemand(BasePageTest):
    """产业需求页面测试用例"""

    page_name = "产业需求"
    page_fixture_name = "industry_demand_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 需求筛选测试 ===================

    @allure.story("需求筛选")
    @allure.title("全部需求筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_全部(self) -> None:
        """筛选全部需求"""
        self.page_obj.open()
        self.page_obj.click_filter("全部")
        self.page_obj.assert_filter_works("全部")
        self.page_obj.take_screenshot("filter_全部", "info")

    @allure.story("需求筛选")
    @allure.title("推荐需求筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_推荐(self) -> None:
        """筛选推荐需求"""
        self.page_obj.open()
        self.page_obj.click_filter("推荐")
        self.page_obj.assert_filter_works("推荐")
        self.page_obj.take_screenshot("filter_推荐", "info")

    # ==================== 需求列表 ===================

    @allure.story("需求列表")
    @allure.title("需求卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_demand_cards_display(self) -> None:
        """验证需求卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_demands_exist(min_count=1)
        titles = self.page_obj.get_demand_titles()
        assert len(titles) > 0, "未找到需求标题"
        self.page_obj.take_screenshot("demand_cards", "info")

    @allure.story("需求列表")
    @allure.title("需求卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_demand_click(self) -> None:
        """点击需求卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_demand()
        self.page_obj.take_screenshot("demand_detail", "info")

    @allure.story("需求详情")
    @allure.title("查看全部需求按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部需求按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")