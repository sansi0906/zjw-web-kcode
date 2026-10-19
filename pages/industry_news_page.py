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

    # Tab 切换
    TAB_行业动态 = "text=行业动态"
    TAB_政策资讯 = "text=政策资讯"
    TAB_政策解读 = "text=政策解读"

    # 分页
    PAGINATION_INPUT = "input[type='text']"

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
        # WEB 端：滚动页面寻找产业新闻区域
        try:
            self.assert_text_visible("产业新闻", partial=True)
            return
        except AssertionError:
            pass
        for _ in range(6):
            self.page.evaluate("window.scrollBy(0, 400)")
            self.page.wait_for_timeout(500)
            try:
                self.assert_text_visible("产业新闻", partial=True)
                return
            except AssertionError:
                continue
        # 最后兜底：检查新闻卡片是否存在
        count = self.get_news_count()
        assert count > 0, "未找到产业新闻区域或新闻卡片"

    def get_nav_texts(self) -> list[str]:
        """获取所有导航链接文本"""
        if self.is_mobile():
            try:
                js_texts = self.page.evaluate("""() => {
                    const sel = 'a, button, [role="button"]';
                    const els = Array.from(document.querySelectorAll(sel));
                    const texts = [];
                    els.forEach(el => {
                        const t = (el.textContent || '').trim();
                        if (t && !texts.includes(t)) texts.push(t);
                    });
                    return texts;
                }""")
                if js_texts:
                    return js_texts
            except Exception:
                pass
        navs = self.page.locator(".nav-left a, .header-title a, header a, nav a, .nav-item a")
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接"""
        # 移动端导航项可能是 button 或 a，优先点击可见元素
        for sel in [f"button:has-text('{nav_text}')", f"text={nav_text}", f"a:has-text('{nav_text}')"]:
            try:
                nav = self.page.locator(sel).first
                if nav.is_visible(timeout=1500):
                    nav.click()
                    self.wait_for_load()
                    return
            except Exception:
                continue
        # 最后兜底：JS 点击不可见元素
        try:
            self.page.evaluate(
                """(text) => {
                const els = Array.from(document.querySelectorAll('a, button, [role="button"]'));
                const el = els.find(e => (e.textContent||'').trim() === text);
                if (el) { el.click(); return true; }
                return false;
                }""",
                nav_text,
            )
            self.page.wait_for_timeout(1500)
            self.wait_for_load()
            return
        except Exception:
            pass

    # ==================== Tab 操作 ====================

    def click_tab(self, tab_name: str) -> None:
        """点击Tab切换"""
        tab_map = {
            "行业动态": self.TAB_行业动态,
            "政策资讯": self.TAB_政策资讯,
            "政策解读": self.TAB_政策解读,
        }
        sel = tab_map.get(tab_name)
        if sel:
            el = self.page.locator(sel).first
            if el.is_visible():
                el.click()
                self.page.wait_for_timeout(1000)

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
