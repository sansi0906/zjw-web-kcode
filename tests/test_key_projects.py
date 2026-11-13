"""重点项目模块测试"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.key_project_page import KeyProjectsPage
from utils.browser_helpers import click_and_wait_for_new_page
from utils.ui_quality import assert_console_clean, assert_no_placeholder_content, assert_images_alt


pytestmark = [pytest.mark.regression]

@allure.feature("重点项目页面")
class TestKeyProjects(BasePageTest):
    """重点项目测试类"""

    page_name = "重点项目"
    page_fixture_name = "key_project_page"


    # ==================== 页面健康度（配置驱动，可扩展） ===================

    @allure.story("页面健康度")
    @allure.title("控制台无未知错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, test_data) -> None:
        self.page_obj.open()
        assert_console_clean(self.page_obj.page, test_data, page_key="key_project")

    @allure.story("页面健康度")
    @allure.title("无未知测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, test_data) -> None:
        self.page_obj.open()
        assert_no_placeholder_content(self.page_obj.page, test_data, page_key="key_project")

    @allure.story("页面健康度")
    @allure.title("图片alt文本检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_images_alt_text(self, test_data) -> None:
        self.page_obj.open()
        assert_images_alt(self.page_obj.page, test_data, page_key="key_project", key="images_alt")

    # ==================== 项目展示测试 ===================

    @allure.story("项目展示")
    @allure.title("项目卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_project_card_display(self) -> None:
        """验证项目卡片正常展示"""
        self.page_obj.open()
        count = self.page_obj.get_project_count()
        assert count > 0, "未找到项目卡片"

    # ==================== 项目交互测试 ===================

    @allure.story("项目交互")
    @allure.title("项目点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_project_click(self) -> None:
        """点击项目卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_project()

    @allure.story("项目交互")
    @allure.title("项目详情信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_project_detail_info(self) -> None:
        """验证项目详情页URL包含keyProject/detail"""
        self.page_obj.open()
        if self.page_obj.is_mobile():
            pytest.skip("移动端点击项目可能不弹出新页面")
        card = self.page_obj.page.locator(self.page_obj.PROJECT_CARD).first
        if card.is_visible():
            result_page = click_and_wait_for_new_page(self.page_obj.page, card)
            assert "keyProject/detail" in result_page.url, \
                f"URL未包含keyProject/detail，当前URL: {result_page.url}"
            result_page.close()

    # ==================== 查看全部 ===================

    @allure.story("查看全部")
    @allure.title("点击查看全部项目")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_projects(self) -> None:
        """点击查看全部按钮跳转到项目列表页"""
        self.page_obj.open()
        self.page_obj.click_view_all()

    # ==================== 发布操作测试 ===================

    @allure.story("发布操作")
    @allure.title("发布项目按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_publish_project(self) -> None:
        """点击发布项目按钮"""
        self.page_obj.open()
        self.page_obj.click_publish_project()
        self.page_obj.take_screenshot("publish_project", "info")

    @allure.story("发布操作")
    @allure.title("发布需求按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_publish_demand(self) -> None:
        """点击发布需求按钮"""
        self.page_obj.open()
        self.page_obj.click_publish_demand()
        self.page_obj.take_screenshot("publish_demand", "info")

    # ==================== 分类筛选测试 ===================

    @allure.story("分类筛选")
    @allure.title("房建项目筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_房建项目(self) -> None:
        """筛选房建项目"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("房建项目")
        self.page_obj.take_screenshot("filter_房建项目", "info")

    @allure.story("分类筛选")
    @allure.title("市政项目筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_市政项目(self) -> None:
        """筛选市政项目"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("市政项目")
        self.page_obj.take_screenshot("filter_市政项目", "info")

    @allure.story("分类筛选")
    @allure.title("其他项目筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_其他项目(self) -> None:
        """筛选其他项目"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("其他项目")
        self.page_obj.take_screenshot("filter_其他项目", "info")

    @allure.story("筛选+分页")
    @allure.title("筛选后翻页列表变化")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_then_pagination(self) -> None:
        """先按分类筛选，再翻到第 2 页：列表应变内容且激活页为 2"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("房建项目")
        pages = self.page_obj.get_pagination_pages()
        if "2" not in pages:
            pytest.skip(f"筛选后仅 {pages} 页，无第 2 页可翻")
        titles_p1 = self.page_obj.get_list_titles()
        assert titles_p1, "筛选后第 1 页列表为空"
        assert self.page_obj.click_pagination_page("2"), "筛选后点击第 2 页失败"
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        # 列表刷新为异步：轮询等待内容变化，避免读到翻页前的旧列表
        titles_p2 = titles_p1
        for _ in range(20):
            try:
                titles_p2 = self.page_obj.get_list_titles()
            except Exception:
                titles_p2 = []
            if titles_p2 and titles_p2 != titles_p1:
                break
            self.page_obj.page.wait_for_timeout(200)

        active = self.page_obj.get_active_pagination_page()
        assert active == "2", f"筛选后翻页激活页应为 2，实际为 {active!r}"
        assert titles_p2, "筛选后第 2 页列表为空"
        assert titles_p1 != titles_p2, "筛选后翻页列表未变化（分页未生效）"

    # ==================== 分页测试 ===================

    @allure.story("分页")
    @allure.title("分页跳转")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_jump(self) -> None:
        """测试分页跳转功能"""
        self.page_obj.open()
        self.page_obj.jump_to_page(2)
        self.page_obj.take_screenshot("pagination", "info")

    @allure.story("分页")
    @allure.title("分页页码展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_pages_display(self) -> None:
        """分页组件应展示页码且默认选中第 1 页"""
        self.page_obj.open()
        pages_loc = self.page_obj.page.locator(".ant-pagination-item, .el-pager li, [class*='pagination'] a, [class*='pagination'] li")
        try:
            pages_loc.first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass
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
        pages_loc = self.page_obj.page.locator(".ant-pagination-item, .el-pager li, [class*='pagination'] a, [class*='pagination'] li")
        try:
            pages_loc.first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass
        pages = self.page_obj.get_pagination_pages()
        if "2" not in pages:
            pytest.skip(f"当前项目数据仅 {pages} 页，无第 2 页可翻")
        titles_p1 = self.page_obj.get_list_titles()
        assert titles_p1, "第 1 页项目列表为空"

        assert self.page_obj.click_pagination_page("2"), "点击第 2 页失败"
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass

        active = self.page_obj.get_active_pagination_page()
        assert active == "2", f"翻页后激活页应为 2，实际为 {active!r}"
        titles_p2 = self.page_obj.get_list_titles()
        assert titles_p2, "第 2 页项目列表为空"
        assert titles_p1 != titles_p2, "翻页后项目列表内容未变化（分页未生效）"
        self.page_obj.take_screenshot("pagination_page2", "info")

    @allure.story("分页")
    @allure.title("返回第一页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_back_to_first(self) -> None:
        """翻到第 2 页后可点击返回第 1 页"""
        self.page_obj.open()
        pages_loc = self.page_obj.page.locator(".ant-pagination-item, .el-pager li, [class*='pagination'] a, [class*='pagination'] li")
        try:
            pages_loc.first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass
        pages = self.page_obj.get_pagination_pages()
        if "2" not in pages:
            pytest.skip(f"当前项目数据仅 {pages} 页，无第 2 页可翻")
        assert self.page_obj.click_pagination_page("2"), "点击第 2 页失败"
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
        assert self.page_obj.click_pagination_page("1"), "点击第 1 页失败"
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
        active = self.page_obj.get_active_pagination_page()
        assert active == "1", f"返回后激活页应为 1，实际为 {active!r}"
