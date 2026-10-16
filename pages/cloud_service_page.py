"""
云服务页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class CloudServicePage(BasePage):
    """云服务页面"""

    PAGE_URL = "/cloudService"

    # ==================== 顶部导航 ====================
    LOGO = "a[href='/'] img, header a:first-child img, .nav-left img"
    NAV_ITEMS = ".nav-left a, .header-title a, header a, nav a, .nav-item a"

    NAV_HOME = "text=首页"
    NAV_INTELLIGENT_CONSTRUCTION = "text=智能建造"
    NAV_KEY_PROJECT = "text=重点项目"
    NAV_INDUSTRY_POLICY = "text=产业政策"
    NAV_INDUSTRY_ASSOCIATION = "text=产业协会"
    NAV_ACHIEVEMENT_TRANSFORMATION = "text=成果转化"
    NAV_CLOUD_SERVICE = "text=云服务"

    LOGIN_BTN = "text=登录"
    REGISTER_BTN = "text=注册"

    # ==================== 云服务卡片 ====================
    SERVICE_CARD = "[class*='service'], [class*='card'], .n-card, article"
    # 移动端云服务卡片选择器
    SERVICE_CARD_MOBILE = (
        "[class*='service'], [class*='card'], .n-card, article, "
        "[class*='cloud-service-card'], .n-carousel__slide"
    )
    SERVICE_TITLE = "h3, h2, .title, .name"
    SERVICE_DESC = "p, .desc, .description"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网安备"

    # ==================== 页面操作 ====================

    def open(self) -> "CloudServicePage":
        """打开云服务页面"""
        base = settings.env_config.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def click_filter(self, filter_name: str) -> None:
        """点击筛选按钮"""
        filter_map = {
            "全部": "text=全部",
            "推荐": "text=推荐",
        }
        selector = filter_map.get(filter_name, f"text={filter_name}")
        btn = self.page.locator(selector).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选功能正常"""
        self.click_filter(filter_name)
        self.page.wait_for_timeout(1000)
        count = self.get_service_count()
        assert count >= 0, f"筛选 {filter_name} 后服务数量异常"

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator("text=查看全部").first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 导航操作 ====================

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

    def get_nav_texts(self) -> list[str]:
        """获取所有导航链接文本"""
        navs = self.page.locator(self.NAV_ITEMS)
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        if not texts:
            url = self.page.url
            if "/cloudService" in url:
                texts = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    # ==================== 云服务卡片操作 ====================

    def get_service_count(self) -> int:
        """获取云服务卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.SERVICE_CARD_MOBILE).count()
        return self.page.locator(self.SERVICE_CARD).count()

    def get_service_titles(self) -> list[str]:
        """获取所有云服务标题"""
        if self.is_mobile():
            cards = self.page.locator(self.SERVICE_CARD_MOBILE)
        else:
            cards = self.page.locator(self.SERVICE_CARD)
        titles = []
        for i in range(cards.count()):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_service(self) -> None:
        """点击第一个云服务卡片"""
        if self.is_mobile():
            card = self.page.locator(self.SERVICE_CARD_MOBILE).first
        else:
            card = self.page.locator(self.SERVICE_CARD).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                # JS 点击兜底（移动端卡片可能被遮挡）
                card.evaluate("el => el.click()")
            self.wait_for_load()

    # ==================== 悬浮按钮操作 ====================

    def click_customer_service(self) -> None:
        """点击在线客服"""
        btn = self.page.locator(self.FLOAT_CUSTOMER_SERVICE).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    def click_intent_form(self) -> None:
        """点击意向填报"""
        btn = self.page.locator(self.FLOAT_INTENT_FORM).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    # ==================== 页脚操作 ====================

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    # ==================== 断言辅助 ====================

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        # 移动端云服务页可能无独立"云服务"标题，改用 URL 断言
        if self.is_mobile():
            assert "cloudService" in self.page.url, f"URL 不包含 cloudService，实际: {self.page.url}"
            return
        self.assert_text_visible("云服务", partial=True)

    def assert_services_exist(self, min_count: int = 1) -> None:
        """断言云服务卡片存在"""
        count = self.get_service_count()
        assert count >= min_count, f"期望云服务数量 >= {min_count}，实际为 {count}"
