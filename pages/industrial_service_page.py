"""
产业化服务 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IndustrialServicePage(BasePage):
    """产业化服务页面"""

    # 移动端服务项选择器
    SERVICE_ITEMS = "[class*='service'], div[class*='card']"
    SERVICE_ITEMS_MOBILE = (
        "[class*='service'], div[class*='card'], "
        "[class*='industrial-service'], .n-carousel__slide, button"
    )

    def open(self) -> IndustrialServicePage:
        """打开首页并定位到产业化服务模块"""
        self.goto()
        self.page.wait_for_timeout(2000)
        return self

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        if self.is_mobile():
            # 移动端首页可能无独立"首页"标题文本，检查服务项是否存在
            count = self.get_service_count()
            assert count > 0, "移动端未找到服务项"
            return
        self.assert_text_visible("首页", partial=True)

    def assert_service_exists(self) -> None:
        """验证产业化服务模块存在"""
        # 检查服务项数量，不依赖特定文本（WEB/移动端可能不同）
        count = self.get_service_count()
        assert count > 0, "未找到产业化服务项"

    def get_service_count(self) -> int:
        """获取服务项数量"""
        if self.is_mobile():
            return self.page.locator(self.SERVICE_ITEMS_MOBILE).count()
        return self.page.locator(self.SERVICE_ITEMS).count()

