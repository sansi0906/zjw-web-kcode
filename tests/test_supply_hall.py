"""供应大厅模块测试"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.supply_hall_page import SupplyHallPage
from utils.browser_helpers import click_and_wait_for_new_page
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content, assert_images_alt

pytestmark = [pytest.mark.regression]

@allure.feature("供应大厅页面")
class TestSupplyHall(BasePageTest):
    """供应大厅页面测试用例"""

    page_name = "供应大厅"
    page_fixture_name = "supply_hall_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="supply_hall")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="supply_hall")

    @allure.story("页面健康度")
    @allure.title("图片alt文本检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_images_alt_text(self, test_data) -> None:
        self.page_obj.open()
        assert_images_alt(self.page_obj.page, test_data, page_key="supply_hall", key="images_alt")


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

    @allure.story("商品交互")
    @allure.title("商品详情与列表一致性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_supply_item_detail_consistency(self) -> None:
        """列表首项点击后，详情页应包含该商品标题且展示价格/商家字段"""
        self.page_obj.open()
        cards = self.page_obj.page.locator("article")
        if cards.count() == 0:
            pytest.skip("未找到供应商品卡片")
        card = cards.first
        card_text = (card.text_content() or "").strip().replace("\n", " ")
        title = card_text[:20]
        assert title, "供应商品卡片标题为空"

        old_url = self.page_obj.page.url
        result_page = self.page_obj.page
        try:
            result_page = click_and_wait_for_new_page(self.page_obj.page, card, timeout=8000)
        except Exception:
            # 无新标签页时 click_and_wait_for_new_page 会抛超时，但点击已生效（同页/弹层跳转）
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=8000)
            except Exception:
                pass

        try:
            assert "detail" in result_page.url, f"点击商品后未进入详情页: {result_page.url}"
            body = (result_page.locator("body").inner_text(timeout=8000) or "").replace("\n", " ")
            key = title[:8]
            assert key in body, f"详情页未包含列表商品标题片段 {key!r}: {body[:120]}"
            assert any(k in body for k in ("产品编号", "产品品牌", "规格型号", "起订量", "价格", "元")), (
                "详情页缺少商品关键字段（编号/品牌/规格/起订量/价格）"
            )
            self.page_obj.take_screenshot("supply_detail_consistency", "info")
        finally:
            if result_page is not self.page_obj.page:
                result_page.close()
            if self.page_obj.page.url != old_url and "supplyHall" not in self.page_obj.page.url:
                self.page_obj.open()

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

    # ==================== 分类筛选 ===================

    @allure.story("分类筛选")
    @allure.title("建筑材料分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_建筑材料(self) -> None:
        """点击建筑材料分类"""
        self.page_obj.open()
        self.page_obj.click_category("建筑材料")
        self.page_obj.take_screenshot("filter_建筑材料", "info")

    @allure.story("分类筛选")
    @allure.title("水电暖通分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_水电暖通(self) -> None:
        """点击水电暖通分类"""
        self.page_obj.open()
        self.page_obj.click_category("水电暖通")
        self.page_obj.take_screenshot("filter_水电暖通", "info")

    @allure.story("分类筛选")
    @allure.title("机械设备分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_机械设备(self) -> None:
        """点击机械设备分类"""
        self.page_obj.open()
        self.page_obj.click_category("机械设备")
        self.page_obj.take_screenshot("filter_机械设备", "info")

    @allure.story("分类筛选")
    @allure.title("工程机械分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_工程机械(self) -> None:
        """点击工程机械分类"""
        self.page_obj.open()
        self.page_obj.click_category("工程机械")
        self.page_obj.take_screenshot("filter_工程机械", "info")

    @allure.story("分类筛选")
    @allure.title("劳务用工分类筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_劳务用工(self) -> None:
        """点击劳务用工分类"""
        self.page_obj.open()
        self.page_obj.click_category("劳务用工")
        self.page_obj.take_screenshot("filter_劳务用工", "info")

    # ==================== 子分类筛选 ===================

    @allure.story("子分类筛选")
    @allure.title("土建子分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_sub_土建(self) -> None:
        """点击土建子分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("土建")
        self.page_obj.take_screenshot("filter_sub_土建", "info")

    @allure.story("子分类筛选")
    @allure.title("装饰装修子分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_sub_装饰装修(self) -> None:
        """点击装饰装修子分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("装饰装修")
        self.page_obj.take_screenshot("filter_sub_装饰装修", "info")

    @allure.story("子分类筛选")
    @allure.title("电气子分类筛选")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_sub_电气(self) -> None:
        """点击电气子分类，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("电气")
        self.page_obj.take_screenshot("filter_sub_电气", "info")

    # ==================== 搜索功能 ===================

    @allure.story("搜索")
    @allure.title("搜索商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search(self) -> None:
        """输入关键词搜索商品"""
        self.page_obj.open()
        self.page_obj.fill_search("钢筋")
        self.page_obj.click_search()
        self.page_obj.take_screenshot("search", "info")

    @allure.story("搜索")
    @allure.title("重置搜索")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reset(self) -> None:
        """测试重置按钮"""
        self.page_obj.open()
        self.page_obj.fill_search("钢筋")
        self.page_obj.click_reset()
        self.page_obj.take_screenshot("reset", "info")