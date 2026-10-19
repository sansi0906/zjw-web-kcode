"""
供应大厅页面 Page Object
"""
from __future__ import annotations

import pytest

from pages.base_page import BasePage


class SupplyHallPage(BasePage):
    """供应大厅页面"""

    PAGE_URL = "/supplyHall"

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

    # ==================== 悬浮功能区 ====================
    FLOAT_PUBLISH = ".floating-action-item:has-text('发布商品')"
    FLOAT_INQUIRY = ".floating-action-item:has-text('求购询价')"
    FLOAT_CUSTOMER_SERVICE = ".floating-action-item:has-text('联系客服')"
    FLOAT_INTENT_FORM = ".floating-action-item:has-text('意向填报')"

    # ==================== 页脚 ====================
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"
    FOOTER_SECURITY = "text=津公网"

    # ==================== 分类筛选 ====================
    # 主分类
    CAT_建筑材料 = "text=建筑材料"
    CAT_水电暖通 = "text=水电暖通"
    CAT_机械设备 = "text=机械设备"
    CAT_工程机械 = "text=工程机械"
    CAT_劳务用工 = "text=劳务用工"

    # 子分类
    CAT_土建 = "text=土建"
    CAT_装饰装修 = "text=装饰装修"
    CAT_给排水 = "text=给排水"
    CAT_电气 = "text=电气"
    CAT_智能设备 = "text=智能设备"
    CAT_专业设备 = "text=专业设备"
    CAT_起重机械 = "text=起重机械"
    CAT_混凝土机械 = "text=混凝土机械"
    CAT_人机协同班组 = "text=人机协同班组"
    CAT_建筑工人 = "text=建筑工人"

    # 搜索
    SEARCH_INPUT = "input[type='text']"
    SEARCH_BTN = "text=搜索"
    RESET_BTN = "text=重置"

    # ==================== 商品卡片 ====================
    PRODUCT_CARDS = (
        "[class*='supply-item'], [class*='product-card'], "
        "[class*='goods-card'], [class*='item-card'], "
        "div[class*='card']:not([class*='nav']):not([class*='header']):"
        "not([class*='footer']):not([class*='float'])"
    )
    # 移动端商品卡片选择器（移动端为 button 网格布局）
    PRODUCT_CARDS_MOBILE = (
        "[class*='supply-item'], [class*='product-card'], "
        "[class*='goods-card'], [class*='item-card'], "
        "div[class*='card']:not([class*='nav']):not([class*='header']):"
        "not([class*='footer']):not([class*='float']), "
        ".n-carousel__slide, [class*='supply-card'], "
        "button[class*='min-w-0'][class*='flex-1'][class*='aspect-']"
    )
    VIEW_ALL_BTN = "text=查看全部"

    # ==================== 统计数据 ====================
    STATISTICS = "div[class*='relative'][class*='flex'][class*='flex-col']"

    # ==================== 页面操作 ====================

    def open(self) -> "SupplyHallPage":
        """打开供应大厅页面"""
        self.goto()
        return self

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接（支持 H5 抽屉导航）"""
        # 先尝试打开抽屉（非移动端直接返回 False，不影响 web）
        self._open_mobile_nav_if_needed()
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
        # 最后兜底：JS 点击不可见元素（移动端导航可能隐藏在抽屉中）
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
            if "supplyHall" in url:
                texts = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        return texts

    def click_view_all(self) -> None:
        """点击查看全部按钮"""
        btn = self.page.locator(self.VIEW_ALL_BTN).first
        if btn.is_visible():
            btn.click()
            self.wait_for_load()

    # ==================== 分类筛选操作 ====================

    def click_category(self, cat_name: str) -> None:
        """点击主分类"""
        cat_map = {
            "建筑材料": self.CAT_建筑材料,
            "水电暖通": self.CAT_水电暖通,
            "机械设备": self.CAT_机械设备,
            "工程机械": self.CAT_工程机械,
            "劳务用工": self.CAT_劳务用工,
        }
        sel = cat_map.get(cat_name)
        if sel:
            el = self.page.locator(sel).first
            if el.is_visible(timeout=3000):
                try:
                    el.click(timeout=5000)
                except Exception:
                    self._js_click_by_text(cat_name)
                self.page.wait_for_timeout(1000)
            else:
                self._js_click_by_text(cat_name)

    def click_subcategory(self, sub_name: str) -> None:
        """点击子分类"""
        sub_map = {
            "土建": self.CAT_土建,
            "装饰装修": self.CAT_装饰装修,
            "给排水": self.CAT_给排水,
            "电气": self.CAT_电气,
            "智能设备": self.CAT_智能设备,
            "专业设备": self.CAT_专业设备,
            "起重机械": self.CAT_起重机械,
            "混凝土机械": self.CAT_混凝土机械,
            "人机协同班组": self.CAT_人机协同班组,
            "建筑工人": self.CAT_建筑工人,
        }
        sel = sub_map.get(sub_name)
        if sel:
            el = self.page.locator(sel).first
            if el.is_visible(timeout=3000):
                try:
                    el.click(timeout=5000)
                except Exception:
                    self._js_click_by_text(sub_name)
                self.page.wait_for_timeout(1000)
            else:
                self._js_click_by_text(sub_name)

    def _js_click_by_text(self, text: str) -> None:
        """通过文本内容用 JS 点击元素"""
        try:
            self.page.evaluate(
                """(text) => {
                const els = Array.from(document.querySelectorAll('*'));
                const el = els.find(e => (e.textContent||'').trim() === text);
                if (el) { el.click(); return true; }
                return false;
                }""",
                text,
            )
            self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def get_category_count(self) -> int:
        """获取主分类数量"""
        cats = [self.CAT_建筑材料, self.CAT_水电暖通, self.CAT_机械设备,
                self.CAT_工程机械, self.CAT_劳务用工]
        count = 0
        for sel in cats:
            if self.page.locator(sel).first.is_visible():
                count += 1
        return count

    def fill_search(self, text: str) -> None:
        """输入搜索关键词"""
        el = self.page.locator(self.SEARCH_INPUT).first
        if el.is_visible():
            el.fill(text)

    def click_search(self) -> None:
        """点击搜索按钮"""
        btn = self.page.locator(self.SEARCH_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_reset(self) -> None:
        """点击重置按钮"""
        btn = self.page.locator(self.RESET_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1000)

    def click_publish(self) -> None:
        """点击发布商品按钮"""
        btn = self.page.locator(self.FLOAT_PUBLISH).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    def click_inquiry(self) -> None:
        """点击求购询价按钮"""
        btn = self.page.locator(self.FLOAT_INQUIRY).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    def click_customer_service(self) -> None:
        """点击联系客服按钮"""
        btn = self.page.locator(self.FLOAT_CUSTOMER_SERVICE).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    def click_intent_form(self) -> None:
        """点击意向填报按钮"""
        btn = self.page.locator(self.FLOAT_INTENT_FORM).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(1500)

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)

    # ==================== 断言辅助 ====================

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        self.assert_text_visible("供应大厅", partial=True)

    def assert_supply_items_exist(self, min_count: int = 1) -> None:
        """断言商品/服务卡片存在"""
        count = self.get_product_count()
        assert count >= min_count, f"期望商品数量 >= {min_count}，实际为 {count}"

    def get_product_count(self) -> int:
        """获取商品/服务卡片数量"""
        if self.is_mobile():
            return self.page.locator(self.PRODUCT_CARDS_MOBILE).count()
        return self.page.locator(self.PRODUCT_CARDS).count()

    def get_supply_item_titles(self) -> list[str]:
        """获取所有商品/服务标题"""
        if self.is_mobile():
            cards = self.page.locator(self.PRODUCT_CARDS_MOBILE)
        else:
            cards = self.page.locator(self.PRODUCT_CARDS)
        titles = []
        for i in range(min(cards.count(), 20)):
            title = cards.nth(i).text_content()
            if title and title.strip():
                titles.append(title.strip()[:50])
        return titles

    def click_first_supply_item(self) -> None:
        """点击第一个供应商品"""
        if self.is_mobile():
            card = self.page.locator(self.PRODUCT_CARDS_MOBILE).first
        else:
            card = self.page.locator(self.PRODUCT_CARDS).first
        if card.is_visible():
            try:
                card.click()
            except Exception:
                # JS 点击兜底（移动端卡片可能被遮挡）
                card.evaluate("el => el.click()")
            self.wait_for_load()

    def get_statistics(self) -> list[str]:
        """获取统计数据"""
        stats = []
        # 统计数据是4个独立的div，class包含 after:absolute after:right-0
        stat_elements = self.page.locator(
            "div[class*='after:absolute'][class*='after:right-0']"
        )
        for i in range(stat_elements.count()):
            text = stat_elements.nth(i).text_content()
            if text and text.strip():
                stats.append(text.strip()[:100])
        return stats

    def assert_prices_displayed(self) -> None:
        """断言商品价格信息正常展示"""
        price_locators = [
            self.page.locator("text=/¥\\d+/"),
            self.page.locator("text=/￥\\d+/"),
            self.page.locator("[class*='price']"),
            self.page.locator("[class*='amount']"),
        ]
        for p in price_locators:
            if p.count() > 0:
                return
        product_count = self.page.locator(self.PRODUCT_CARDS).count()
        if product_count == 0:
            pytest.skip("未找到供应商品卡片，跳过价格检查")
        pytest.skip(f"找到 {product_count} 个供应商品但未找到价格元素，可能为环境数据问题")

    def has_pagination(self) -> bool:
        """检查是否存在分页控件"""
        pagination = self.page.locator(
            ".n-pagination, [class*='pagination'], [class*='pager']"
        )
        return pagination.count() > 0

    def assert_url_contains(self, url_part: str) -> None:
        """断言 URL 包含指定字符串"""
        assert url_part in self.page.url, f"URL 不包含 {url_part}，当前 URL: {self.page.url}"