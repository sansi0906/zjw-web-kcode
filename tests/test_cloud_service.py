"""
云服务页面测试用例

URL: https://dev.tj.gongrenle.com/cloudService

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.cloud_service_page import CloudServicePage


import pytest
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content

pytestmark = [pytest.mark.regression]

@allure.feature("云服务页面")
class TestCloudService(BasePageTest):
    """云服务页面测试用例"""

    page_name = "云服务"
    page_fixture_name = "cloud_service_page"

    # 云服务页面已从首页导航移除，顶部导航完整性/高亮用例不适用
    EXPECTED_NAV_TEXTS = []
    SKIP_NAV_ACTIVE_ASSERT = True

    # 云服务页面本身无顶部导航栏，不继承 BasePageTest 的导航相关通用用例
    def test_nav_completeness(self) -> None:
        pytest.skip("云服务页面无顶部导航栏，不适用导航完整性断言")

    def test_nav_active_state(self) -> None:
        pytest.skip("云服务页面无顶部导航栏，不适用导航高亮断言")

    # ==================== 服务筛选测试 ===================


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="cloud_service")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="cloud_service")


    @allure.story("服务筛选")
    @allure.title("全部服务筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("服务筛选")
    @allure.title("推荐服务筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("服务列表")
    @allure.title("服务卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_service_cards_display(self) -> None:
        """验证服务卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_services_exist(min_count=1)
        titles = self.page_obj.get_service_titles()
        assert len(titles) > 0, "未找到服务标题"
        self.page_obj.take_screenshot("service_cards", "info")

    @allure.story("服务列表")
    @allure.title("服务卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_service_click(self) -> None:
        """点击服务卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_service()
        self.page_obj.take_screenshot("service_detail", "info")

    @allure.story("服务详情")
    @allure.title("查看全部服务按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部服务按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")