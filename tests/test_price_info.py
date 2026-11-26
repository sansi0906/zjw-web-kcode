"""
造价信息查询页面测试用例（PC 端）

URL: /priceInfo
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.price_info_page import PriceInfoPage
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content, assert_images_alt

pytestmark = [pytest.mark.regression]


@allure.feature("造价信息查询页面")
class TestPriceInfo(BasePageTest):
    """造价信息查询页面测试用例"""

    page_name = "造价信息查询"
    page_fixture_name = "price_info_page"

    # ==================== 页面标题 ====================

    @allure.story("页面加载")
    @allure.title("页面主标题展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h1_title(self) -> None:
        """验证页面 h1 标题为「建设工程造价信息查询」"""
        self.page_obj.open()
        h1 = self.page_obj.get_h1()
        assert "造价信息" in h1, f"未找到页面标题，实际 h1={h1!r}"
        self.page_obj.take_screenshot("price_info_h1", "info")

    # ==================== 功能 tab ====================

    @allure.story("功能切换")
    @allure.title("功能 tab 展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tabs_display(self) -> None:
        """验证 4 个功能 tab 均展示"""
        self.page_obj.open()
        tabs = self.page_obj.get_tab_names()
        assert len(tabs) >= 4, f"功能 tab 不足 4 个，实际: {tabs}"
        for name in self.page_obj.TAB_NAMES:
            assert name in tabs, f"缺少 tab「{name}」，实际: {tabs}"
        self.page_obj.take_screenshot("price_info_tabs", "info")

    @allure.story("功能切换")
    @allure.title("默认激活材料价格查询")
    @allure.severity(allure.severity_level.NORMAL)
    def test_default_active_tab(self) -> None:
        """默认激活 tab 应为「材料价格查询」"""
        self.page_obj.open()
        active = self.page_obj.get_active_tab()
        assert "材料价格查询" in active, f"默认激活 tab 不正确，实际: {active!r}"

    @allure.story("功能切换")
    @allure.title("切换 tab 生效")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_switch(self) -> None:
        """切换到「预拌混凝土」tab 后激活态与标题更新"""
        self.page_obj.open()
        self.page_obj.click_tab("预拌混凝土")
        active = self.page_obj.get_active_tab()
        assert "预拌混凝土" in active, f"切换后激活 tab 不正确，实际: {active!r}"
        # 切换后应有对应的 h2 标题
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        assert "预拌混凝土" in body, "切换后未找到预拌混凝土相关内容"
        self.page_obj.take_screenshot("price_info_tab_switch", "info")

    # ==================== 筛选区 ====================

    @allure.story("筛选")
    @allure.title("筛选区展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_area(self) -> None:
        """验证数据地区/数据年月/材料分类筛选区展示"""
        self.page_obj.open()
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        for label in ["数据地区", "数据年月", "材料分类"]:
            assert label in body, f"筛选区缺少「{label}」"
        self.page_obj.take_screenshot("price_info_filter", "info")

    # ==================== 价格明细表格 ====================

    @allure.story("价格明细")
    @allure.title("价格明细表格展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_table_display(self) -> None:
        """验证价格明细表格存在且有数据行"""
        self.page_obj.open()
        count = self.page_obj.get_table_count()
        assert count >= 1, f"未找到价格明细表格，table 数={count}"
        rows = self.page_obj.get_table_row_count()
        assert rows >= 1, f"价格明细表格无数据行，行数={rows}"
        self.page_obj.take_screenshot("price_info_table", "info")

    @allure.story("价格明细")
    @allure.title("表格表头完整")
    @allure.severity(allure.severity_level.NORMAL)
    def test_table_headers(self) -> None:
        """验证价格明细表格表头包含关键列"""
        self.page_obj.open()
        headers = self.page_obj.get_table_headers()
        assert headers, "未获取到表格表头"
        body = "".join(headers)
        for key in ["材料名称", "规格型号", "单位", "中准价"]:
            assert key in body, f"表头缺少「{key}」，实际: {headers}"
        self.page_obj.take_screenshot("price_info_headers", "info")

    # ==================== 搜索 ====================

    @allure.story("搜索")
    @allure.title("搜索框展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_input(self) -> None:
        """验证搜索框存在"""
        self.page_obj.open()
        el = self.page_obj.first_visible(self.page_obj.SEARCH_INPUT, timeout=3000)
        assert el is not None, "未找到搜索框"
        self.page_obj.take_screenshot("price_info_search", "info")

    @allure.story("搜索")
    @allure.title("搜索关键词可输入并触发")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_input_and_click(self) -> None:
        """输入关键词并点击搜索，页面应正常响应"""
        self.page_obj.open()
        self.page_obj.fill_search("钢筋")
        self.page_obj.click_search()
        # 搜索后页面仍应保留表格或给出无结果提示
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        assert ("价格明细" in body) or ("没有" in body) or ("暂无" in body), "搜索后页面无合理响应"
        self.page_obj.take_screenshot("price_info_search_result", "info")

    # ==================== 分页 ====================

    @allure.story("分页")
    @allure.title("分页组件展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self) -> None:
        """验证分页组件存在（数据超过 1 页时）"""
        self.page_obj.open()
        pages = self.page_obj.get_pagination_page_count()
        if pages < 2:
            pytest.skip("当前数据不足 2 页，分页不适用")
        assert pages >= 2, f"分页页数异常: {pages}"
        self.page_obj.take_screenshot("price_info_pagination", "info")

    @allure.story("分页")
    @allure.title("翻页后表格更新")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_switch(self) -> None:
        """切换到第 2 页后表格仍有数据"""
        self.page_obj.open()
        pages = self.page_obj.get_pagination_page_count()
        if pages < 2:
            pytest.skip("当前数据不足 2 页，分页不适用")
        self.page_obj.goto_page(2)
        rows = self.page_obj.get_table_row_count()
        assert rows >= 1, f"翻页后表格无数据，行数={rows}"
        self.page_obj.take_screenshot("price_info_page2", "info")
    @allure.story("功能切换")
    @allure.title("切换到预拌砂浆 tab")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tab_switch_mortar(self) -> None:
        """切换到「预拌砂浆」tab 后激活态更新"""
        self.page_obj.open()
        self.page_obj.click_tab("预拌砂浆")
        active = self.page_obj.get_active_tab()
        assert "预拌砂浆" in active, f"切换后激活 tab 不正确，实际: {active!r}"
        self.page_obj.take_screenshot("price_info_tab_mortar", "info")

    @allure.story("功能切换")
    @allure.title("切换到人工单价 tab")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tab_switch_labor(self) -> None:
        """切换到「人工单价」tab 后激活态更新"""
        self.page_obj.open()
        self.page_obj.click_tab("人工单价")
        active = self.page_obj.get_active_tab()
        assert "人工单价" in active, f"切换后激活 tab 不正确，实际: {active!r}"
        self.page_obj.take_screenshot("price_info_tab_labor", "info")

    @allure.story("筛选")
    @allure.title("数据地区筛选切换")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_region_switch(self) -> None:
        """切换数据地区后页面正常响应（动态读取可用选项）"""
        self.page_obj.open()
        opts = self.page_obj.get_filter_options(0)
        current = self.page_obj.get_filter_current_value(0)
        candidates = [o for o in opts if o != current]
        if not candidates:
            pytest.skip("数据地区仅一个选项，无法切换")
        target = candidates[0]
        self.page_obj.select_filter(0, target)
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        assert target in body, f"切换数据地区后未反映 {target}"
        self.page_obj.take_screenshot("price_info_filter_region", "info")

    @allure.story("筛选")
    @allure.title("数据年月筛选切换")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_month_switch(self) -> None:
        """切换数据年月后页面正常响应（动态读取可用选项）"""
        self.page_obj.open()
        opts = self.page_obj.get_filter_options(1)
        current = self.page_obj.get_filter_current_value(1)
        candidates = [o for o in opts if o != current]
        if not candidates:
            pytest.skip("数据年月仅一个选项，无法切换")
        target = candidates[0]
        self.page_obj.select_filter(1, target)
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        assert target in body, f"切换数据年月后未反映 {target}"
        self.page_obj.take_screenshot("price_info_filter_month", "info")

    @allure.story("搜索")
    @allure.title("搜索无结果提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_no_result(self) -> None:
        """搜索不存在的关键词应给出无结果或空表"""
        self.page_obj.open()
        self.page_obj.fill_search("zzz不存在的关键词zzz")
        self.page_obj.click_search()
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        # 不崩溃即可；允许空表或提示
        assert ("价格明细" in body) or ("没有" in body) or ("暂无" in body) or ("无数据" in body), "搜索后页面异常"
        self.page_obj.take_screenshot("price_info_search_no_result", "info")
    @allure.story("悬浮功能区")
    @allure.title("在线客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_price_info_customer_service(self) -> None:
        """点击在线客服悬浮按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.FLOAT_CUSTOMER_SERVICE, timeout=3000)
        assert btn is not None, "未找到在线客服按钮"
        self.page_obj.click_customer_service()
        self.page_obj.take_screenshot("price_info_customer_service", "info")

    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_price_info_intent_form(self) -> None:
        """点击意向填报悬浮按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.FLOAT_INTENT_FORM, timeout=3000)
        assert btn is not None, "未找到意向填报按钮"
        self.page_obj.click_intent_form()
        self.page_obj.take_screenshot("price_info_intent_form", "info")
    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="price_info")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="price_info")

    @allure.story("页面健康度")
    @allure.title("图片 alt 文本")
    @allure.severity(allure.severity_level.MINOR)
    def test_images_alt(self, test_data) -> None:
        self.page_obj.open()
        assert_images_alt(self.page_obj.page, test_data, page_key="price_info", key="images_alt")