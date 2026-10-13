"""
智能建造页面测试用例

URL: https://dev.tj.gongrenle.com/intelligentConstruction

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.intelligent_construction_page import IntelligentConstructionPage


@allure.feature("智能建造页面")
class TestIntelligentConstruction(BasePageTest):
    """智能建造页面测试用例"""

    page_name = "智能建造"
    page_fixture_name = "intelligent_construction_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 建造筛选测试 ===================

    @allure.story("建造筛选")
    @allure.title("全部建造筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_全部(self) -> None:
        """筛选全部建造"""
        self.page_obj.open()
        self.page_obj.click_filter("全部")
        self.page_obj.assert_filter_works("全部")
        self.page_obj.take_screenshot("filter_全部", "info")

    @allure.story("建造筛选")
    @allure.title("推荐建造筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_推荐(self) -> None:
        """筛选推荐建造"""
        self.page_obj.open()
        self.page_obj.click_filter("推荐")
        self.page_obj.assert_filter_works("推荐")
        self.page_obj.take_screenshot("filter_推荐", "info")

    @allure.story("建造列表")
    @allure.title("建造卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_construction_cards_display(self) -> None:
        """验证建造卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_constructions_exist(min_count=1)
        titles = self.page_obj.get_construction_titles()
        assert len(titles) > 0, "未找到建造标题"
        self.page_obj.take_screenshot("construction_cards", "info")

    @allure.story("建造列表")
    @allure.title("建造卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_construction_click(self) -> None:
        """点击建造卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_construction()
        self.page_obj.take_screenshot("construction_detail", "info")

    @allure.story("建造详情")
    @allure.title("查看全部建造按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部建造按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")