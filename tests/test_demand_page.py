"""
产业需求页面测试用例
URL: /demandPage
首页"产业需求"模块的"查看全部"按钮跳转至此页面。
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.demand_page import DemandPage


@allure.feature("产业需求页面")
class TestDemandPage(BasePageTest):
    """产业需求页面测试用例"""

    page_name = "产业需求"
    page_fixture_name = "demand_page"

    # ==================== 分类筛选测试 ===================

    @allure.story("分类筛选")
    @allure.title("建筑建材分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_建筑建材(self) -> None:
        """筛选建筑建材分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("建筑建材")
        self.page_obj.take_screenshot("filter_建筑建材", "info")

    @allure.story("分类筛选")
    @allure.title("机械设备分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_机械设备(self) -> None:
        """筛选机械设备分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("机械设备")
        self.page_obj.take_screenshot("filter_机械设备", "info")

    @allure.story("分类筛选")
    @allure.title("劳务用工分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_劳务用工(self) -> None:
        """筛选劳务用工分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("劳务用工")
        self.page_obj.take_screenshot("filter_劳务用工", "info")

    @allure.story("分类筛选")
    @allure.title("技术服务分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_技术服务(self) -> None:
        """筛选技术服务分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("技术服务")
        self.page_obj.take_screenshot("filter_技术服务", "info")

    # ==================== 搜索测试 ===================

    @allure.story("搜索")
    @allure.title("搜索功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search(self) -> None:
        """输入关键词搜索"""
        self.page_obj.open()
        self.page_obj.fill_search("钢筋")
        self.page_obj.click_search()
        self.page_obj.take_screenshot("search", "info")

    @allure.story("搜索")
    @allure.title("重置功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reset(self) -> None:
        """测试重置按钮"""
        self.page_obj.open()
        self.page_obj.fill_search("钢筋")
        self.page_obj.click_reset()
        self.page_obj.take_screenshot("reset", "info")

    # ==================== 统计数据测试 ===================

    @allure.story("统计数据")
    @allure.title("统计数据展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_stats_display(self) -> None:
        """验证统计数据正常展示"""
        self.page_obj.open()
        stats = self.page_obj.get_stats_texts()
        self.page_obj.take_screenshot("stats", "info")

    # ==================== 分页测试 ===================

    @allure.story("分页")
    @allure.title("分页跳转")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_jump(self) -> None:
        """测试分页跳转功能"""
        self.page_obj.open()
        self.page_obj.jump_to_page(2)
        self.page_obj.take_screenshot("pagination", "info")