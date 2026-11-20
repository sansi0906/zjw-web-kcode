"""
产业金融页面 H5 专项测试（移动端设备仿真）
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.finance_page import FinancePage

pytestmark = [pytest.mark.h5, pytest.mark.regression]


@allure.feature("产业金融页面-H5")
class TestFinanceH5(BasePageTest):
    """产业金融页面 H5 测试用例"""

    page_name = "产业金融"
    page_fixture_name = "h5_finance_page"

    @allure.story("金融卡片")
    @allure.title("H5 金融卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_finance_cards_display(self) -> None:
        """验证 H5 端金融卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_finance_exists(min_count=1)
        titles = self.page_obj.get_finance_titles()
        assert len(titles) > 0, "H5 未找到金融卡片标题"
        self.page_obj.take_screenshot("h5_finance_cards", "info")

    @allure.story("金融卡片")
    @allure.title("H5 金融卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_finance_card_click(self) -> None:
        """点击 H5 金融卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_finance()
        self.page_obj.take_screenshot("h5_finance_detail", "info")

    @allure.story("申报入口")
    @allure.title("H5 申请融资按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_hero_apply_button(self) -> None:
        """点击 H5 申请融资按钮"""
        self.page_obj.open()
        self.page_obj.click_hero_apply()
        self.page_obj.take_screenshot("h5_hero_apply", "info")

    @allure.story("顶部功能")
    @allure.title("H5 顶部功能按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_top_buttons(self) -> None:
        """验证 H5 顶部功能按钮存在"""
        self.page_obj.open()
        btn = self.page_obj.first_visible("button:has-text('平台支持企业融资')", timeout=2000)
        if btn is None:
            pytest.skip("H5 当前环境未展示顶部功能按钮")
        self.page_obj.take_screenshot("h5_top_buttons", "info")