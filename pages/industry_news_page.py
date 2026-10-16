"""
产业新闻 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IndustryNewsPage(BasePage):
    """产业新闻页面"""

    PAGE_URL = "/industryNews"

    NEWS_CARDS = "div[class*='news'], article, div[class*='card']"
    # 移动端新闻卡片选择器
    NEWS_CARDS_MOBILE = (
        "div[class*='news'], article, div[class*='card'], "
        "[class*='news-card'], .n-carousel__slide, button"
    )
    NEWS_TITLE = "h3, h2, .title"

    def open(self) -> IndustryNewsPage:
        base = settings.env_config.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def get_news_count(self) -> int:
        """获取新闻卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.NEWS_CARDS_MOBILE).count()
        return self.page.locator(self.NEWS_CARDS).count()

    def click_first_news(self) -> None:
        """点击第一条新闻"""
        if self.is_mobile():
            card = self.page.locator(self.NEWS_CARDS_MOBILE).first
        else:
            card = self.page.locator(self.NEWS_CARDS).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                card.evaluate("el => el.click()")
            self.wait_for_load()

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        if self.is_mobile():
            assert "/industryNews" in self.page.url, \
                f"URL 不包含 industryNews，实际: {self.page.url}"
            return
        self.assert_text_visible("首页", partial=True)
