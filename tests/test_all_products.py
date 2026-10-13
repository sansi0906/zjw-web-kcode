"""全部商品模块测试"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.all_products_page import AllProductsPage
from utils.browser_helpers import click_and_wait_for_new_page


@allure.feature("全部商品页面")
class TestAllProducts(BasePageTest):
    """全部商品测试类"""

    page_name = "全部商品"
    page_fixture_name = "all_products_page"

    # ==================== 商品展示测试 ===================

    @allure.story("商品展示")
    @allure.title("商品卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_card_display(self) -> None:
        """验证商品卡片正常展示"""
        self.page_obj.open()
        count = self.page_obj.get_product_count()
        assert count > 0, "未找到商品卡片"

    @allure.story("商品展示")
    @allure.title("价格显示格式")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_price_format(self) -> None:
        """验证价格显示格式正确"""
        self.page_obj.open()
        self.page_obj.assert_prices_displayed()

    @allure.story("商品展示")
    @allure.title("图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_images_load(self) -> None:
        """验证商品图片正常加载"""
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

    # ==================== 商品交互测试 ===================

    @allure.story("商品交互")
    @allure.title("商品卡片点击")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_card_click(self) -> None:
        """点击商品卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_product()

    @allure.story("商品交互")
    @allure.title("商品详情信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_detail_info(self) -> None:
        """验证商品详情页URL包含product或detail"""
        self.page_obj.open()
        product_cards = self.page_obj.page.locator(self.page_obj.PRODUCT_CARDS).first
        if product_cards.is_visible():
            product_cards.click(force=True)
            self.page_obj.wait_for_load()
            url = self.page_obj.page.url
            assert "product" in url.lower() or "detail" in url.lower() or "goods" in url.lower(), \
                f"URL未包含product/detail/goods，当前URL: {url}"