"""
产业需求页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class DemandPage(BasePage):
    """产业需求页面"""

    PAGE_URL = "/demandPage"

    # 分类标签（w-[140px] 的 tab 容器内，避免误匹配页脚同名链接）
    FILTER_TABS = {
        name: f"div[class*='w-[140px]'] span:text-is('{name}')"
        for name in ["建筑建材", "机械设备", "劳务用工", "技术服务"]
    }
    TAB_建筑建材 = FILTER_TABS["建筑建材"]
    TAB_机械设备 = FILTER_TABS["机械设备"]
    TAB_劳务用工 = FILTER_TABS["劳务用工"]
    TAB_技术服务 = FILTER_TABS["技术服务"]

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
        base = settings.base_url.rstrip("/")
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

    def get_demand_titles(self) -> list[str]:
        """获取需求条目标题"""
        cards = self.page.locator("span.line-clamp-2")
        titles = []
        for i in range(cards.count()):
            t = cards.nth(i).text_content()
            if t and t.strip():
                titles.append(t.strip()[:50])
        return titles

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（供筛选/分页断言使用）"""
        return self.get_demand_titles()

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选生效（列表非空，且切换后内容变化）"""
        self.assert_filter_effective(filter_name)

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

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)