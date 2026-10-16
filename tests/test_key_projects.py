"""重点项目模块测试"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.key_project_page import KeyProjectsPage
from utils.browser_helpers import click_and_wait_for_new_page


@allure.feature("重点项目页面")
class TestKeyProjects(BasePageTest):
    """重点项目测试类"""

    page_name = "重点项目"
    page_fixture_name = "key_project_page"

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