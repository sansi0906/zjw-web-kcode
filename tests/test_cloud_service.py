"""
云服务页面测试用例

URL: https://dev.tj.gongrenle.com/cloudService

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.cloud_service_page import CloudServicePage


@allure.feature("云服务页面")
class TestCloudService(BasePageTest):
    """云服务页面测试用例"""

    page_name = "云服务"
    page_fixture_name = "cloud_service_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 服务筛选测试 ===================

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