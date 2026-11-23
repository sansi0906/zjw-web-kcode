"""
产业金融页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class FinancePage(BasePage):
    """产业金融页面"""

    PAGE_URL = "/finance"

    # 顶部导航
    NAV_ITEMS = ".header-title a, .nav-cneter a, header a, nav a, .nav a"
    NAV_HOME = "text=首页"
    NAV_FINANCE = "text=产业金融"

    # 金融卡片
    FINANCE_CARD = ".finance-card"
    FINANCE_CARD_TITLE = "h3, h2, .title, [class*='title']"
    FINANCE_CARD_DESC = "p, .desc, [class*='desc']"
    FINANCE_CARD_BUTTON = "button"

    # H5：移动 UA 访问 /finance 会被前端重定向到 /financeProductType 产品列表页
    H5_FINANCE_PAGE_FRAGMENT = "financeProductType"
    H5_FINANCE_ROOT = ".finance-product-type-mobile"
    H5_FINANCE_CARD = ".finance-product-type-mobile div.cursor-pointer:has(h2)"
    H5_FINANCE_VIEW_TEXT = "查看产品"

    # 申报入口按钮
    HERO_BUTTON_APPLY = "text=申请融资"

    # 顶部功能按钮
    TOP_BUTTON_1 = "text=平台支持企业融资"
    TOP_BUTTON_2 = "text=企业融资"
    TOP_BUTTON_3 = "text=查看全部"

    # 悬浮功能区
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # 页脚
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津 initiating"

    def open(self) -> "FinancePage":
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        try:
            self.page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
        return self

    def _is_h5_finance_page(self) -> bool:
        """判断当前是否 H5 产业金融产品列表页（/financeProductType）"""
        if not self.is_mobile():
            return False
        return self.H5_FINANCE_PAGE_FRAGMENT in (self.page.url or "")

    def _h5_card_locator(self):
        return self.page.locator(self.H5_FINANCE_CARD)

    def get_finance_count(self) -> int:
        try:
            if self._is_h5_finance_page():
                return self._h5_card_locator().count()
            return self.page.evaluate("document.querySelectorAll('.finance-card').length")
        except Exception:
            return 0

    def get_finance_titles(self) -> list[str]:
        try:
            if self._is_h5_finance_page():
                texts = self.page.evaluate(
                    """() => Array.from(document.querySelectorAll('.finance-product-type-mobile div.cursor-pointer'))
                        .map(e => { const h = e.querySelector('h2'); return h ? (h.textContent||'').trim().slice(0,50) : ''; })
                        .filter(t => t)"""
                )
                return texts
            texts = self.page.evaluate(
                """() => Array.from(document.querySelectorAll('.finance-card'))
                    .map(e => (e.textContent||'').trim().slice(0,50))
                    .filter(t => t)"""
            )
            return texts
        except Exception:
            return []

    def get_finance_card_titles(self) -> list[str]:
        """获取金融卡片标题"""
        try:
            if self._is_h5_finance_page():
                return self.get_finance_titles()
            texts = self.page.evaluate(
                """() => Array.from(document.querySelectorAll('.finance-card h3, .finance-card h2, .finance-card .title, .finance-card [class*="title"]'))
                    .map(e => (e.textContent||'').trim().slice(0,50))
                    .filter(t => t)"""
            )
            return texts
        except Exception:
            return []

    def assert_finance_exists(self, min_count: int = 1) -> None:
        count = self.get_finance_count()
        if count < min_count:
            try:
                self.page.evaluate("window.scrollTo(0, window.innerHeight)")
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=2000)
                except Exception:
                    pass
                count = self.get_finance_count()
            except Exception:
                pass
        assert count >= min_count, f"期望金融卡片数量 >= {min_count}，实际为 {count}"

    def click_first_finance(self) -> None:
        if self._is_h5_finance_page():
            card = self._h5_card_locator().first
        else:
            card = self.page.locator(self.FINANCE_CARD).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                card.evaluate("el => el.click()")
            self.wait_for_load()

    def click_hero_apply(self) -> None:
        btn = self.page.locator(self.HERO_BUTTON_APPLY).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    def click_top_button(self, text: str) -> None:
        btn = self.page.locator(f"button:has-text('{text}')").first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    def click_view_all(self) -> None:
        btn = self.page.locator(self.TOP_BUTTON_3).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    def assert_page_loaded(self) -> None:
        if self.is_mobile():
            assert "finance" in self.page.url, f"URL 不包含 finance，实际: {self.page.url}"
            return
        self.assert_text_visible("产业金融", partial=True)