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

    # ==================== 分类标签 ====================
    FILTER_TABS = {
        "行业动态": "button:has-text('行业动态')",
        "政策资讯": "button:has-text('政策资讯')",
        "政策解读": "button:has-text('政策解读')",
    }
    # 移动端新闻卡片选择器
    NEWS_CARDS_MOBILE = (
        "div[class*='news'], article, div[class*='card'], "
        "[class*='news-card'], .n-carousel__slide, button"
    )
    NEWS_TITLE = "h3, h2, .title"

    # Tab 切换
    TAB_行业动态 = "text=行业动态"
    TAB_政策资讯 = "text=政策资讯"
    TAB_政策解读 = "text=政策解读"
    TAB_MAP = {
        "行业动态": TAB_行业动态,
        "政策资讯": TAB_政策资讯,
        "政策解读": TAB_政策解读,
    }

    # 分页
    PAGINATION_INPUT = "input[type='text']"

    def open(self) -> IndustryNewsPage:
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def get_news_count(self) -> int:
        """获取新闻卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.NEWS_CARDS_MOBILE).count()
        return self.page.locator(self.NEWS_CARDS).count()

    def get_news_titles(self) -> list[str]:
        """获取新闻标题（容错：结构/渲染时序可能变化）

        产业新闻列表通常使用 <article> 渲染，每条包含标题 + 简介 + 日期。
        """
        try:
            self.page.locator("article, [class*='news'] h2, [class*='news'] h3, h2, h3").first.wait_for(
                state="attached", timeout=4000
            )
        except Exception:
            pass

        titles = []
        try:
            cards = self.page.locator("article")
            count = cards.count()
            for i in range(min(count, 30)):
                try:
                    el = cards.nth(i)
                    if not el.is_visible(timeout=300):
                        continue
                    text = (el.text_content(timeout=1500) or "").strip()
                except Exception:
                    continue
                if text:
                    titles.append(text.replace("\n", " ")[:60])
        except Exception:
            pass
        if titles:
            return titles

        for sel in ["h2", "h3", ".title", "[class*='title']"]:
            try:
                loc = self.page.locator(sel)
                count = loc.count()
                if count == 0:
                    continue
                out = []
                for i in range(min(count, 30)):
                    try:
                        el = loc.nth(i)
                        if not el.is_visible(timeout=300):
                            continue
                        text = (el.text_content(timeout=1500) or "").strip()
                    except Exception:
                        continue
                    if text:
                        out.append(text.replace("\n", " ")[:60])
                if out:
                    return out
            except Exception:
                continue
        return titles

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（供筛选/分页断言使用）"""
        return self.get_news_titles()

    def click_tab(self, tab_name: str) -> None:
        """点击分类标签"""
        selector = self.FILTER_TABS.get(tab_name, self.TAB_MAP.get(tab_name, f"text={tab_name}"))
        el = self.page.locator(selector).first
        if el.is_visible(timeout=3000):
            el.click()
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=3000)
                except Exception:
                    pass

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选生效（列表非空，且切换后内容变化）"""
        self.assert_filter_effective(filter_name)

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
        # WEB 端：滚动页面寻找产业新闻区域
        try:
            self.assert_text_visible("产业新闻", partial=True)
            return
        except AssertionError:
            pass
        for _ in range(6):
            self.page.evaluate("window.scrollBy(0, 400)")
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=1500)
            except Exception:
                pass
            try:
                self.assert_text_visible("产业新闻", partial=True)
                return
            except AssertionError:
                continue
        # 最后兜底：检查新闻卡片是否存在
        count = self.get_news_count()
        assert count > 0, "未找到产业新闻区域或新闻卡片"

    # ==================== 分页操作 ====================

    def jump_to_page(self, page_num: int) -> None:
        """跳转到指定页"""
        try:
            inp = self.page.locator(self.PAGINATION_INPUT).first
            if inp.is_visible():
                inp.fill(str(page_num))
                inp.press("Enter")
                self.wait_for_load()
        except Exception:
            pass
