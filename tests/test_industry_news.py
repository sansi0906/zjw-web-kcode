"""产业新闻模块测试

入口说明：
- 导航栏"产业政策"链接跳转至 /industryNews（改版后路由）
- 该页面 title 为"产业新闻"
- 首页"产业政策"模块的"查看全部"按钮也跳转至 /industryNews
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.industry_news_page import IndustryNewsPage
from utils.browser_helpers import click_and_wait_for_new_page


@allure.feature("产业新闻页面")
class TestIndustryNews(BasePageTest):
    """产业新闻测试类"""

    page_name = "产业新闻"
    page_fixture_name = "industry_news_page"

    # ==================== 新闻展示测试 ===================

    @allure.story("新闻展示")
    @allure.title("新闻卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_news_card_display(self) -> None:
        """验证新闻卡片正常展示"""
        self.page_obj.open()
        count = self.page_obj.get_news_count()
        assert count > 0, "未找到新闻卡片"

    @allure.story("新闻展示")
    @allure.title("新闻图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_news_images_load(self) -> None:
        """验证新闻图片正常加载"""
        self.page_obj.open()
        news_images = self.page_obj.page.locator("img")
        if news_images.count() > 0:
            img = news_images.first
            assert img.evaluate("el => el.complete && el.naturalHeight > 0")

    # ==================== 新闻交互测试 ===================

    @allure.story("新闻交互")
    @allure.title("新闻点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_news_click(self) -> None:
        """点击新闻卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_news()

    @allure.story("新闻交互")
    @allure.title("新闻详情内容")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_news_detail_content(self) -> None:
        """验证新闻详情页内容完整"""
        self.page_obj.open()
        news_title = self.page_obj.page.locator(
            "div[class*='card'] h3, div[class*='card'] h4, "
            "div[class*='card'] [class*='title'], div[class*='card'] a"
        ).first
        if news_title.is_visible():
            result_page = click_and_wait_for_new_page(self.page_obj.page, news_title)
            assert len(result_page.content()) > 1000, "新闻内容过短"
            result_page.close()

    # ==================== Tab 切换测试 ===================

    @allure.story("Tab切换")
    @allure.title("行业动态Tab切换")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_行业动态(self) -> None:
        """切换到行业动态Tab，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("行业动态")
        self.page_obj.take_screenshot("tab_行业动态", "info")

    @allure.story("Tab切换")
    @allure.title("政策资讯Tab切换")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_政策资讯(self) -> None:
        """切换到政策资讯Tab，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("政策资讯")
        self.page_obj.take_screenshot("tab_政策资讯", "info")

    @allure.story("Tab切换")
    @allure.title("政策解读Tab切换")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_政策解读(self) -> None:
        """切换到政策解读Tab，校验列表内容随之变化"""
        self.page_obj.open()
        self.page_obj.assert_filter_works("政策解读")
        self.page_obj.take_screenshot("tab_政策解读", "info")

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
            pytest.skip(f"当前新闻数据仅 {pages} 页，无第 2 页可翻")
        titles_p1 = self.page_obj.get_list_titles()
        assert titles_p1, "第 1 页新闻列表为空"

        assert self.page_obj.click_pagination_page("2"), "点击第 2 页失败"
        self.page_obj.page.wait_for_timeout(1500)

        active = self.page_obj.get_active_pagination_page()
        assert active == "2", f"翻页后激活页应为 2，实际为 {active!r}"
        titles_p2 = self.page_obj.get_list_titles()
        assert titles_p2, "第 2 页新闻列表为空"
        assert titles_p1 != titles_p2, "翻页后新闻列表内容未变化（分页未生效）"
        self.page_obj.take_screenshot("news_pagination_page2", "info")
