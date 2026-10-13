"""供应大厅模块测试"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.supply_hall_page import SupplyHallPage


@allure.feature("供应大厅页面")
class TestSupplyHall(BasePageTest):
    """供应大厅页面测试用例"""

    page_name = "供应大厅"
    page_fixture_name = "supply_hall_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 页面内容展示 ===================

    @allure.story("页面展示")
    @allure.title("供应大厅页面正常加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_supply_hall_page_load(self) -> None:
        """验证供应大厅页面正常加载（首页模块，不涉及统计数据）"""
        self.page_obj.open()
        self.page_obj.assert_page_loaded()
        self.page_obj.assert_supply_items_exist(min_count=1)
        self.page_obj.take_screenshot("supply_hall_page", "info")

    @allure.story("页面展示")
    @allure.title("供应商品卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_supply_items_display(self) -> None:
        """验证供应商品正常展示"""
        self.page_obj.open()
        self.page_obj.assert_supply_items_exist(min_count=1)
        titles = self.page_obj.get_supply_item_titles()
        assert len(titles) > 0, "未找到供应商品"
        self.page_obj.take_screenshot("supply_items", "info")

    @allure.story("页面展示")
    @allure.title("商品图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_supply_item_images_load(self) -> None:
        """验证供应商品图片正常加载"""
        self.page_obj.open()
        images = self.page_obj.page.locator("img")
        loaded_count = 0
        for i in range(min(images.count(), 10)):
            img = images.nth(i)
            if img.is_visible():
                try:
                    if img.evaluate("el => el.complete && el.naturalHeight > 0"):
                        loaded_count += 1
                except Exception:
                    continue
        assert loaded_count > 0, f"没有图片加载成功，检查了{min(images.count(), 10)}张图片"

    @allure.story("页面展示")
    @allure.title("价格信息展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_supply_item_price_display(self) -> None:
        """验证供应商品价格信息正常展示"""
        self.page_obj.open()
        self.page_obj.assert_prices_displayed()

    # ==================== 商品交互 ===================

    @allure.story("商品交互")
    @allure.title("供应商品点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_supply_item_click(self) -> None:
        """点击供应商品跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_supply_item()
        self.page_obj.take_screenshot("supply_item_detail", "info")

    # ==================== 悬浮功能区 ===================

    @allure.story("悬浮功能区")
    @allure.title("发布商品按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_publish_button(self) -> None:
        """点击发布商品按钮"""
        self.page_obj.open()
        self.page_obj.click_publish()
        self.page_obj.take_screenshot("publish_button", "info")

    @allure.story("悬浮功能区")
    @allure.title("求购询价按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_inquiry_button(self) -> None:
        """点击求购询价按钮"""
        self.page_obj.open()
        self.page_obj.click_inquiry()
        self.page_obj.take_screenshot("inquiry_button", "info")

    @allure.story("悬浮功能区")
    @allure.title("联系客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_customer_service_button(self) -> None:
        """点击联系客服按钮"""
        self.page_obj.open()
        self.page_obj.click_customer_service()
        self.page_obj.take_screenshot("customer_service", "info")

    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_intent_form_button(self) -> None:
        """点击意向填报按钮"""
        self.page_obj.open()
        self.page_obj.click_intent_form()
        self.page_obj.take_screenshot("intent_form", "info")

    # ==================== 分页 ===================

    @allure.story("分页")
    @allure.title("分页功能")
    @allure.severity(allure.severity_level.MINOR)
    def test_pagination(self) -> None:
        """验证分页功能（如有多页商品）"""
        self.page_obj.open()
        if self.page_obj.has_pagination():
            self.page_obj.take_screenshot("pagination", "info")

    # ==================== 导航 ===================

    @allure.story("导航")
    @allure.title("导航到智能建造页面")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_to_intelligent_construction(self) -> None:
        """点击导航跳转到智能建造页面"""
        self.page_obj.open()
        self.page_obj.click_nav_by_text("智能建造")
        self.page_obj.assert_url_contains("intelligentConstruction")
        self.page_obj.take_screenshot("nav_intelligent_construction", "info")

    @allure.story("导航")
    @allure.title("导航到重点项目页面")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_to_key_project(self) -> None:
        """点击导航跳转到重点项目页面"""
        self.page_obj.open()
        self.page_obj.click_nav_by_text("重点项目")
        self.page_obj.assert_url_contains("keyProject")
        self.page_obj.take_screenshot("nav_key_project", "info")