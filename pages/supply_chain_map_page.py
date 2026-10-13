"""
供应链地图页面 Page Object

供应链地图是首页的一个模块，不需要独立页面导航。
"""
from __future__ import annotations

from pages.base_page import BasePage


class SupplyChainMapPage(BasePage):
    """供应链地图模块"""

    # 分类标签
    CATEGORY_TABS = ".supply_chain_map_tab"

    # 区域数据
    REGION_ITEMS = (
        "[class*='region'], [class*='area'], "
        "text=/区/, text=/县/, text=/市/"
    )

    # 区域名称匹配
    REGION_NAMES = [
        "蓟州区", "宝坻区", "武清区", "宁河区", "北辰区",
        "市内六区", "东丽区", "西青区", "津南区", "静海区", "滨海新区",
    ]

    def open(self) -> "SupplyChainMapPage":
        """打开首页并滚动到供应链地图模块"""
        self.goto()
        self.page.wait_for_timeout(2000)
        # 滚动到供应链地图区域
        self.page.evaluate("window.scrollTo(0, 800)")
        self.page.wait_for_timeout(1000)
        return self

    def scroll_to_map(self) -> None:
        """滚动到供应链地图区域"""
        self.page.evaluate("window.scrollTo(0, 800)")
        self.page.wait_for_timeout(1000)

    def get_category_tabs(self) -> list[str]:
        """获取所有分类标签文本"""
        tabs = self.page.locator(self.CATEGORY_TABS)
        texts = []
        for i in range(tabs.count()):
            text = tabs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

    def click_category_tab(self, category: str) -> None:
        """点击分类标签"""
        tab = self.page.locator(f".supply_chain_map_tab:has-text('{category}')").first
        if tab.is_visible():
            tab.click()
            self.page.wait_for_timeout(1000)

    def get_region_count(self) -> int:
        """获取区域数量"""
        self.scroll_to_map()
        count = 0
        for region_name in self.REGION_NAMES:
            el = self.page.locator(f"text={region_name}").first
            if el.is_visible():
                count += 1
        return count

    def get_region_info(self, region_name: str) -> str:
        """获取区域信息（包含建材数量）"""
        el = self.page.locator(f"text={region_name}").first
        if el.is_visible():
            # 尝试获取父级元素文本
            parent = el.locator("..")
            if parent.count() > 0:
                text = parent.text_content()
                if text:
                    return text.strip()[:100]
        return ""

    def assert_map_displayed(self) -> None:
        """断言供应链地图正常展示"""
        self.scroll_to_map()
        count = self.get_region_count()
        assert count > 0, "未找到供应链地图区域数据"

    def assert_category_tabs_exist(self) -> None:
        """断言分类标签存在"""
        tabs = self.get_category_tabs()
        assert len(tabs) > 0, "未找到供应链地图分类标签"

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        self.assert_text_visible("供应链地图", partial=True)

    def click_first_region(self) -> None:
        """点击第一个区域"""
        for region_name in self.REGION_NAMES:
            el = self.page.locator(f"text={region_name}").first
            if el.is_visible():
                el.click()
                self.page.wait_for_timeout(1000)
                return