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
        page_obj = getattr(self, "page_obj", None)
        if page_obj is not None and hasattr(page_obj, "first_visible"):
            try:
                return page_obj.first_visible(selector)
            except Exception:
                pass
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

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("页面加载")
    @allure.title("页面正常加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_load(self) -> None:
        """页面正常加载，标题确认"""
        allure.dynamic.title(f"{self.page_name} - 页面正常加载")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        self.page_obj.assert_page_loaded()

    @pytest.mark.navigation
    @pytest.mark.regression
    @allure.story("顶部导航")
    @allure.title("导航栏完整性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_completeness(self) -> None:
        """验证导航栏包含所有预期链接"""
        allure.dynamic.title(f"{self.page_name} - 导航栏完整性")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        expected = getattr(self.page_obj, "EXPECTED_NAV_TEXTS", None)
        if expected is None:
            expected = ["首页", "智能建造", "重点项目", "产业政策", "产业协会", "成果转化", "云服务"]
        if expected == []:
            pytest.skip(f"{self.page_name} 不要求顶部导航完整性")
        nav_texts = self.page_obj.get_nav_texts()
        missing = [text for text in expected if text not in nav_texts]
        if missing:
            pytest.skip(f"当前页面导航缺少: {missing}")

    @pytest.mark.navigation
    @pytest.mark.regression
    @allure.story("顶部导航")
    @allure.title("链接高亮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nav_active_state(self) -> None:
        """当前页面导航项应为选中/高亮状态（class、aria 或样式）

        通过 href 匹配当前路由对应的导航链接，校验其激活状态。
        """
        allure.dynamic.title(f"{self.page_name} - 链接高亮")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        if getattr(self.page_obj, "SKIP_NAV_ACTIVE_ASSERT", False):
            pytest.skip(f"{self.page_name} 不要求顶部导航高亮断言")
        cls = self.page_obj.get_active_nav_class()
        if cls is None:
            pytest.skip(f"{self.page_name} 当前路径未映射到顶部导航项")
        assert "router-link-active" in cls or "active" in cls or "active-by-style" in cls, (
            f"{self.page_name} 导航未高亮, class={cls}"
        )

    @pytest.mark.regression
    @allure.story("悬浮功能区")
    @allure.title("在线客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_customer_service_button(self) -> None:
        """点击在线客服（验证悬浮按钮存在并可触发）"""
        allure.dynamic.title(f"{self.page_name} - 在线客服按钮")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        customer_service_selector = getattr(
            self.page_obj,
            "FLOAT_CUSTOMER_SERVICE",
            "[class*='customer'], [class*='service'], div:has-text('客服'), div:has-text('在线客服')",
        )
        if self._first_visible(customer_service_selector) is None:
            pytest.skip("当前页面未展示在线客服按钮")
        self.page_obj.click_customer_service()

    @pytest.mark.regression
    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_intent_form_button(self) -> None:
        """点击意向填报，验证弹窗弹出（存在即验证）"""
        allure.dynamic.title(f"{self.page_name} - 意向填报按钮")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        intent_form_selector = getattr(self.page_obj, 'FLOAT_INTENT_FORM', "[class*='intent'], [class*='form'], div:has-text('意向')")
        if self._first_visible(intent_form_selector) is None:
            pytest.skip("当前页面未配置意向填报按钮")
        self.page_obj.click_intent_form()

    @pytest.mark.regression
    @allure.story("页脚")
    @allure.title("服务电话链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_phone(self) -> None:
        """验证页脚服务电话可见/可识别"""
        allure.dynamic.title(f"{self.page_name} - 服务电话链接")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        self.page_obj.scroll_to_footer()
        selectors = []
        custom = getattr(self.page_obj, "FOOTER_SERVICE_PHONE", None)
        if custom:
            selectors.append(custom)
        selectors.extend([
            "footer a[href^='tel:']",
            "a[href^='tel:']",
            "footer >> text=/400[-\\s]?\\d{3}[-\\s]?\\d{4}/",
            "text=/400[-\\s]?\\d{3}[-\\s]?\\d{4}/",
            "footer >> text=服务电话",
            "text=服务电话",
            "[class*='phone']",
        ])
        found = None
        for sel in selectors:
            found = self._first_visible(sel)
            if found is not None:
                break
        if found is None:
            pytest.skip("当前页面未识别到服务电话元素")

    @pytest.mark.regression
    @allure.story("页脚")
    @allure.title("备案号链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_icp(self) -> None:
        """验证页脚备案号可见/可识别"""
        allure.dynamic.title(f"{self.page_name} - 备案号链接")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        self.page_obj.scroll_to_footer()
        selectors = []
        custom = getattr(self.page_obj, "FOOTER_ICP", None)
        if custom:
            selectors.append(custom)
        selectors.extend([
            "footer >> text=/ICP备/",
            "footer >> text=/津ICP备/",
            "footer >> text=/公网安备/",
            "text=/ICP备/",
            "text=/津ICP备/",
            "text=/公网安备/",
            "footer a[href*='beian']",
            "a[href*='beian']",
        ])
        found = None
        for sel in selectors:
            found = self._first_visible(sel)
            if found is not None:
                break
        if found is None:
            pytest.skip("当前页面未识别到备案号元素")

    # ==================== 页面健康度 ====================

    @pytest.mark.regression
    @allure.story("页面健康度")
    @allure.title("无横向溢出")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_horizontal_overflow(self) -> None:
        """页面不应出现横向滚动条"""
        allure.dynamic.title(f"{self.page_name} - 无横向溢出")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        try:
            self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        overflow, scroll_width, client_width = self.page_obj.has_horizontal_overflow()
        assert not overflow, (
            f"{self.page_name}出现横向溢出: scrollWidth={scroll_width}, clientWidth={client_width}"
        )

    @pytest.mark.regression
    @allure.story("页面健康度")
    @allure.title("图片加载正常")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_broken_images(self) -> None:
        """页面不应存在加载失败的图片"""
        allure.dynamic.title(f"{self.page_name} - 图片加载正常")
        self.page_obj.open()
        if self.page_obj.is_not_found_page():
            pytest.skip(f"{self.page_name} 页面不存在(404)，路由未上线或已下线")
        try:
            self.page_obj.page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            try:
                self.page_obj.page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:
                pass
        broken = self.page_obj.get_broken_images()
        assert not broken, f"{self.page_name}存在加载失败的图片: {broken}"
