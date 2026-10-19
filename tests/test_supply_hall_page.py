"""
供应大厅独立页面测试
URL: /supplyHall
与首页供应大厅模块区分，独立页面涉及统计数据、分页等完整功能
"""
from __future__ import annotations

import allure
import pytest

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
        """验证统计数据（商品数、企业数等）正常展示

        注意：改版后供应大厅页面可能不展示统计数据，此用例为旧版验证点。
        当前环境已验证无此功能，保留仅作历史参考。
        """
        pytest.skip("改版后供应大厅页面无统计数据展示，已废弃")

    @allure.story("分页")
    @allure.title("分页功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self) -> None:
        """验证分页功能

        注意：改版后供应大厅页面可能无分页组件，此用例为旧版验证点。
        当前环境已验证无此功能，保留仅作历史参考。
        """
        pytest.skip("改版后供应大厅页面无分页组件，已废弃")