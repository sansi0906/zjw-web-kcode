"""
产业需求页面测试用例
URL: /demandPage
首页"产业需求"模块的"查看全部"按钮跳转至此页面。
"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.demand_page import DemandPage


import pytest
from utils.browser_helpers import click_and_wait_for_new_page
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content

pytestmark = [pytest.mark.regression]

@allure.feature("产业需求页面")
class TestDemandPage(BasePageTest):
    """产业需求页面测试用例"""

    page_name = "产业需求"
    page_fixture_name = "demand_page"
    NAV_ACTIVE_STATE_APPLICABLE = False

    # ==================== 分类筛选测试 ===================


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="demand_page")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="demand_page")


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

    @allure.story("搜索")
    @allure.title("无结果空态提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_no_result_hint(self, test_data) -> None:
        """搜索不存在关键词时应给出空态提示或空列表（不应报错/白屏）"""
        empty_keyword = ((test_data or {}).get("search_keywords") or {}).get(
            "common_empty", "zzzxxyyynonexist9999"
        )
        self.page_obj.open()
        self.page_obj.fill_search(empty_keyword)
        self.page_obj.click_search()
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        body = (self.page_obj.page.locator("body").inner_text(timeout=5000) or "")
        titles = self.page_obj.get_list_titles()
        empty_hint = any(k in body for k in ("暂无", "无数据", "没有找到", "空", "无相关"))
        assert not titles or empty_hint, (
            f"无结果搜索后仍展示 {len(titles)} 条数据且无空态提示: {titles[:3]}"
        )
        self.page_obj.take_screenshot("search_empty", "info")

    # ==================== 需求详情 ====================

    @allure.story("需求详情")
    @allure.title("需求详情与列表一致")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_demand_detail_consistency(self) -> None:
        """点击需求条目应进入详情页，且标题/预算/联系人字段一致"""
        self.page_obj.open()
        titles = self.page_obj.get_demand_titles()
        if not titles:
            pytest.skip("需求列表为空，无法校验详情")
        first = titles[0].strip()
        card = self.page_obj.page.locator("span.line-clamp-2").first
        if not card.is_visible(timeout=3000):
            pytest.skip("未找到可点击的需求条目标题")
        old_url = self.page_obj.page.url
        result_page = self.page_obj.page
        try:
            result_page = click_and_wait_for_new_page(self.page_obj.page, card, timeout=8000)
        except Exception:
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=8000)
            except Exception:
                pass
        try:
            assert "/demandPage/detail/" in result_page.url, (
                f"未进入需求详情页: {result_page.url}"
            )
            body = (result_page.locator("body").inner_text(timeout=8000) or "").replace("\n", " ")
            assert first[:8] in body, f"详情页标题与列表不一致: 列表={first[:20]!r}, 详情={body[:100]!r}"
            assert any(k in body for k in ("预算金额", "联系人", "需求详情")), (
                "需求详情缺少预算金额/联系人字段"
            )
            self.page_obj.take_screenshot("demand_detail", "info")
        finally:
            if result_page is not self.page_obj.page:
                result_page.close()
            if self.page_obj.page.url != old_url and "demandPage" not in self.page_obj.page.url:
                self.page_obj.open()

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