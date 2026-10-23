"""
产业政策页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IndustryPolicyPage(BasePage):
    PAGE_URL = "/industryPolicy"
    """产业政策页面"""

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

    # ==================== 政策分类筛选 ====================
    # 分类 tab 使用 .nav-item 精确定位（页面上的"全部/推荐"并不存在，属于历史遗留用例）
    FILTER_TABS = {
        "政策资讯": ".nav-item:has-text('政策资讯')",
        "政策解读": ".nav-item:has-text('政策解读')",
        "行业动态": ".nav-item:has-text('行业动态')",
    }
    FILTER_政策资讯 = ".nav-item:has-text('政策资讯')"
    FILTER_政策解读 = ".nav-item:has-text('政策解读')"
    FILTER_行业动态 = ".nav-item:has-text('行业动态')"

    # ==================== 政策文章 ====================
    POLICY_CARD = "[class*='policy'], [class*='article'], [class*='news'], article, .n-card"
    # 条目标题（内容区主标题），排除简介与日期
    POLICY_TITLE = (
        ".industry-policy-content div[class*='text-[#1D2129]'][class*='font-medium']"
    )
    POLICY_TITLE_FALLBACK = "h3, h2, .title, .name"
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

    def open(self) -> "IndustryPolicyPage":
        """打开产业政策页面"""
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator(self.VIEW_ALL_BTN).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 导航操作 ====================

    # ==================== 政策筛选操作 ====================

    def click_filter(self, filter_name: str) -> None:
        """点击政策分类筛选"""
        selector = self.FILTER_TABS.get(filter_name, f"text={filter_name}")
        filter_btn = self.page.locator(selector).first
        if filter_btn.is_visible():
            filter_btn.click()
            self.page.wait_for_timeout(1000)

    def get_active_filter(self) -> str:
        """获取当前选中的筛选分类"""
        for filter_name, selector in [
            ("政策资讯", self.FILTER_政策资讯),
            ("政策解读", self.FILTER_政策解读),
            ("行业动态", self.FILTER_行业动态),
        ]:
            el = self.page.locator(selector).first
            if el.is_visible():
                cls = el.get_attribute("class") or ""
                if "active" in cls or "#1653FF" in cls or "blue" in cls:
                    return filter_name
        return ""

    def get_policy_count(self) -> int:
        """获取政策文章数量"""
        return self.page.locator(self.POLICY_CARD).count()

    def get_policy_titles(self) -> list[str]:
        """获取所有政策文章标题

        政策内容区的条目标题类名为 `text-[#1D2129] text-[24px] font-medium`，
        简介类名为 `content-item-title`，需排除简介与日期。
        """
        titles = []
        loc = self.page.locator(self.POLICY_TITLE)
        for i in range(loc.count()):
            el = loc.nth(i)
            if not el.is_visible():
                continue
            text = (el.text_content() or "").strip()
            if text:
                titles.append(text.replace("\n", " ")[:60])
        if not titles:
            loc = self.page.locator(self.POLICY_TITLE_FALLBACK)
            for i in range(loc.count()):
                el = loc.nth(i)
                if not el.is_visible():
                    continue
                text = (el.text_content() or "").strip()
                if text:
                    titles.append(text.replace("\n", " ")[:60])
        if titles:
            return titles
        cards = self.page.locator(self.POLICY_CARD)
        for i in range(cards.count()):
            text = (cards.nth(i).text_content() or "").strip()
            if text:
                titles.append(text.replace("\n", " ")[:60])
        return titles

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（供筛选/分页断言使用）"""
        return self.get_policy_titles()

    def click_first_policy(self) -> None:
        """点击第一篇政策文章"""
        card = self.page.locator(self.POLICY_CARD).first
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
        self.assert_text_visible("产业政策", partial=True)

    def assert_policies_exist(self, min_count: int = 1) -> None:
        """断言政策文章存在"""
        count = self.get_policy_count()
        assert count >= min_count, f"期望政策数量 >= {min_count}，实际为 {count}"

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选生效（列表非空，且切换后内容变化）"""
        self.assert_filter_effective(filter_name)
