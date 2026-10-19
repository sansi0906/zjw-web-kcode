"""供应链地图模块测试 - 已废弃

改版后首页不再展示供应链地图模块，此文件保留仅作历史参考。
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.supply_chain_map_page import SupplyChainMapPage


@pytest.mark.skip(reason="改版后首页无供应链地图模块，已废弃")
@allure.feature("供应链地图")
class TestSupplyChainMap(BasePageTest):
    """供应链地图测试用例 - 已废弃"""

    page_name = "供应链地图"
    page_fixture_name = "supply_chain_map_page"

    @allure.story("地图展示")
    @allure.title("供应链地图正常展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_map_displayed(self) -> None:
        """验证供应链地图区域数据正常展示"""
        self.page_obj.open()
        self.page_obj.assert_map_displayed()
        self.page_obj.take_screenshot("supply_chain_map", "info")

    @allure.story("地图展示")
    @allure.title("分类标签存在")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_category_tabs_exist(self) -> None:
        """验证供应链地图分类标签存在"""
        self.page_obj.open()
        self.page_obj.assert_category_tabs_exist()
        tabs = self.page_obj.get_category_tabs()
        assert len(tabs) > 0, "未找到分类标签"
        self.page_obj.take_screenshot("category_tabs", "info")

    @allure.story("区域数据")
    @allure.title("区域数据展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_region_data_display(self) -> None:
        """验证各区域建材数量数据正常展示"""
        self.page_obj.open()
        count = self.page_obj.get_region_count()
        assert count > 0, "未找到区域数据"
        self.page_obj.take_screenshot("region_data", "info")

    @allure.story("区域数据")
    @allure.title("点击区域详情")
    @allure.severity(allure.severity_level.NORMAL)
    def test_click_region(self) -> None:
        """点击区域查看详情"""
        self.page_obj.open()
        self.page_obj.click_first_region()
        self.page_obj.take_screenshot("region_detail", "info")

    @allure.story("分类筛选")
    @allure.title("建筑建材分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_building_materials(self) -> None:
        """点击建筑建材分类标签"""
        self.page_obj.open()
        self.page_obj.click_category_tab("建筑建材")
        self.page_obj.take_screenshot("filter_building_materials", "info")

    @allure.story("分类筛选")
    @allure.title("机械设备分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_machinery(self) -> None:
        """点击机械设备分类标签"""
        self.page_obj.open()
        self.page_obj.click_category_tab("机械设备")
        self.page_obj.take_screenshot("filter_machinery", "info")