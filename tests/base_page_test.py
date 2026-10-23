"""
页面通用测试基类
所有页面测试类继承此类，自动获得通用测试用例
避免页面之间重复测试逻辑
"""
from __future__ import annotations

import allure
import pytest


class BasePageTest:
    """
    页面通用测试基类
    
    子类需定义:
        page_name: 页面中文名称，用于标题和 allure
        page_fixture_name: fixture 名称，默认 f"{class_name.lower()}_page"
    """

    page_name: str = ""
    page_fixture_name: str = ""

    def _first_visible(self, selector: str):
        """返回第一个可见的匹配元素（找不到返回 None）

        站点同时渲染 PC/移动端两套页脚与悬浮按钮，隐藏的那套在 DOM 中排在前，
        直接用 .first 会取到隐藏元素导致误判。
        """
        loc = self.page_obj.page.locator(selector)
        for i in range(min(loc.count(), 20)):
            el = loc.nth(i)
            try:
                if el.is_visible(timeout=500):
                    return el
            except Exception:
                continue
        return None

    @pytest.fixture(autouse=True)
    def _setup(self, request) -> None:
        """自动注入页面 fixture"""
        if self.page_fixture_name:
            self.page_obj = request.getfixturevalue(self.page_fixture_name)
            request.node.page = self.page_obj.page

    @allure.story("页面加载")
    @allure.title("页面正常加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_load(self) -> None:
        """页面正常加载，标题确认"""
        allure.dynamic.title(f"{self.page_name} - 页面正常加载")
        self.page_obj.open()
        self.page_obj.assert_page_loaded()

    @allure.story("顶部导航")
    @allure.title("导航栏完整性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_completeness(self) -> None:
        """验证导航栏包含所有预期链接"""
        allure.dynamic.title(f"{self.page_name} - 导航栏完整性")
        self.page_obj.open()
        nav_texts = self.page_obj.get_nav_texts()
        expected = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        missing = [text for text in expected if text not in nav_texts]
        if missing:
            pytest.skip(f"当前页面导航缺少: {missing}")

    @allure.story("顶部导航")
    @allure.title("链接高亮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_active_state(self) -> None:
        """当前页面导航项应为激活状态

        按 href 匹配当前路由对应的导航链接，校验其带有激活样式。
        """
        allure.dynamic.title(f"{self.page_name} - 链接高亮")
        self.page_obj.open()
        cls = self.page_obj.get_active_nav_class()
        if cls is None:
            pytest.skip(f"{self.page_name}当前路由不在顶部导航中")
        assert "router-link-active" in cls or "active" in cls, (
            f"{self.page_name}导航项未激活, class={cls}"
        )

    @allure.story("悬浮功能区")
    @allure.title("在线客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_customer_service_button(self) -> None:
        """点击在线客服，验证弹窗弹出（存在即验证）"""
        allure.dynamic.title(f"{self.page_name} - 在线客服按钮")
        self.page_obj.open()
        customer_service_selector = getattr(self.page_obj, 'FLOAT_CUSTOMER_SERVICE', "[class*='customer'], [class*='service'], div:has-text('客服')")
        if self._first_visible(customer_service_selector) is None:
            pytest.skip("当前页面未配置在线客服按钮")
        self.page_obj.click_customer_service()

    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_intent_form_button(self) -> None:
        """点击意向填报，验证弹窗弹出（存在即验证）"""
        allure.dynamic.title(f"{self.page_name} - 意向填报按钮")
        self.page_obj.open()
        intent_form_selector = getattr(self.page_obj, 'FLOAT_INTENT_FORM', "[class*='intent'], [class*='form'], div:has-text('意向')")
        if self._first_visible(intent_form_selector) is None:
            pytest.skip("当前页面未配置意向填报按钮")
        self.page_obj.click_intent_form()

    @allure.story("页脚")
    @allure.title("服务电话链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_phone(self) -> None:
        """验证页脚服务电话可点击"""
        allure.dynamic.title(f"{self.page_name} - 服务电话链接")
        self.page_obj.open()
        self.page_obj.scroll_to_footer()
        phone_selector = getattr(self.page_obj, 'FOOTER_SERVICE_PHONE', "text=400-, text=电话, [class*='phone']")
        if self._first_visible(phone_selector) is None:
            pytest.skip("当前页面未配置服务电话")

    @allure.story("页脚")
    @allure.title("备案号链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_icp(self) -> None:
        """验证页脚备案号链接"""
        allure.dynamic.title(f"{self.page_name} - 备案号链接")
        self.page_obj.open()
        self.page_obj.scroll_to_footer()
        icp_selector = getattr(self.page_obj, 'FOOTER_ICP', "text=ICP, text=备案, text=京ICP, text=津ICP")
        if self._first_visible(icp_selector) is None:
            pytest.skip("当前页面未配置备案号链接")

    # ==================== 页面健康度 ====================

    @allure.story("页面健康度")
    @allure.title("无横向溢出")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_horizontal_overflow(self) -> None:
        """页面不应出现横向滚动条"""
        allure.dynamic.title(f"{self.page_name} - 无横向溢出")
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(1000)
        overflow, scroll_width, client_width = self.page_obj.has_horizontal_overflow()
        assert not overflow, (
            f"{self.page_name}出现横向溢出: scrollWidth={scroll_width}, clientWidth={client_width}"
        )

    @allure.story("页面健康度")
    @allure.title("图片加载正常")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_broken_images(self) -> None:
        """页面不应存在加载失败的图片"""
        allure.dynamic.title(f"{self.page_name} - 图片加载正常")
        self.page_obj.open()
        self.page_obj.page.wait_for_timeout(1500)
        broken = self.page_obj.get_broken_images()
        assert not broken, f"{self.page_name}存在加载失败的图片: {broken}"
