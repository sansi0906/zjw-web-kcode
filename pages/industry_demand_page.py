"""
产业需求 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IndustryDemandPage(BasePage):
    """产业需求页面"""

    PAGE_URL = "/industryDemand"

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
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

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
        """断言筛选生效（旧版 /industryDemand 页面已无筛选项）"""
        self.assert_filter_effective(filter_name)

    # 移动端需求卡片选择器
    DEMAND_CARDS_MOBILE = (
        "div[class*='card'], div[class*='item'], article, "
        "[class*='demand-card'], .n-carousel__slide, button"
    )

    def get_demand_count(self) -> int:
        """获取需求卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.DEMAND_CARDS_MOBILE).count()
        return self.page.locator(
            "div[class*='card'], div[class*='item'], article"
        ).count()

    def get_demand_titles(self) -> list[str]:
        """获取所有需求标题"""
        if self.is_mobile():
            cards = self.page.locator(self.DEMAND_CARDS_MOBILE)
        else:
            cards = self.page.locator("div[class*='card'], div[class*='item'], article")
        titles = []
        for i in range(min(cards.count(), 20)):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_demand(self) -> None:
        """点击第一个需求卡片"""
        if self.is_mobile():
            card = self.page.locator(self.DEMAND_CARDS_MOBILE).first
        else:
            card = self.page.locator(
                "div[class*='card'], div[class*='item'], article"
            ).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                card.evaluate("el => el.click()")
            self.wait_for_load()

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator(self.VIEW_ALL_BTN).first
        if btn.is_visible():
            try:
                btn.click()
            except Exception:
                btn.evaluate("el => el.click()")
            self.wait_for_load()

    # ==================== 断言 ====================

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        if self.is_mobile():
            assert "/industryDemand" in self.page.url, \
                f"URL 不包含 industryDemand，实际: {self.page.url}"
            return
        # WEB 端：滚动页面寻找产业需求区域
        try:
            self.assert_text_visible("产业需求", partial=True)
            return
        except AssertionError:
            pass
        for _ in range(6):
            self.page.evaluate("window.scrollBy(0, 400)")
            self.page.wait_for_timeout(500)
            try:
                self.assert_text_visible("产业需求", partial=True)
                return
            except AssertionError:
                continue
        # 最后兜底：检查需求卡片是否存在
        count = self.get_demand_count()
        assert count > 0, "未找到产业需求区域或需求卡片"

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