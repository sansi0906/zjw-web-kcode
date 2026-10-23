"""
产业政策页面测试用例

URL: https://dev.tj.gongrenle.com/industryPolicy

"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.industry_policy_page import IndustryPolicyPage


@allure.feature("产业政策页面")
class TestIndustryPolicy(BasePageTest):
    """产业政策页面测试用例"""

    page_name = "产业政策"
    page_fixture_name = "industry_policy_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 政策筛选测试 ===================

    @allure.story("政策筛选")
    @allure.title("全部政策筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_政策资讯(self) -> None:
        """筛选政策资讯分类"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("政策资讯")
        self.page_obj.take_screenshot("filter_全部", "info")

    @allure.story("政策筛选")
    @allure.title("推荐政策筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_行业动态(self) -> None:
        """筛选行业动态分类"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("行业动态")
        self.page_obj.take_screenshot("filter_推荐", "info")

    @allure.story("政策列表")
    @allure.title("政策卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_policy_cards_display(self) -> None:
        """验证政策卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_policies_exist(min_count=1)
        titles = self.page_obj.get_policy_titles()
        assert len(titles) > 0, "未找到政策标题"
        self.page_obj.take_screenshot("policy_cards", "info")

    @allure.story("政策列表")
    @allure.title("政策卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_policy_click(self) -> None:
        """点击政策卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_policy()
        self.page_obj.take_screenshot("policy_detail", "info")

    @allure.story("政策详情")
    @allure.title("查看全部政策按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部政策按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")

    # ==================== 分页测试 ===================

    @allure.story("分页")
    @allure.title("分页页码展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_pages_display(self) -> None:
        """分页组件应展示页码且默认选中第 1 页"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        pages = self.page_obj.get_pagination_pages()
        assert pages, "未找到分页页码"
        assert "1" in pages, f"分页缺少第 1 页，实际: {pages}"
        active = self.page_obj.get_active_pagination_page()
        assert active == "1", f"默认激活页应为 1，实际为 {active!r}"

    @allure.story("分页")
    @allure.title("翻页后列表内容变化")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pagination_switches_content(self) -> None:
        """点击第 2 页后，列表内容必须变化且激活页变为 2"""
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(2000)
        pages = self.page_obj.get_pagination_pages()
        if "2" not in pages:
            pytest.skip(f"当前政策数据仅 {pages} 页，无第 2 页可翻")
        titles_p1 = self.page_obj.get_list_titles()
        assert titles_p1, "第 1 页政策列表为空"

        assert self.page_obj.click_pagination_page("2"), "点击第 2 页失败"
        self.page_obj.page.wait_for_timeout(1500)

        active = self.page_obj.get_active_pagination_page()
        assert active == "2", f"翻页后激活页应为 2，实际为 {active!r}"
        titles_p2 = self.page_obj.get_list_titles()
        assert titles_p2, "第 2 页政策列表为空"
        assert titles_p1 != titles_p2, "翻页后政策列表内容未变化（分页未生效）"
        self.page_obj.take_screenshot("policy_pagination_page2", "info")
