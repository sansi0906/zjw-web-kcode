"""产业化服务模块测试"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.industrial_service_page import IndustrialServicePage


import pytest
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content

pytestmark = [pytest.mark.regression]

@allure.feature("产业化服务页面")
class TestIndustrialService(BasePageTest):
    """产业化服务页面测试用例"""

    page_name = "产业化服务"
    page_fixture_name = "industrial_service_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 服务展示测试 ===================


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="industrial_service")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="industrial_service")


    @allure.story("服务展示")
    @allure.title("产业化服务模块存在")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_industrial_service_module_exists(self) -> None:
        """验证产业化服务模块正常显示"""
        self.page_obj.open()
        self.page_obj.assert_service_exists()
        self.page_obj.take_screenshot("industrial_service_module", "info")

    @allure.story("服务展示")
    @allure.title("服务项展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_service_items_display(self) -> None:
        """验证服务项正常展示"""
        self.page_obj.open()
        count = self.page_obj.get_service_count()
        assert count > 0, "未找到服务项"
        self.page_obj.take_screenshot("service_items", "info")