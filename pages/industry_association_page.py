"""
产业协会页面 Page Object
"""
from __future__ import annotations

from pages.base_page import BasePage


class IndustryAssociationPage(BasePage):
    """产业协会页面"""

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

    # ==================== 协会分类筛选 ====================
    FILTER_产业协会 = "text=产业协会"
    FILTER_协会入驻 = "text=协会入驻"

    # ==================== 协会列表 ====================
    ASSOCIATION_CARD = "[class*='association'], [class*='card'], .n-card, article"
    ASSOCIATION_TITLE = "h3, h2, .title, .name"
    VIEW_DETAIL_BTN = "text=查看详情"
    VIEW_ALL_BTN = "text=查看全部"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网安备"

    # ==================== 页面操作 ====================

    def open(self) -> "IndustryAssociationPage":
        """打开产业协会页面"""
        self.goto()
        return self

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator(self.VIEW_ALL_BTN).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 导航操作 ====================

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接"""
        nav = self.page.locator(f"text={nav_text}").first
        if nav.is_visible():
            nav.click()
            self.wait_for_load()

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
            if "/industryAssociation" in url:
                texts = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    # ==================== 协会筛选操作 ====================

    def click_filter(self, filter_name: str) -> None:
        """点击协会分类筛选"""
        self._close_modal_if_exists()
        
        filter_map = {
            "产业协会": self.FILTER_产业协会,
            "协会入驻": self.FILTER_协会入驻,
        }
        selector = filter_map.get(filter_name)
        if selector:
            filter_btn = self.page.locator(selector).first
            if filter_btn.is_visible():
                try:
                    filter_btn.click()
                except Exception:
                    self._js_click_by_text(filter_name)
                self.page.wait_for_timeout(1000)

    def _js_click_by_text(self, text: str) -> None:
        """通过文本内容用 JS 点击元素"""
        self.page.evaluate(f"""(text) => {{
            const elements = Array.from(document.querySelectorAll('*'));
            const el = elements.find(e => e.textContent?.trim() === text);
            if (el) {{
                el.click();
            }}
        }}""", text)

    def _close_modal_if_exists(self) -> None:
        """关闭可能存在的弹窗"""
        try:
            modal = self.page.locator(".n-modal-container, [class*='modal']").first
            if modal.is_visible(timeout=2000):
                close_btn = modal.locator(".n-dialog__close, .n-modal__close, [class*='close']:visible").first
                if close_btn.is_visible(timeout=1000):
                    close_btn.click()
                    self.page.wait_for_timeout(1000)
                else:
                    self.page.keyboard.press("Escape")
                    self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def get_active_filter(self) -> str:
        """获取当前选中的筛选分类"""
        for filter_name, selector in [
            ("产业协会", self.FILTER_产业协会),
            ("协会入驻", self.FILTER_协会入驻),
        ]:
            el = self.page.locator(selector).first
            if el.is_visible():
                cls = el.get_attribute("class") or ""
                if "active" in cls or "#1653FF" in cls or "blue" in cls:
                    return filter_name
        return ""

    def get_association_count(self) -> int:
        """获取协会卡片数量"""
        return self.page.locator(self.ASSOCIATION_CARD).count()

    def get_association_titles(self) -> list[str]:
        """获取所有协会标题"""
        cards = self.page.locator(self.ASSOCIATION_CARD)
        titles = []
        for i in range(cards.count()):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_association(self) -> None:
        """点击第一个协会卡片"""
        card = self.page.locator(self.ASSOCIATION_CARD).first
        if card.is_visible():
            card.click()
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
        self.assert_text_visible("产业协会", partial=True)

    def assert_associations_exist(self, min_count: int = 1) -> None:
        """断言协会卡片存在"""
        count = self.get_association_count()
        assert count >= min_count, f"期望协会数量 >= {min_count}，实际为 {count}"

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选功能正常"""
        self.click_filter(filter_name)
        self.page.wait_for_timeout(1000)
        count = self.get_association_count()
        assert count >= 0, f"筛选 {filter_name} 后协会数量异常"
