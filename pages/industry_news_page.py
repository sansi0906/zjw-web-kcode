"""
产业新闻 Page Object
"""
from __future__ import annotations

from pages.base_page import BasePage


class IndustryNewsPage(BasePage):
    """产业新闻页面"""

    NEWS_CARDS = "div[class*='news'], article, div[class*='card']"
    NEWS_TITLE = "h3, h2, .title"

    def open(self) -> IndustryNewsPage:
        self.goto()
        return self

    def get_news_count(self) -> int:
        """获取新闻卡片数量"""
        return self.page.locator(self.NEWS_CARDS).count()

    def click_first_news(self) -> None:
        """点击第一条新闻"""
        self.page.locator(self.NEWS_CARDS).first.click()
        self.wait_for_load()
