"""产业新闻模块测试

入口说明：
- 导航栏"产业政策"链接跳转至 /industryNews（改版后路由）
- 该页面 title 为"产业新闻"
- 首页"产业政策"模块的"查看全部"按钮也跳转至 /industryNews
"""
from __future__ import annotations

import allure

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
        """切换到行业动态Tab"""
        self.page_obj.open()
        self.page_obj.click_tab("行业动态")
        self.page_obj.take_screenshot("tab_行业动态", "info")

    @allure.story("Tab切换")
    @allure.title("政策资讯Tab切换")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_政策资讯(self) -> None:
        """切换到政策资讯Tab"""
        self.page_obj.open()
        self.page_obj.click_tab("政策资讯")
        self.page_obj.take_screenshot("tab_政策资讯", "info")

    @allure.story("Tab切换")
    @allure.title("政策解读Tab切换")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tab_政策解读(self) -> None:
        """切换到政策解读Tab"""
        self.page_obj.open()
        self.page_obj.click_tab("政策解读")
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