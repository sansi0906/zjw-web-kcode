"""
产业政策页面测试用例

URL: https://dev.tj.gongrenle.com/industryPolicy

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_policy_page import IndustryPolicyPage


@allure.feature("产业政策页面")
class TestIndustryPolicy(BasePageTest):
    """产业政策页面测试用例"""

    page_name = "产业政策"
    page_fixture_name = "industry_policy_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 政策筛选测试 ===================

    @allure.story("政策筛选")
    @allure.title("全部政策筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_全部(self) -> None:
        """筛选全部政策"""
        self.page_obj.open()
        self.page_obj.click_filter("全部")
        self.page_obj.assert_filter_works("全部")
        self.page_obj.take_screenshot("filter_全部", "info")

    @allure.story("政策筛选")
    @allure.title("推荐政策筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_推荐(self) -> None:
        """筛选推荐政策"""
        self.page_obj.open()
        self.page_obj.click_filter("推荐")
        self.page_obj.assert_filter_works("推荐")
        self.page_obj.take_screenshot("filter_推荐", "info")

    @allure.story("政策列表")
    @allure.title("政策卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_policy_cards_display(self) -> None:
        """验证政策卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_policies_exist(min_count=1)
        titles = self.page_obj.get_policy_titles()
        assert len(titles) > 0, "未找到政策标题"
        self.page_obj.take_screenshot("policy_cards", "info")

    @allure.story("政策列表")
    @allure.title("政策卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_policy_click(self) -> None:
        """点击政策卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_policy()
        self.page_obj.take_screenshot("policy_detail", "info")

    @allure.story("政策详情")
    @allure.title("查看全部政策按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部政策按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")