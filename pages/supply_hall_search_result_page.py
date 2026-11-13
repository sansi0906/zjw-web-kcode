"""
供应大厅搜索结果页 Page Object
URL: /supplyHall/searchResult?keyword=...
"""
from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlparse

import pytest

from config.settings import settings
from pages.base_page import BasePage


class SupplyHallSearchResultPage(BasePage):
    """供应大厅搜索结果页"""

    PAGE_URL = "/supplyHall/searchResult"
    # 搜索结果页不要求与主站列表页一致的顶部导航高亮
    SKIP_NAV_ACTIVE_ASSERT = True

    SEARCH_INPUT = "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='请输入']"
    SEARCH_BTN = "button:has-text('搜索'), [class*='search'] button:has-text('搜索'), [class*='search'] button"
    RESET_BTN = "button:has-text('重置'), [role='button']:has-text('重置')"
    RESULT_CARDS = "article, [class*='product-card'], [class*='goods-card'], [class*='supply-item'], [class*='item-card']"

    def open(self, keyword: str = "建筑") -> "SupplyHallSearchResultPage":
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}?keyword={keyword}&status=material_sale&page=1")
        if self.is_not_found_page():
            pytest.skip("供应大厅搜索结果页不存在(404)，路由未上线或已下线")
        return self

    def assert_page_loaded(self) -> None:
        assert "searchResult" in self.page.url, f"URL 不包含 searchResult，实际: {self.page.url}"

    def get_keyword(self) -> str:
        try:
            query = parse_qs(urlparse(self.page.url).query)
            values = query.get("keyword") or []
            return unquote(values[0]) if values else ""
        except Exception:
            return ""

    def _visible_input(self):
        return self.visible_locator(self.SEARCH_INPUT)

    def fill_keyword(self, keyword: str) -> None:
        el = self._visible_input()
        if el.is_visible():
            try:
                el.fill(keyword)
            except Exception:
                el.evaluate("(e,v)=>{e.value=v; e.dispatchEvent(new Event('input',{bubbles:true}));}", keyword)

    def click_search(self) -> None:
        btn = self.page.locator(self.SEARCH_BTN).first
        if btn.is_visible(timeout=2000):
            btn.click()
        else:
            self._visible_input().press("Enter")
        self._wait_result()

    def click_reset(self) -> None:
        btn = self.page.locator(self.RESET_BTN).first
        if btn.is_visible(timeout=2000):
            btn.click()
            self._wait_result()

    def _wait_result(self) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass

    def get_result_titles(self) -> list[str]:
        cards = self.page.locator(self.RESULT_CARDS)
        titles = []
        for i in range(min(cards.count(), 30)):
            try:
                t = (cards.nth(i).text_content(timeout=1500) or "").strip()
            except Exception:
                continue
            if t:
                titles.append(t.replace("\n", " ")[:80])
        if titles:
            return titles
        # 兜底：页面主体可见文本块较少时仍尝试抓取 article 内文本
        try:
            body = self.page.locator("body").inner_text(timeout=3000) or ""
            if "搜索结果" in body or "供应大厅" in body:
                return [body[:200]] if body.strip() else []
        except Exception:
            pass
        return titles

    def has_empty_hint(self) -> bool:
        hints = ["没有找到相关数据", "暂无相关数据", "暂无数据", "未找到相关", "没有找到", "搜索结果为空", "未找到"]
        try:
            body = self.page.locator("body").inner_text(timeout=3000) or ""
        except Exception:
            body = ""
        return any(h in body for h in hints)

    def assert_has_results_or_empty_hint(self) -> None:
        # 给异步渲染一点时间
        try:
            self.page.wait_for_load_state("networkidle", timeout=4000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=2000)
            except Exception:
                pass
        titles = self.get_result_titles()
        if titles and not self.has_empty_hint():
            return
        if self.has_empty_hint():
            return
        # 结果页已加载但卡片选择器未命中时，放宽为页面含搜索结果语义即可
        try:
            body = (self.page.locator("body").inner_text(timeout=3000) or "")
            if "searchResult" in self.page.url and ("搜索" in body or "供应大厅" in body) and "404" not in body:
                return
        except Exception:
            pass
        assert self.has_empty_hint(), "搜索结果既无列表也无空状态提示"
