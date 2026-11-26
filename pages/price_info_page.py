"""
造价信息查询页面 Page Object

URL: /priceInfo
PC 端为完整功能页（材料价格/预拌混凝土/预拌砂浆/人工单价 4 个 tab + 筛选 + 表格 + 分页）；
H5 端当前为「正在开发中」占位页。
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class PriceInfoPage(BasePage):
    """造价信息查询页面"""

    PAGE_URL = "/priceInfo"

    # 顶部导航（价格信息在主导航中）
    NAV_ITEMS = "header a, nav a, [class*='nav'] a, [class*='header'] a"
    NAV_PRICE_INFO = "text=价格信息"

    # 页面标题
    H1 = "h1"

    # 功能 tab（button.tab-item，active 为 tab-item--active）
    TAB_ITEM = "button.tab-item"
    TAB_ACTIVE = "button.tab-item--active"
    TAB_NAMES = ["材料价格查询", "预拌混凝土", "预拌砂浆", "人工单价"]

    # 筛选区
    FILTER_REGION = "text=数据地区"
    FILTER_MONTH = "text=数据年月"
    FILTER_CATEGORY = "text=材料分类"

    # 搜索
    SEARCH_INPUT = "input.search-input"
    SEARCH_BTN = "text=搜索"

    # 价格明细表格
    TABLE = "table"
    TABLE_HEADERS = ["序号", "材料名称", "规格型号", "单位", "中准价（元）", "区间价格（元）", "振幅", "分类", "操作"]

    # 分页（naive-ui）
    PAGINATION = ".n-pagination"
    PAGINATION_ITEM = ".n-pagination-item"

    # 页脚
    FOOTER_SERVICE_PHONE = "text=400-115-0629"
    FOOTER_ICP = "text=津ICP备"

    # H5 占位
    H5_UNDER_DEV = ".price-info-mobile"
    H5_DEV_TEXT = "正在开发中"
    H5_DEV_SUB_TEXT = "价格信息功能即将上线"

    def open(self) -> "PriceInfoPage":
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        try:
            self.page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
        return self

    def get_h1(self) -> str:
        try:
            el = self.page.locator(self.H1).first
            if el.is_visible(timeout=2000):
                return (el.text_content() or "").strip()
        except Exception:
            pass
        return ""

    def get_tab_names(self) -> list[str]:
        try:
            return self.page.evaluate(
                """() => Array.from(document.querySelectorAll('button.tab-item'))
                    .map(e => (e.innerText||'').trim()).filter(t => t)"""
            )
        except Exception:
            return []

    def get_active_tab(self) -> str:
        try:
            el = self.page.locator(self.TAB_ACTIVE).first
            if el.is_visible(timeout=2000):
                return (el.text_content() or "").strip()
        except Exception:
            pass
        return ""

    def click_tab(self, name: str) -> None:
        el = self.page.locator(f"button.tab-item:has-text('{name}')").first
        if el.is_visible(timeout=2000):
            el.click()
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=3000)
                except Exception:
                    pass

    def get_table_count(self) -> int:
        try:
            return self.page.evaluate("() => document.querySelectorAll('table').length")
        except Exception:
            return 0

    def get_table_headers(self) -> list[str]:
        """获取第一个表格的表头文本"""
        try:
            return self.page.evaluate(
                """() => {
                    const t = document.querySelector('table');
                    if (!t) return [];
                    const ths = t.querySelectorAll('thead th, thead td, tr:first-child th, tr:first-child td');
                    return Array.from(ths).map(e => (e.innerText||'').trim()).filter(t => t);
                }"""
            )
        except Exception:
            return []

    def get_table_row_count(self) -> int:
        """获取第一个表格的数据行数（排除表头）"""
        try:
            return self.page.evaluate(
                """() => {
                    const t = document.querySelector('table');
                    if (!t) return 0;
                    const rows = t.querySelectorAll('tbody tr, tr');
                    return Math.max(0, rows.length - 1);
                }"""
            )
        except Exception:
            return 0

    def fill_search(self, text: str) -> None:
        el = self.page.locator(self.SEARCH_INPUT).first
        if el.is_visible(timeout=2000):
            el.fill(text)

    def click_search(self) -> None:
        btn = self.page.locator(self.SEARCH_BTN).first
        if btn.is_visible(timeout=2000):
            btn.click()
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=3000)
                except Exception:
                    pass

    def get_pagination_page_count(self) -> int:
        try:
            return self.page.evaluate(
                "() => document.querySelectorAll('.n-pagination-item').length"
            )
        except Exception:
            return 0

    def goto_page(self, page_num: int) -> None:
        el = self.page.locator(f".n-pagination-item:has-text('{page_num}')").first
        if el.is_visible(timeout=2000):
            el.click()
            try:
                self.page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass

    def is_h5_under_development(self) -> bool:
        """H5 端是否为「正在开发中」占位页"""
        if not self.is_mobile():
            return False
        try:
            body = self.page.evaluate("() => document.body ? (document.body.innerText||'') : ''")
            return self.H5_DEV_TEXT in body
        except Exception:
            return False

    def select_filter(self, filter_index: int, option_text: str) -> None:
        """点击第 filter_index 个筛选项并选择 option_text"""
        items = self.page.locator("div.filter-item")
        if items.count() <= filter_index:
            return
        items.nth(filter_index).click()
        try:
            self.page.wait_for_timeout(500)
            opt = self.page.locator(f".n-select-option:has-text('{option_text}')").first
            if opt.is_visible(timeout=2000):
                opt.click()
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass

    def get_filter_values(self) -> list[str]:
        """获取筛选区当前值列表"""
        try:
            return self.page.evaluate(
                """() => Array.from(document.querySelectorAll('div.filter-item')).map(e => (e.innerText||'').trim().replace(/\\n/g,'：'))"""
            )
        except Exception:
            return []

    def click_tab_by_name(self, name: str) -> None:
        self.click_tab(name)
    def assert_page_loaded(self) -> None:
        if self.is_mobile():
            assert "priceInfo" in self.page.url, f"URL 不包含 priceInfo，实际: {self.page.url}"
            return
        h1 = self.get_h1()
        assert "造价信息" in h1, f"未找到页面标题「建设工程造价信息查询」，实际 h1={h1!r}"

    def scroll_to_footer(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=3000)
        except Exception:
            pass