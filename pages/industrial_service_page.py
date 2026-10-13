"""
产业化服务 Page Object
"""
from __future__ import annotations

from pages.base_page import BasePage


class IndustrialServicePage(BasePage):
    """产业化服务页面"""

    SERVICE_ITEMS = "[class*='service'], div[class*='card']"

    def open(self) -> IndustrialServicePage:
        """打开首页并定位到产业化服务模块"""
        self.goto()
        self.page.wait_for_timeout(2000)
        return self

    def assert_service_exists(self) -> None:
        """验证产业化服务模块存在"""
        self.assert_text_visible("专属客服", partial=True)

    def get_service_count(self) -> int:
        """获取服务项数量"""
        return self.page.locator(self.SERVICE_ITEMS).count()
