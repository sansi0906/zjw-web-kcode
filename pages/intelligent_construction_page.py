"""
智能建造页面 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IntelligentConstructionPage(BasePage):
    PAGE_URL = "/intelligentConstruction"
    """智能建造页面"""

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

    # ==================== 主要内容区 ====================
    # 申报入口
    DECLARATION_NEW_TECH = "text=智能建造新技术新产品申报"
    DECLARATION_SEED_ENTERPRISE = "text=智能建造种子企业申报"

    # 标准规范
    STANDARD_JJJ = "text=京津冀智能建造技术规程"
    STANDARD_ZJB = "text=住建部智能建造技术导则"
    STANDARD_TJ = "text=天津市智慧工地建设技术标准"

    # 平台/产品
    PLATFORM_CONTROL = "text=智能建造管控平台"
    PLATFORM_DIGITAL = "text=数字化交付平台"
    PRODUCT_BIM = "text=基于BIM的挂篮设计软件"
    PRODUCT_BEIDOU = "text=基于北斗卫星的自动化变形监测系统"
    PRODUCT_CARBON = "text=碳控官综合能源管理平台"
    PRODUCT_ASSEMBLY = "text=装配式搭建"

    # 轮播/展示区
    CAROUSEL_CONTAINER = ".n-carousel"
    CAROUSEL_DOT = ".n-carousel__dot"
    CAROUSEL_DOT_ACTIVE = ".n-carousel__dot--active"

    # 分页
    PAGINATION_INPUT = "input[type='text']"
    PAGINATION_PREV = ".n-pagination-item--button:has-text('上一页')"
    PAGINATION_NEXT = ".n-pagination-item--button:has-text('下一页')"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = "div:has-text('在线客服')"
    FLOAT_INTENT_FORM = "div:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网安备"

    # ==================== 页面操作 ====================

    def open(self) -> "IntelligentConstructionPage":
        """打开智能建造页面"""
        base = settings.base_url.rstrip("/")
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
        """断言筛选生效（智能建造页当前无分类 tab，调用即视为用例设计错误）"""
        self.assert_filter_effective(filter_name)

    def get_construction_count(self) -> int:
        """获取建造卡片数量"""
        return self.page.locator(
            "div[class*='card'], div[class*='item'], article"
        ).count()

    def get_construction_titles(self) -> list[str]:
        """获取所有建造标题"""
        cards = self.page.locator("div[class*='card'], div[class*='item'], article")
        titles = []
        for i in range(min(cards.count(), 20)):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def assert_constructions_exist(self, min_count: int = 1) -> None:
        """断言建造卡片存在"""
        count = self.get_construction_count()
        assert count >= min_count, f"期望建造数量 >= {min_count}，实际为 {count}"

    def click_first_construction(self) -> None:
        """点击第一个建造卡片"""
        card = self.page.locator("div[class*='card'], div[class*='item'], article").first
        if card.is_visible():
            card.click()
            self.wait_for_load()

    def click_view_all(self) -> None:
        """点击查看全部"""
        btn = self.page.locator("text=查看全部").first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 导航操作 ====================

    # ==================== 申报操作 ====================

    def click_new_tech_declaration(self) -> None:
        """点击智能建造新技术新产品申报"""
        btn = self.page.locator(self.DECLARATION_NEW_TECH).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_seed_enterprise_declaration(self) -> None:
        """点击智能建造种子企业申报"""
        btn = self.page.locator(self.DECLARATION_SEED_ENTERPRISE).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    # ==================== 标准规范操作 ====================

    def view_standard(self, standard_name: str) -> None:
        """查看标准规范详情"""
        standard_map = {
            "京津冀": self.STANDARD_JJJ,
            "住建部": self.STANDARD_ZJB,
            "天津": self.STANDARD_TJ,
        }
        selector = standard_map.get(standard_name)
        if selector:
            el = self.page.locator(selector).first
            if el.is_visible():
                el.click()
                self.wait_for_load()

    # ==================== 平台/产品操作 ====================

    def view_platform(self, platform_name: str) -> None:
        """查看平台/产品详情"""
        platform_map = {
            "管控平台": self.PLATFORM_CONTROL,
            "数字化交付": self.PLATFORM_DIGITAL,
            "BIM": self.PRODUCT_BIM,
            "北斗": self.PRODUCT_BEIDOU,
            "碳控官": self.PRODUCT_CARBON,
            "装配式": self.PRODUCT_ASSEMBLY,
        }
        selector = platform_map.get(platform_name)
        if selector:
            el = self.page.locator(selector).first
            if el.is_visible():
                el.click()
                self.wait_for_load()

    # ==================== 轮播图操作 ====================

    def get_carousel_dots_count(self) -> int:
        """获取轮播图 dots 数量"""
        return self.page.locator(self.CAROUSEL_DOT).count()

    def click_carousel_dot(self, index: int) -> None:
        """点击指定索引的轮播图 dot"""
        dots = self.page.locator(self.CAROUSEL_DOT)
        if dots.count() > index:
            dots.nth(index).click()
            self.page.wait_for_timeout(1500)

    # ==================== 分页操作 ====================

    def get_current_page(self) -> int:
        """获取当前页码"""
        try:
            input_el = self.page.locator(self.PAGINATION_INPUT).first
            if input_el.is_visible():
                text = input_el.input_value()
                return int(text) if text.isdigit() else 1
        except Exception:
            pass
        return 1

    def go_to_page(self, page_num: int) -> None:
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
        self.assert_text_visible("智能建造", partial=True)

    def assert_nav_link_works(self, link_text: str) -> None:
        """断言导航链接可点击且跳转正确"""
        self.click_nav_by_text(link_text)
        self.assert_url_contains(link_text)
