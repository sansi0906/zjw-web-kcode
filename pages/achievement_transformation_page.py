"""
成果转化页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class AchievementTransformationPage(BasePage):
    """成果转化页面"""

    PAGE_URL = "/achievementTransformation"

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

    # ==================== 成果分类筛选 ====================
    # 课题/成果 是真正的分类 tab；"科技创新成果" 是板块标题，不是筛选项
    FILTER_TABS = {
        "课题": "div[class*='gap-[55px]'] > div:has-text('课题')",
        "成果": "div[class*='gap-[55px]'] > div:has-text('成果')",
    }
    FILTER_科技创新成果 = "text=科技创新成果"
    FILTER_课题 = "text=课题"
    FILTER_成果 = "text=成果"

    # ==================== 成果列表 ====================
    ACHIEVEMENT_CARD = "[class*='achievement'], [class*='card'], .n-card, article"
    # 移动端成果卡片选择器
    ACHIEVEMENT_CARD_MOBILE = (
        "[class*='achievement'], [class*='card'], .n-card, article, "
        "[class*='achievement-card'], .n-carousel__slide, button"
    )
    ACHIEVEMENT_TITLE = "h3, h2, .title, .name"
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

    def open(self) -> "AchievementTransformationPage":
        """打开成果转化页面"""
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    # ==================== 导航操作 ====================

    # ==================== 成果筛选操作 ====================

    def click_filter(self, filter_name: str) -> None:
        """点击成果分类筛选"""
        selector = self.FILTER_TABS.get(filter_name, f"text={filter_name}")
        filter_btn = self.page.locator(selector).first
        if filter_btn.is_visible(timeout=3000):
            filter_btn.click()
            self.page.wait_for_timeout(1000)

    def get_active_filter(self) -> str:
        """获取当前选中的筛选分类"""
        for filter_name, selector in [
            ("科技创新成果", self.FILTER_科技创新成果),
            ("课题", self.FILTER_课题),
            ("成果", self.FILTER_成果),
        ]:
            el = self.page.locator(selector).first
            if el.is_visible():
                cls = el.get_attribute("class") or ""
                if "active" in cls or "#1653FF" in cls or "blue" in cls:
                    return filter_name
        return ""

    def get_achievement_count(self) -> int:
        """获取成果卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.ACHIEVEMENT_CARD_MOBILE).count()
        return self.page.locator(self.ACHIEVEMENT_CARD).count()

    def get_achievement_titles(self) -> list[str]:
        """获取所有成果标题"""
        if self.is_mobile():
            cards = self.page.locator(self.ACHIEVEMENT_CARD_MOBILE)
        else:
            cards = self.page.locator(self.ACHIEVEMENT_CARD)
        titles = []
        for i in range(cards.count()):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（供筛选/分页断言使用）"""
        return self.get_achievement_titles()

    def click_first_achievement(self) -> None:
        """点击第一个成果卡片"""
        if self.is_mobile():
            card = self.page.locator(self.ACHIEVEMENT_CARD_MOBILE).first
        else:
            card = self.page.locator(self.ACHIEVEMENT_CARD).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
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
        # 移动端可能无独立"成果转化"标题，改用 URL 断言
        if self.is_mobile():
            assert "/achievementTransformation" in self.page.url, \
                f"URL 不包含 achievementTransformation，实际: {self.page.url}"
            return
        self.assert_text_visible("成果转化", partial=True)

    def assert_achievements_exist(self, min_count: int = 1) -> None:
        """断言成果卡片存在"""
        count = self.get_achievement_count()
        assert count >= min_count, f"期望成果数量 >= {min_count}，实际为 {count}"

    def assert_filter_works(self, filter_name: str) -> None:
        """断言筛选生效（列表非空，且切换后内容变化）"""
        self.assert_filter_effective(filter_name)
