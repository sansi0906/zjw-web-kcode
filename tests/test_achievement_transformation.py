"""
成果转化页面测试用例

URL: https://dev.tj.gongrenle.com/achievementTransformation

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.achievement_transformation_page import AchievementTransformationPage


import pytest
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content

pytestmark = [pytest.mark.regression]

@allure.feature("成果转化页面")
class TestAchievementTransformation(BasePageTest):
    """成果转化页面测试用例"""

    page_name = "成果转化"
    page_fixture_name = "achievement_transformation_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 成果筛选测试 ===================


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="achievement_transformation")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="achievement_transformation")


    @allure.story("成果筛选")
    @allure.title("科技创新成果筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("成果筛选")
    @allure.title("课题筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_课题(self) -> None:
        """筛选课题"""
        self.page_obj.open()
        self.page_obj.click_filter("课题")
        self.page_obj.assert_filter_works("课题")
        self.page_obj.take_screenshot("filter_课题", "info")

    @allure.story("成果筛选")
    @allure.title("成果筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_成果(self) -> None:
        """筛选成果"""
        self.page_obj.open()
        self.page_obj.click_filter("成果")
        self.page_obj.assert_filter_works("成果")
        self.page_obj.take_screenshot("filter_成果", "info")

    @allure.story("成果列表")
    @allure.title("成果卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_achievement_cards_display(self) -> None:
        """验证成果卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_achievements_exist(min_count=1)
        titles = self.page_obj.get_achievement_titles()
        assert len(titles) > 0, "未找到成果标题"
        self.page_obj.take_screenshot("achievement_cards", "info")

    @allure.story("成果列表")
    @allure.title("成果卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_achievement_click(self) -> None:
        """点击成果卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_achievement()
        self.page_obj.take_screenshot("achievement_detail", "info")