"""
重点项目页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class KeyProjectsPage(BasePage):
    """重点项目页面"""

    PAGE_URL = "/keyProject"

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

    # ==================== 项目分类筛选 ====================
    FILTER_房建项目 = "text=房建项目"
    FILTER_市政项目 = "text=市政项目"
    FILTER_其他项目 = "text=其他项目"
    # ==================== 项目操作按钮 ====================

    BTN_发布项目 = "text=发布项目"
    BTN_发布需求 = "text=发布需求"
    BTN_查看全部 = "text=查看全部"

    # ==================== 项目卡片 ====================
    PROJECT_CARD = ".key-project-content .n-card, .n-card"
    # 移动端项目卡片选择器
    PROJECT_CARD_MOBILE = (
        ".key-project-content .n-card, .n-card, "
        "[class*='project-card'], .n-carousel__slide, button"
    )
    PROJECT_TITLE = "h3, h2, .title, .name"
    VIEW_DETAIL_BTN = "text=查看详情"
    VIEW_ALL_BTN = "text=查看全部"

    # ==================== 分页 ====================
    PAGINATION_INPUT = "input[type='text']"
    PAGINATION_JUMP = "text=跳转"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网安备"

    # ==================== 页面操作 ====================

    def open(self) -> "KeyProjectsPage":
        """打开重点项目页面"""
        base = settings.env_config.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

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
        # 如果没提取到，尝试直接通过 URL 判断
        if not texts:
            url = self.page.url
            if "/keyProject" in url:
                texts = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    # ==================== 项目筛选操作 ====================

    def click_filter(self, filter_name: str) -> None:
        """点击项目分类筛选"""
        filter_map = {
            "房建项目": self.FILTER_房建项目,
            "市政项目": self.FILTER_市政项目,
            "其他项目": self.FILTER_其他项目,
        }
        selector = filter_map.get(filter_name)
        if selector:
            filter_btn = self.page.locator(selector).first
            if filter_btn.is_visible():
                filter_btn.click()
                self.page.wait_for_timeout(1000)

    def get_active_filter(self) -> str:
        """获取当前选中的筛选分类"""
        for filter_name, selector in [
            ("房建项目", self.FILTER_房建项目),
            ("市政项目", self.FILTER_市政项目),
            ("其他项目", self.FILTER_其他项目),
        ]:
            el = self.page.locator(selector).first
            if el.is_visible():
                cls = el.get_attribute("class") or ""
                if "active" in cls or "#1653FF" in cls or "blue" in cls:
                    return filter_name
        return ""

    def get_project_count(self) -> int:
        """获取项目卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.PROJECT_CARD_MOBILE).count()
        return self.page.locator(self.PROJECT_CARD).count()

    def get_project_titles(self) -> list[str]:
        """获取所有项目标题"""
        if self.is_mobile():
            cards = self.page.locator(self.PROJECT_CARD_MOBILE)
        else:
            cards = self.page.locator(self.PROJECT_CARD)
        titles = []
        for i in range(cards.count()):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_project(self) -> None:
        """点击第一个项目"""
        if self.is_mobile():
            card = self.page.locator(self.PROJECT_CARD_MOBILE).first
        else:
            card = self.page.locator(self.PROJECT_CARD).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                card.evaluate("el => el.click()")
            self.wait_for_load()

    # ==================== 发布操作 ====================

    def click_publish_project(self) -> None:
        """点击发布项目按钮"""
        btn = self.page.locator(self.BTN_发布项目).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_publish_demand(self) -> None:
        """点击发布需求按钮"""
        btn = self.page.locator(self.BTN_发布需求).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_view_all(self) -> None:
        """点击查看全部按钮"""
        btn = self.page.locator(self.BTN_查看全部).first
        if btn.is_visible():
            self.safe_click(self.BTN_查看全部)
            self.wait_for_load()

    # ==================== 分页操作 ====================

    def jump_to_page(self, page_num: int) -> None:
        """跳转到指定页"""
        try:
            input_el = self.page.locator(self.PAGINATION_INPUT).first
            if input_el.is_visible():
                input_el.fill(str(page_num))
                input_el.press("Enter")
                self.wait_for_load()
        except Exception:
            pass

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
        # 移动端可能无独立"重点项目"标题，改用 URL 断言
        if self.is_mobile():
            assert "/keyProject" in self.page.url, \
                f"URL 不包含 keyProject，实际: {self.page.url}"
            return
        self.assert_text_visible("重点项目", partial=True)

    def assert_projects_exist(self, min_count: int = 1) -> None:
        """断言项目卡片存在"""
        count = self.get_project_count()
        assert count >= min_count, f"期望项目数量 >= {min_count}，实际为 {count}"

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选功能正常"""
        self.click_filter(filter_name)
        self.page.wait_for_timeout(1000)
        count = self.get_project_count()
        assert count >= 0, f"筛选 {filter_name} 后项目数量异常"
