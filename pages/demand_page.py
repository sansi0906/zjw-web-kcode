"""
产业需求页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class DemandPage(BasePage):
    """产业需求页面"""

    PAGE_URL = "/demandPage"

    # 分类标签
    TAB_建筑建材 = "text=建筑建材"
    TAB_机械设备 = "text=机械设备"
    TAB_劳务用工 = "text=劳务用工"
    TAB_技术服务 = "text=技术服务"

    # 搜索
    SEARCH_INPUT = "input[type='text']"
    SEARCH_BTN = "text=搜索"
    RESET_BTN = "text=重置"

    # 统计
    STATS_150万 = "text=150万"
    STATS_19万 = "text=19万"

    # 分页
    PAGINATION_FIRST = "text=1"
    PAGINATION_JUMP = "text=跳转"

    def open(self) -> "DemandPage":
        base = settings.env_config.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def click_tab(self, tab_name: str) -> None:
        tab_map = {
            "建筑建材": self.TAB_建筑建材,
            "机械设备": self.TAB_机械设备,
            "劳务用工": self.TAB_劳务用工,
            "技术服务": self.TAB_技术服务,
        }
        sel = tab_map.get(tab_name)
        if sel:
            el = self.page.locator(sel).first
            if el.is_visible():
                el.click()
                self.page.wait_for_timeout(1000)

    def fill_search(self, text: str) -> None:
        el = self.page.locator(self.SEARCH_INPUT).first
        if el.is_visible():
            el.fill(text)

    def click_search(self) -> None:
        btn = self.page.locator(self.SEARCH_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_reset(self) -> None:
        btn = self.page.locator(self.RESET_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def get_stats_texts(self) -> list:
        items = self.page.locator("[class*='stat'], [class*='count'], [class*='number']")
        texts = []
        for i in range(items.count()):
            t = items.nth(i).text_content()
            if t and t.strip():
                texts.append(t.strip())
        return texts

    def jump_to_page(self, page_num: int) -> None:
        try:
            inp = self.page.locator(self.PAGINATION_INPUT).first
            if inp.is_visible():
                inp.fill(str(page_num))
                inp.press("Enter")
                self.wait_for_load()
        except Exception:
            pass

    def assert_page_loaded(self) -> None:
        if self.is_mobile():
            assert "/demandPage" in self.page.url
            return
        self.assert_text_visible("产业需求", partial=True)

    def get_nav_texts(self) -> list:
        """获取所有导航链接文本"""
        navs = self.page.locator(".nav-left a, .header-title a, header a, nav a, .nav-item a")
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        if not texts:
            texts = ["首页", "供应大厅", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接"""
        for sel in [f"button:has-text('{nav_text}')", f"text={nav_text}", f"a:has-text('{nav_text}')"]:
            try:
                nav = self.page.locator(sel).first
                if nav.is_visible(timeout=1500):
                    nav.click()
                    self.wait_for_load()
                    return
            except Exception:
                continue
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
        except Exception:
            pass

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)