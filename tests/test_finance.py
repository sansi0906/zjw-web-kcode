"""
产业金融页面测试用例
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.finance_page import FinancePage

import pytest
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content, assert_images_alt

pytestmark = [pytest.mark.regression]


@allure.feature("产业金融页面")
class TestFinance(BasePageTest):
    """产业金融页面测试用例"""

    page_name = "产业金融"
    page_fixture_name = "finance_page"

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="finance")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="finance")

    @allure.story("金融卡片")
    @allure.title("金融卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_finance_cards_display(self) -> None:
        """验证金融卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_finance_exists(min_count=1)
        titles = self.page_obj.get_finance_titles()
        assert len(titles) > 0, "未找到金融卡片标题"
        self.page_obj.take_screenshot("finance_cards", "info")

    @allure.story("金融卡片")
    @allure.title("金融卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_finance_card_click(self) -> None:
        """点击金融卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_finance()
        self.page_obj.take_screenshot("finance_detail", "info")

    @allure.story("申报入口")
    @allure.title("申请融资按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hero_apply_button(self) -> None:
        """点击申请融资按钮"""
        self.page_obj.open()
        self.page_obj.click_hero_apply()
        self.page_obj.take_screenshot("hero_apply", "info")

    @allure.story("顶部功能")
    @allure.title("顶部功能按钮")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="当前环境未展示顶部功能按钮（站点已知限制）", strict=False)
    def test_top_buttons(self) -> None:
        """验证顶部功能按钮存在"""
        self.page_obj.open()
        btn = self.page_obj.first_visible("button:has-text('平台支持企业融资')", timeout=2000)
        assert btn is not None, "当前环境未展示顶部功能按钮"
        self.page_obj.take_screenshot("top_buttons", "info")
    @allure.story("金融卡片")
    @allure.title("金融卡片标题与描述展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_finance_card_titles_and_descs(self) -> None:
        """验证金融卡片标题与描述非空"""
        self.page_obj.open()
        titles = self.page_obj.get_finance_card_titles()
        descs = self.page_obj.get_finance_card_descriptions()
        assert len(titles) >= 3, f"金融卡片标题不足 3 个，实际: {titles}"
        assert len(descs) >= 3, f"金融卡片描述不足 3 条，实际: {len(descs)}"
        for d in descs:
            assert len(d) > 5, f"金融卡片描述过短: {d!r}"
        self.page_obj.take_screenshot("finance_card_titles_descs", "info")

    @allure.story("金融卡片")
    @allure.title("金融卡片按钮展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_finance_card_buttons(self) -> None:
        """验证金融卡片存在按钮（查看详情/申请融资）"""
        self.page_obj.open()
        btns = self.page_obj.get_finance_card_button_texts()
        assert len(btns) >= 3, f"金融卡片按钮不足 3 个，实际: {btns}"
        self.page_obj.take_screenshot("finance_card_buttons", "info")

    @allure.story("金融卡片")
    @allure.title("金融卡片查看详情按钮点击")
    @allure.severity(allure.severity_level.NORMAL)
    def test_finance_card_detail_button(self) -> None:
        """点击金融卡片「查看详情」按钮"""
        self.page_obj.open()
        btns = self.page_obj.get_finance_card_button_texts()
        if "查看详情" not in btns:
            pytest.skip("当前环境金融卡片无「查看详情」按钮")
        self.page_obj.click_finance_card_button("查看详情")
        self.page_obj.take_screenshot("finance_card_detail", "info")
    @allure.story("悬浮功能区")
    @allure.title("在线客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_finance_customer_service(self) -> None:
        """点击在线客服悬浮按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.FLOAT_CUSTOMER_SERVICE, timeout=3000)
        assert btn is not None, "未找到在线客服按钮"
        self.page_obj.click_customer_service()
        self.page_obj.take_screenshot("finance_customer_service", "info")

    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_finance_intent_form(self) -> None:
        """点击意向填报悬浮按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.FLOAT_INTENT_FORM, timeout=3000)
        assert btn is not None, "未找到意向填报按钮"
        self.page_obj.click_intent_form()
        self.page_obj.take_screenshot("finance_intent_form", "info")
    @allure.story("页面健康度")
    @allure.title("图片 alt 文本")
    @allure.severity(allure.severity_level.MINOR)
    def test_images_alt(self, test_data) -> None:
        self.page_obj.open()
        assert_images_alt(self.page_obj.page, test_data, page_key="finance", key="images_alt")