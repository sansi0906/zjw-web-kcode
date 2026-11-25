"""
造价信息查询页面 H5 专项测试（移动端设备仿真）

H5 端当前为「正在开发中」占位页，验证占位文案与基础结构。
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.price_info_page import PriceInfoPage

pytestmark = [pytest.mark.h5, pytest.mark.regression]


@allure.feature("造价信息查询页面-H5")
class TestPriceInfoH5(BasePageTest):
    """造价信息查询页面 H5 测试用例"""

    page_name = "造价信息查询"
    page_fixture_name = "h5_price_info_page"

    # H5 端无顶部导航栏（导航在菜单图标内），且页面为占位页
    EXPECTED_NAV_TEXTS = []
    SKIP_NAV_ACTIVE_ASSERT = True

    @allure.story("占位页")
    @allure.title("H5 正在开发中占位展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_under_development(self) -> None:
        """验证 H5 端展示「正在开发中」占位文案"""
        self.page_obj.open()
        assert self.page_obj.is_h5_under_development(), "H5 端未展示「正在开发中」占位"
        body = self.page_obj.page.evaluate("() => document.body.innerText || ''")
        assert self.page_obj.H5_DEV_SUB_TEXT in body, "H5 占位页缺少「价格信息功能即将上线」副文案"
        self.page_obj.take_screenshot("h5_price_info_under_dev", "info")

    @allure.story("占位页")
    @allure.title("H5 占位页无横向溢出")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_no_horizontal_overflow(self) -> None:
        """验证 H5 占位页无横向溢出"""
        self.page_obj.open()
        overflow, sw, cw = self.page_obj.has_horizontal_overflow()
        assert not overflow, f"H5 造价信息占位页存在横向溢出: scrollWidth={sw}, clientWidth={cw}"

    @allure.story("页脚")
    @allure.title("H5 页脚联系电话")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_footer_phone(self) -> None:
        """验证 H5 页脚联系电话展示"""
        self.page_obj.open()
        self.page_obj.scroll_to_footer()
        self.page_obj.assert_text_visible("400-115-0629")

    @allure.story("页脚")
    @allure.title("H5 页脚 ICP 备案")
    @allure.severity(allure.severity_level.MINOR)
    def test_h5_footer_icp(self) -> None:
        """验证 H5 页脚 ICP 备案展示"""
        self.page_obj.open()
        self.page_obj.scroll_to_footer()
        self.page_obj.assert_text_visible("津ICP备")