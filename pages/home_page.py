"""
首页 Page Object - 基于改版后实际元素
URL: http://172.16.1.165:3200/
"""
from __future__ import annotations

from pages.base_page import BasePage


class HomePage(BasePage):
    """天津市建筑产业互联网平台首页"""

    # ==================== 顶部导航 ====================
    LOGO = "img[src*='logoAndTitle']"
    LOGIN_BTN = "span:has-text('登录')"
    REGISTER_BTN = "span:has-text('注册')"
    NAV_ITEMS = ".header-title a, .nav-cneter a, header a, nav a, .nav a"
    NAV_HOME = "text=首页"
    NAV_SUPPLY_HALL = "text=供应大厅"
    NAV_INTELLIGENT_CONSTRUCTION = "text=智能建造"
    NAV_KEY_PROJECT = "text=重点项目"
    NAV_INDUSTRY_POLICY = "text=产业政策"
    NAV_INDUSTRY_ASSOCIATION = "text=产业协会"
    NAV_ACHIEVEMENT_TRANSFORMATION = "text=成果转化"
    NAV_CLOUD_SERVICE = "text=云服务"

    # 导航 URL 映射（用于跳转验证）
    NAV_ROUTES = {
        "首页": "/",
        "供应大厅": "supplyHall",
        "智能建造": "intelligentConstruction",
        "重点项目": "keyProject",
        "产业政策": "industryNews",
        "产业协会": "industryAssociation",
        "成果转化": "achievementTransformation",
        "云服务": "cloudService",
    }

    # ==================== 搜索栏 ====================
    SEARCH_INPUT = "input[placeholder='请输入您要找的类目、商品或、材料']"
    SEARCH_BTN = "button:has-text('搜索')"

    # ==================== 热门搜索 ====================
    HOT_SEARCH_LABEL = "text=热门搜索："
    HOT_SEARCH_BTNS = "button[class*='bg-[#F4F7FF]']"

    # ==================== 轮播图 ====================
    CAROUSEL_CONTAINER = ".n-carousel"
    CAROUSEL_DOT_ACTIVE = ".n-carousel__dot--active"
    CAROUSEL_DOT = ".n-carousel__dot"
    CAROUSEL_IMG = "img[src*='/api/sys/file/pub/download']"

    # ==================== 服务链接区 ====================
    SERVICE_STATS = "span[class*='cursor-default'][class*='bg-white/25'][class*='text-[#1653FF]']"

    # ==================== 产业服务 ====================
    SECTION_INDUSTRY_SERVICE = "h2:has-text('产业服务')"
    SERVICE_CARDS = "h3:has-text('供应大厅'), h3:has-text('劳务对接'), h3:has-text('AI+工具集'), h3:has-text('金融服务'), h3:has-text('建筑机器人'), h3:has-text('智慧工地')"
    SERVICE_CARD_TITLES = ["供应大厅", "劳务对接", "AI+工具集", "金融服务", "建筑机器人", "智慧工地"]
    DETAIL_BTNS = "button:has-text('了解详情')"

    # ==================== 津筑云商 ====================
    SECTION_TJDIGITAL = "h2:has-text('津筑云商')"
    MERCHANT_TABS = ".merchant-tabs"
    MERCHANT_TAB_ECOLOGY = "text=产业生态全景图"
    MERCHANT_TAB_SERVICE = "text=建筑服务业"
    MERCHANT_TAB_MANUFACTURING = "text=建筑制造业"
    MERCHANT_TAB_CONSTRUCTION = "text=建筑建造业"
    MERCHANT_IMAGES = "img[src*='/20260923/']"

    # ==================== 会展活动 ====================
    SECTION_EXHIBITION = "h2:has-text('会展活动')"
    ACTIVITY_CARDS = "h3[class*='max-h-[56px]']"

    # ==================== 产业需求 ====================
    SECTION_DEMAND = "h2:has-text('产业需求')"
    DEMAND_ITEMS = "h3[class*='h-[44px]'][class*='w-[232px]']"
    VIEW_ALL_DEMAND = "a:has-text('查看全部')"

    # ==================== 产业政策 ====================
    SECTION_POLICY = "h2:has-text('产业政策')"
    POLICY_TABS = "button:has-text('行业动态'), button:has-text('政策资讯'), button:has-text('政策解读')"
    POLICY_TAB_INDUSTRY_NEWS = "text=行业动态"
    POLICY_TAB_POLICY_INFO = "text=政策资讯"
    POLICY_TAB_POLICY_INTERPRETATION = "text=政策解读"
    NEWS_ITEMS = "h3[class*='mt-[26px]']"
    VIEW_ALL_POLICY = "a:has-text('查看全部')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_COPYRIGHT = "text=工人乐"
    FOOTER_NAV = "footer span.cursor-pointer"

    # ==================== 悬浮功能区 ====================
    FLOAT_CUSTOMER_SERVICE = ".floating-action-label:has-text('在线客服')"
    FLOAT_INTENT_FORM = ".floating-action-label:has-text('意向填报')"

    # ==================== 页面操作 ====================

    def open(self) -> HomePage:
        """打开首页并等待加载"""
        self.goto()
        self.wait_for_load()
        return self

    def click_logo(self) -> None:
        """点击 Logo 返回首页"""
        self.safe_click(self.LOGO)

    # ==================== 导航操作 ====================

    def click_login(self) -> None:
        """点击登录按钮"""
        self.click(self.LOGIN_BTN)

    def click_register(self) -> None:
        """点击注册按钮"""
        self.click(self.REGISTER_BTN)

    def get_nav_texts(self) -> list[str]:
        """获取所有导航链接文本"""
        if self.is_mobile():
            self._open_mobile_nav_if_needed()
            nav_selectors = [
                ".n-drawer a",
                ".ant-drawer a",
                ".drawer a",
                "[class*='drawer'] a",
                ".nav-collapse a",
                ".mobile-nav a",
                "nav a",
                "header a",
                ".nav a",
                self.NAV_ITEMS,
                "button",
            ]
            texts = []
            for sel in nav_selectors:
                try:
                    navs = self.page.locator(sel)
                    for i in range(navs.count()):
                        try:
                            text = navs.nth(i).text_content()
                        except Exception:
                            continue
                        if text and text.strip():
                            t = text.strip()
                            if t and t not in texts:
                                texts.append(t)
                except Exception:
                    continue
            return texts

        navs = self.page.locator(self.NAV_ITEMS)
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接"""
        if self.is_mobile():
            self._open_mobile_nav_if_needed()
            # 移动端导航项可能是 button 或 a，直接查找可见元素
            for sel in [f"button:has-text('{nav_text}')", f"text={nav_text}", f"a:has-text('{nav_text}')"]:
                try:
                    nav = self.page.locator(sel).first
                    if nav.is_visible(timeout=1500):
                        nav.click()
                        self.wait_for_load()
                        return
                except Exception:
                    continue
            # 优先在抽屉内查找（作为兜底）
            for ds in [".n-drawer", ".ant-drawer", ".drawer", "[class*='drawer']", ".nav-collapse"]:
                try:
                    if self.page.locator(ds).first.is_visible(timeout=800):
                        link = self.page.locator(f"{ds} a:has-text('{nav_text}')").first
                        if link.is_visible(timeout=1000):
                            link.click()
                            self.wait_for_load()
                            return
                except Exception:
                    continue
            self._close_mobile_nav_if_needed()
            return
        nav = self.page.locator(f"text={nav_text}").first
        if nav.is_visible():
            nav.click()
            self.wait_for_load()

    # ==================== 搜索操作 ====================

    def fill_search_input(self, text: str) -> None:
        """填充搜索框"""
        search = self.page.locator(self.SEARCH_INPUT).first
        if search.is_visible():
            search.fill(text)

    def click_search_btn(self) -> None:
        """点击搜索按钮"""
        btn = self.page.locator(self.SEARCH_BTN).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 热门搜索 ====================

    def get_hot_search_count(self) -> int:
        """获取热搜词按钮数量"""
        return self.page.locator(self.HOT_SEARCH_BTNS).count()

    def click_hot_search(self, index: int = 0) -> None:
        """点击热搜词按钮"""
        btns = self.page.locator(self.HOT_SEARCH_BTNS)
        if btns.count() > index:
            btns.nth(index).click()
            self.wait_for_load()

    # ==================== 轮播图 ====================

    def assert_carousel_loaded(self) -> bool:
        """断言轮播图加载完成"""
        return self.is_visible(self.CAROUSEL_CONTAINER, timeout=5000)

    def get_carousel_dots_count(self) -> int:
        """获取轮播图 dots 数量"""
        return self.page.locator(self.CAROUSEL_DOT).count()

    def get_active_carousel_dot_index(self) -> int:
        """获取当前激活的 dot 索引"""
        dots = self.page.locator(self.CAROUSEL_DOT)
        for i in range(dots.count()):
            dot = dots.nth(i)
            if dot.evaluate("el => el.classList.contains('n-carousel__dot--active')"):
                return i
        return -1

    def click_carousel_dot(self, index: int) -> None:
        """点击指定索引的轮播图 dot"""
        dots = self.page.locator(self.CAROUSEL_DOT)
        if dots.count() > index:
            dots.nth(index).click()
            self.page.wait_for_timeout(1500)

    def get_carousel_images_count(self) -> int:
        """获取轮播图图片数量"""
        return self.page.locator(self.CAROUSEL_IMG).count()

    # ==================== 服务链接区 ====================

    def get_service_stats_count(self) -> int:
        """获取统计数字数量"""
        return self.page.locator(self.SERVICE_STATS).count()

    def get_service_stats_texts(self) -> list[str]:
        """获取统计数字文本"""
        stats = self.page.locator(self.SERVICE_STATS)
        texts = []
        for i in range(stats.count()):
            text = stats.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

    # ==================== 产业服务 ====================

    def scroll_to_industry_service(self) -> None:
        """滚动到产业服务区域"""
        self.scroll_to(self.SECTION_INDUSTRY_SERVICE)

    def get_service_card_titles(self) -> list[str]:
        """获取服务子分类卡片标题"""
        cards = self.page.locator(self.SERVICE_CARDS)
        titles = []
        for i in range(cards.count()):
            text = cards.nth(i).text_content()
            if text and text.strip():
                titles.append(text.strip())
        return titles

    def click_detail_btn(self, index: int = 0) -> None:
        """点击'了解详情'按钮"""
        btns = self.page.locator(self.DETAIL_BTNS)
        if btns.count() > index:
            btns.nth(index).click()
            self.wait_for_load()

    # ==================== 津筑云商 ====================

    def scroll_to_tjdigital(self) -> None:
        """滚动到津筑云商区域"""
        self.scroll_to(self.SECTION_TJDIGITAL)

    def get_merchant_tab_count(self) -> int:
        """获取生态标签数量"""
        return self.page.locator(self.MERCHANT_TAB_ECOLOGY).count() + \
               self.page.locator("button:has-text('建筑服务业')").count() + \
               self.page.locator("button:has-text('建筑制造业')").count() + \
               self.page.locator("button:has-text('建筑建造业')").count()

    def click_merchant_tab(self, tab_text: str) -> None:
        """点击生态标签"""
        self.click(f"text={tab_text}")
        self.page.wait_for_timeout(1000)

    def get_merchant_images_count(self) -> int:
        """获取企业图片数量"""
        return self.page.locator(self.MERCHANT_IMAGES).count()

    # ==================== 会展活动 ====================

    def scroll_to_exhibition(self) -> None:
        """滚动到会展活动区域"""
        self.scroll_to(self.SECTION_EXHIBITION)

    def get_activity_card_count(self) -> int:
        """获取活动卡片数量"""
        return self.page.locator(self.ACTIVITY_CARDS).count()

    def get_activity_card_titles(self) -> list[str]:
        """获取活动卡片标题"""
        cards = self.page.locator(self.ACTIVITY_CARDS)
        titles = []
        for i in range(cards.count()):
            text = cards.nth(i).text_content()
            if text and text.strip():
                titles.append(text.strip())
        return titles

    # ==================== 产业需求 ====================

    def scroll_to_demand(self) -> None:
        """滚动到产业需求区域"""
        self.scroll_to(self.SECTION_DEMAND)

    def get_demand_item_count(self) -> int:
        """获取需求条目数量"""
        return self.page.locator(self.DEMAND_ITEMS).count()

    def get_demand_item_titles(self) -> list[str]:
        """获取需求条目标题"""
        items = self.page.locator(self.DEMAND_ITEMS)
        titles = []
        for i in range(min(items.count(), 20)):
            text = items.nth(i).text_content()
            if text and text.strip():
                titles.append(text.strip())
        return titles

    def click_view_all_demand(self) -> None:
        """点击产业需求'查看全部'"""
        btn = self.page.locator(self.VIEW_ALL_DEMAND).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 产业政策 ====================

    def scroll_to_policy(self) -> None:
        """滚动到产业政策区域"""
        self.scroll_to(self.SECTION_POLICY)

    def get_policy_tab_count(self) -> int:
        """获取政策标签页数量"""
        return self.page.locator("button:has-text('行业动态'), button:has-text('政策资讯'), button:has-text('政策解读')").count()

    def click_policy_tab(self, tab_text: str) -> None:
        """点击政策标签页"""
        self.click(f"text={tab_text}")
        self.page.wait_for_timeout(1000)

    def get_news_item_count(self) -> int:
        """获取新闻条目数量"""
        return self.page.locator(self.NEWS_ITEMS).count()

    def get_news_item_titles(self) -> list[str]:
        """获取新闻条目标题"""
        items = self.page.locator(self.NEWS_ITEMS)
        titles = []
        for i in range(min(items.count(), 10)):
            text = items.nth(i).text_content()
            if text and text.strip():
                titles.append(text.strip())
        return titles

    def click_view_all_policy(self) -> None:
        """点击产业政策'查看全部'"""
        btns = self.page.locator(self.VIEW_ALL_POLICY)
        for i in range(btns.count()):
            btn = btns.nth(i)
            href = btn.get_attribute("href") or ""
            if "industryNews" in href:
                btn.click()
                self.wait_for_load()
                return

    # ==================== 页脚 ====================

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    def click_footer_phone(self) -> None:
        """点击页脚服务电话"""
        phone = self.page.locator(self.FOOTER_SERVICE_PHONE).first
        if phone.is_visible():
            phone.click()

    def get_footer_nav_count(self) -> int:
        """获取页脚导航链接数量"""
        return self.page.locator("footer span.cursor-pointer").count()

    # ==================== 悬浮按钮 ====================

    def click_customer_service(self) -> None:
        """点击在线客服"""
        btn = self.page.locator(self.FLOAT_CUSTOMER_SERVICE).first
        if btn.is_visible():
            self.safe_click(self.FLOAT_CUSTOMER_SERVICE)
            self.page.wait_for_timeout(1500)

    def click_intent_form(self) -> None:
        """点击意向填报"""
        btn = self.page.locator(self.FLOAT_INTENT_FORM).first
        if btn.is_visible():
            self.safe_click(self.FLOAT_INTENT_FORM)
            self.page.wait_for_timeout(1500)

    # ==================== 断言辅助 ====================

    def assert_page_loaded(self) -> None:
        """断言首页加载完成"""
        title = self.page.title()
        assert "天津市建筑产业互联网平台" in title, f"标题不匹配，实际: {title}"

    def assert_nav_links_exists(self, expected: list[str]) -> None:
        """断言导航包含所有预期链接"""
        nav_texts = self.get_nav_texts()
        missing = [text for text in expected if text not in nav_texts]
        assert not missing, f"导航缺少: {missing}"

    def assert_url_contains(self, fragment: str) -> None:
        """断言 URL 包含指定字符串"""
        url = self.page.url
        assert fragment in url, f"URL 不包含 '{fragment}'，实际 URL: {url}"
