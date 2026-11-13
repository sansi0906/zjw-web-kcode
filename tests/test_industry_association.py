"""
产业协会页面测试用例

URL: https://dev.tj.gongrenle.com/industryAssociation

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industry_association_page import IndustryAssociationPage


import pytest
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content

pytestmark = [pytest.mark.regression]

@allure.feature("产业协会页面")
class TestIndustryAssociation(BasePageTest):
    """产业协会页面测试用例"""

    page_name = "产业协会"
    page_fixture_name = "industry_association_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 协会筛选测试 ===================


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="industry_association")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="industry_association")


    @allure.story("协会筛选")
    @allure.title("全部协会筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("协会筛选")
    @allure.title("推荐协会筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("协会列表")
    @allure.title("协会卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_association_cards_display(self) -> None:
        """验证协会卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_associations_exist(min_count=1)
        titles = self.page_obj.get_association_titles()
        assert len(titles) > 0, "未找到协会标题"
        self.page_obj.take_screenshot("association_cards", "info")

    @allure.story("协会列表")
    @allure.title("协会卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_association_click(self) -> None:
        """点击协会卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_association()
        self.page_obj.take_screenshot("association_detail", "info")

    @allure.story("协会详情")
    @allure.title("查看全部协会按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部协会按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")

    # ==================== 协会入驻测试 ===================

    @allure.story("协会入驻")
    @allure.title("协会入驻筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("搜索")
    @allure.title("搜索协会")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search(self) -> None:
        """搜索协会"""
        self.page_obj.open()
        self.page_obj.fill_search("混凝土")
        self.page_obj.click_search()
        self.page_obj.take_screenshot("search", "info")

    # ==================== 分页测试 ===================

    @allure.story("分页")
    @allure.title("分页跳转")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_jump(self) -> None:
        """测试分页跳转功能"""
        self.page_obj.open()
        self.page_obj.jump_to_page(2)
        self.page_obj.take_screenshot("pagination", "info")