"""
产业金融页面 H5 专项测试（移动端设备仿真，2026-11 改版后）
"""
from __future__ import annotations

import allure
import pytest

from tests.base_page_test import BasePageTest
from pages.finance_page import FinancePage

pytestmark = [pytest.mark.h5, pytest.mark.regression]


@allure.feature("产业金融页面-H5")
class TestFinanceH5(BasePageTest):
    """产业金融页面 H5 测试用例（改版后结构：finance-home-mobile）"""

    page_name = "产业金融"
    page_fixture_name = "h5_finance_page"

    # H5 产业金融首页无顶部导航栏（导航在注册旁菜单图标里）
    EXPECTED_NAV_TEXTS = []
    SKIP_NAV_ACTIVE_ASSERT = True

    # ==================== 金融卡片 ====================

    @allure.story("金融卡片")
    @allure.title("H5 金融卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_finance_cards_display(self) -> None:
        """验证 H5 端金融卡片正常展示（支付担保/农民工工资支付担保/履约担保）"""
        self.page_obj.open()
        self.page_obj.assert_finance_exists(min_count=3)
        titles = self.page_obj.get_finance_titles()
        assert len(titles) >= 3, f"H5 金融卡片标题不足 3 个，实际: {titles}"
        # 改版后卡片标题应为：支付担保、农民工工资支付担保、履约担保
        expected_keywords = ["支付担保", "履约担保"]
        for kw in expected_keywords:
            assert any(kw in t for t in titles), f"H5 金融卡片标题缺少「{kw}」，实际: {titles}"
        self.page_obj.take_screenshot("h5_finance_cards", "info")

    @allure.story("金融卡片")
    @allure.title("H5 金融卡片描述展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_finance_card_descriptions(self) -> None:
        """验证 H5 金融卡片描述非空"""
        self.page_obj.open()
        descs = self.page_obj.get_finance_card_descriptions()
        assert len(descs) >= 3, f"H5 金融卡片描述不足 3 条，实际: {len(descs)}"
        for d in descs:
            assert len(d) > 10, f"H5 金融卡片描述过短: {d!r}"
        self.page_obj.take_screenshot("h5_finance_card_desc", "info")

    @allure.story("金融卡片")
    @allure.title("H5 金融卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_finance_card_click(self) -> None:
        """点击 H5 金融卡片跳转至详情页"""
        self.page_obj.open()
        # H5 滚动容器是内部 div.overflow-y-scroll，需滚动到第一张卡片
        self.page_obj.page.evaluate("""() => {
            const scroller = document.querySelector('.overflow-y-scroll') || document.scrollingElement;
            const card = document.querySelector('.finance-product-card-mobile');
            if (card && scroller) {
                scroller.scrollTop = card.offsetTop - 50;
            }
        }""")
        self.page_obj.page.wait_for_timeout(800)
        # 用 JS click 兜底（卡片可能在视口边缘）
        self.page_obj.page.evaluate("() => document.querySelector('.finance-product-card-mobile')?.click()")
        self.page_obj.wait_for_load()
        self.page_obj.take_screenshot("h5_finance_detail", "info")

    # ==================== 申报入口 ====================

    @allure.story("申报入口")
    @allure.title("H5 立即申请金融产品按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_hero_apply_button(self) -> None:
        """点击 H5 hero 立即申请金融产品按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.H5_HERO_APPLY_BTN, timeout=3000)
        assert btn is not None, "H5 未找到「立即申请金融产品」按钮"
        self.page_obj.click_hero_apply()
        self.page_obj.take_screenshot("h5_hero_apply", "info")

    @allure.story("申报入口")
    @allure.title("H5 立即体验支付担保按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_hero_experience_button(self) -> None:
        """点击 H5 hero 立即体验按钮"""
        self.page_obj.open()
        btn = self.page_obj.first_visible(self.page_obj.H5_HERO_EXPERIENCE_BTN, timeout=3000)
        assert btn is not None, "H5 未找到「立即体验」按钮"
        self.page_obj.click_hero_experience()
        self.page_obj.take_screenshot("h5_hero_experience", "info")

    # ==================== 平台金融服务 ====================

    @allure.story("平台金融服务")
    @allure.title("H5 平台金融服务 tab 展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_platform_finance_tabs(self) -> None:
        """验证 H5 平台金融服务 4 个 tab 均展示"""
        self.page_obj.open()
        tabs = self.page_obj.get_platform_tab_texts()
        assert len(tabs) >= 4, f"H5 平台金融服务 tab 不足 4 个，实际: {tabs}"
        expected = ["电子保函服务", "融资信贷服务", "供应链金融", "意外伤害保险服务"]
        for t in expected:
            assert t in tabs, f"H5 平台金融服务缺少 tab「{t}」，实际: {tabs}"
        self.page_obj.take_screenshot("h5_platform_finance_tabs", "info")

    # ==================== 区块标题 ====================

    @allure.story("页面结构")
    @allure.title("H5 核心区块标题展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_section_titles(self) -> None:
        """验证 H5 核心区块标题均展示"""
        self.page_obj.open()
        body_text = self.page_obj.page.evaluate("() => document.body.textContent || ''")
        for title in self.page_obj.H5_SECTION_TITLES:
            assert title in body_text, f"H5 缺少区块标题「{title}」"
        self.page_obj.take_screenshot("h5_section_titles", "info")

    # ==================== 页脚 ====================

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

    # ==================== 横向溢出 ====================

    @allure.story("布局")
    @allure.title("H5 无横向溢出")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_no_horizontal_overflow(self) -> None:
        """验证 H5 产业金融无横向溢出"""
        self.page_obj.open()
        overflow, sw, cw = self.page_obj.has_horizontal_overflow()
        assert not overflow, f"H5 产业金融存在横向溢出: scrollWidth={sw}, clientWidth={cw}"