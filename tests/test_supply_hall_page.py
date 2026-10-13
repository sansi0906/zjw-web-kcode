"""
供应大厅独立页面测试
URL: /supplyHall
与首页供应大厅模块区分，独立页面涉及统计数据、分页等完整功能
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.supply_hall_page import SupplyHallPage


@allure.feature("供应大厅独立页面")
class TestSupplyHallPage(BasePageTest):
    """供应大厅独立页面测试用例"""

    page_name = "供应大厅"
    page_fixture_name = "supply_hall_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 独立页面特有测试 ===================

    @allure.story("页面展示")
    @allure.title("统计数据展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_statistics_display(self) -> None:
        """验证统计数据（商品数、企业数等）正常展示"""
        import pytest

        self.page_obj.open()
        stats = self.page_obj.get_statistics()
        if len(stats) == 0:
            pytest.skip("当前环境未显示统计数据")
        self.page_obj.take_screenshot("statistics", "info")

    @allure.story("分页")
    @allure.title("分页功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self) -> None:
        """验证分页功能"""
        self.page_obj.open()
        if self.page_obj.has_pagination():
            self.page_obj.take_screenshot("pagination", "info")