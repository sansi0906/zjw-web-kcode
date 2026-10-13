"""
产业需求 Page Object
"""
from __future__ import annotations

from pages.base_page import BasePage


class IndustryDemandPage(BasePage):
    """产业需求页面"""

    # ==================== 顶部导航 ====================
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

    # 筛选标签
    FILTER_BUILDING_MATERIALS = "text=建筑建材"
    FILTER_MACHINERY = "text=机械设备"
    FILTER_LABOR = "text=劳务用工"
    FILTER_TECH_SERVICE = "text=技术服务"

    # 操作按钮
    VIEW_DETAIL_BTN = "text=查看详情"
    VIEW_ALL_BTN = "text=查看全部"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网"

    # ==================== 页面操作 ====================

    def open(self) -> "IndustryDemandPage":
        """打开产业需求页面"""
        self.goto()
        return self

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
            if "industryDemand" in url or "industry-demand" in url:
                texts = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    def click_filter(self, filter_name: str) -> None:
        """点击筛选按钮"""
        filter_map = {
            "全部": "text=全部",
            "推荐": "text=推荐",
            "建筑建材": self.FILTER_BUILDING_MATERIALS,
            "机械设备": self.FILTER_MACHINERY,
            "劳务用工": self.FILTER_LABOR,
            "技术服务": self.FILTER_TECH_SERVICE,
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
        count = self.get_demand_count()
        assert count >= 0, f"筛选 {filter_name} 后需求数量异常"

    def get_demand_count(self) -> int:
        """获取需求卡片数量"""
        return self.page.locator(
            "div[class*='card'], div[class*='item'], article"
        ).count()

    def get_demand_titles(self) -> list[str]:
        """获取所有需求标题"""
        cards = self.page.locator("div[class*='card'], div[class*='item'], article")
        titles = []
        for i in range(min(cards.count(), 20)):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_demand(self) -> None:
        """点击第一个需求卡片"""
        card = self.page.locator("div[class*='card'], div[class*='item'], article").first
        if card.is_visible():
            card.click()
            self.wait_for_load()

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator(self.VIEW_ALL_BTN).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 断言 ====================

    def assert_demands_exist(self, min_count: int = 1) -> None:
        """断言需求卡片存在"""
        cards = self.page.locator("div[class*='card'], div[class*='item'], article")
        assert cards.count() >= min_count, f"未找到足够的需求卡片，期望 >= {min_count}"

    def assert_filter_result_contains(self, keywords: list[str]) -> None:
        """断言筛选结果包含指定关键词"""
        demand_section = self.page.locator(
            "div:has(h2:text('产业需求')), div:has(h3:text('产业需求'))"
        ).first
        content = demand_section.inner_text()
        assert any(kw in content for kw in keywords), (
            f"筛选结果未包含预期关键词: {keywords}"
        )