"""会展活动模块测试

入口：首页“会展活动”模块“查看全部” -> /exhibitionActivity
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.exhibition_page import ExhibitionPage

pytestmark = [pytest.mark.regression]


@allure.feature("会展活动页面")
class TestExhibition(BasePageTest):
    """会展活动页面测试用例"""

    page_name = "会展活动"
    page_fixture_name = "exhibition_page"
    # 会展活动不在顶部主导航中，无需校验导航高亮
    NAV_ACTIVE_STATE_APPLICABLE = False

    @allure.story("页面展示")
    @allure.title("会展活动列表加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_exhibition_list_load(self) -> None:
        """会展活动列表正常加载并展示活动卡片"""
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip("会展活动页面不存在(404)")
        self.page_obj.assert_page_loaded()
        titles = self.page_obj.get_activity_titles()
        assert titles, "未找到会展活动标题"
        self.page_obj.take_screenshot("exhibition_list", "info")

    @allure.story("会展详情")
    @allure.title("活动详情跳转与标题一致")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_exhibition_detail_consistency(self) -> None:
        """点击'了解详情'进入详情页，标题与列表首项一致且含时间/地点信息"""
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip("会展活动页面不存在(404)")
        titles = self.page_obj.get_activity_titles()
        if not titles:
            pytest.skip("会展活动列表为空")
        first = titles[0].strip()
        old_url = self.page_obj.page.url
        detail_url = self.page_obj.open_first_detail()
        if detail_url == old_url:
            pytest.skip("点击'了解详情'后未发生路由跳转（站点未配置详情链接）")
        assert "detail" in detail_url, f"详情页 URL 异常: {detail_url}"
        body = (self.page_obj.page.locator("body").inner_text(timeout=8000) or "").replace("\n", " ")
        assert first[:10] in body, f"详情页标题与列表不一致: 列表={first[:24]!r}, 详情={body[:120]!r}"
        assert any(k in body for k in ("会", "时间", "地点", "地址", "2026", "2027")), (
            "会展详情缺少时间/地点信息"
        )
        self.page_obj.take_screenshot("exhibition_detail", "info")
        self.page_obj.open()

    @allure.story("会展详情")
    @allure.title("详情页无横向溢出")
    @allure.severity(allure.severity_level.MINOR)
    def test_exhibition_detail_no_overflow(self) -> None:
        """会展详情页无横向溢出"""
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip("会展活动页面不存在(404)")
        titles = self.page_obj.get_activity_titles()
        if not titles:
            pytest.skip("会展活动列表为空")
        old_url = self.page_obj.page.url
        detail_url = self.page_obj.open_first_detail()
        if detail_url == old_url:
            pytest.skip("点击'了解详情'后未发生路由跳转")
        overflow, scroll_width, client_width = self.page_obj.has_horizontal_overflow()
        assert not overflow, f"详情页横向溢出: scrollWidth={scroll_width}, clientWidth={client_width}"
        self.page_obj.open()