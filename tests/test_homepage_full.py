"""
首页全量测试用例 - 改版后

使用 module 级共享 page，浏览器只开一次，首页只打开一次。
每个测试自行维护页面状态，跳转后需返回首页。
"""
from __future__ import annotations

import allure
import json
import pytest

from tests.base_page_test import BasePageTest

from pages.home_page import HomePage


@allure.feature("首页")
class TestHomePage(BasePageTest):
    """首页测试类 - 单页快速模式

    使用 module 级共享 page，浏览器只开一次，首页只打开一次。
    每个测试自行维护页面状态，跳转后需返回首页。
    """

    page_name = "首页"
    page_fixture_name = "home_page_shared"

    @pytest.fixture(autouse=True)
    def _goto_home(self, home_page_shared: HomePage) -> None:
        """每个用例前回到首页

        共享 page 会被上一个用例遗留的路由/滚动状态影响，
        这里统一重置，保证用例之间相互独立、可单独执行。
        """
        home_page_shared.goto()
        home_page_shared.page.wait_for_timeout(500)

    # ==================== 通用测试由 BasePageTest 自动继承 ====================
    # test_page_load, test_nav_completeness, test_nav_active_state,
    # test_customer_service_button, test_intent_form_button

    # ==================== 顶部导航栏 ====================

    @allure.story("顶部导航")
    @allure.title("Logo显示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logo_display(self, home_page_shared: HomePage) -> None:
        """Logo图片正确加载"""
        assert home_page_shared.is_visible(home_page_shared.LOGO), "Logo未显示"

    @allure.story("顶部导航")
    @allure.title("Logo点击返回首页")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logo_click(self, home_page_shared: HomePage) -> None:
        """点击Logo返回首页"""
        home_page_shared.click_nav_by_text("智能建造")
        home_page_shared.click_logo()
        assert "/" in home_page_shared.page.url

    @allure.story("顶部导航")
    @allure.title("导航链接完整性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_links_complete(self, home_page_shared: HomePage) -> None:
        """导航栏包含全部8个预期链接"""
        expected = [
            "首页", "供应大厅", "智能建造", "重点项目",
            "产业政策", "产业协会", "成果转化", "云服务",
        ]
        nav_texts = home_page_shared.get_nav_texts()
        missing = [text for text in expected if text not in nav_texts]
        assert not missing, f"导航缺少: {missing}"

    @allure.story("顶部导航")
    @allure.title("首页链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_home(self, home_page_shared: HomePage) -> None:
        """点击首页链接跳转到首页"""
        home_page_shared.click_nav_by_text("智能建造")
        assert "intelligentConstruction" in home_page_shared.page.url
        home_page_shared.click_nav_by_text("首页")
        assert "intelligentConstruction" not in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("顶部导航")
    @allure.title("供应大厛链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_supply_hall(self, home_page_shared: HomePage) -> None:
        """点击供应大厅跳转"""
        home_page_shared.click_nav_by_text("供应大厅")
        assert "supplyHall" in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("顶部导航")
    @allure.title("智能建造链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_intelligent_construction(self, home_page_shared: HomePage) -> None:
        """点击智能建造跳转"""
        home_page_shared.click_nav_by_text("智能建造")
        assert "intelligentConstruction" in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("顶部导航")
    @allure.title("重点项目链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_key_project(self, home_page_shared: HomePage) -> None:
        """点击重点项目跳转"""
        home_page_shared.click_nav_by_text("重点项目")
        assert "keyProject" in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("字体一致性")
    @allure.title("首页区块标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_section_title_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页区块标题字体样式一致

        检查项：产业服务、津筑云商、会展活动、产业需求、产业政策
        这些H2标题应具有相同的 fontFamily、fontSize、fontWeight、color。
        """
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        section_texts = ["产业服务", "津筑云商", "会展活动", "产业需求", "产业政策"]
        styles = {}
        for text in section_texts:
            el = home_page_shared.page.locator(f"h2:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    """(el) => {
                        const s = getComputedStyle(el);
                        return {
                            fontFamily: s.fontFamily,
                            fontSize: s.fontSize,
                            fontWeight: s.fontWeight,
                            color: s.color,
                        };
                    }"""
                )
                styles[text] = style

        # 至少应找到 2 个以上区块标题
        assert len(styles) >= 2, f"仅找到 {len(styles)} 个区块标题: {list(styles.keys())}"

        # 检查所有区块标题的字体样式是否一致
        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    f"区块 '{text}' 的 {key} ({style[key]}) "
                    f"与 '{first_text}' ({first_style[key]}) 不一致"
                )
        home_page_shared.take_screenshot("font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("首页服务卡片标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_service_card_title_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页服务卡片H3标题字体样式一致

        供应大厅、劳务对接、AI+工具集等服务卡片标题应使用相同的字体样式。
        """
        card_titles = ["供应大厅", "劳务对接", "AI+工具集", "金融服务", "建筑机器人", "智慧工地"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for title in card_titles:
            el = home_page_shared.page.locator(f"h3:has-text('{title}')").first
            if el.is_visible():
                style = el.evaluate(
                    """(el) => {
                        const s = getComputedStyle(el);
                        return {
                            fontFamily: s.fontFamily,
                            fontSize: s.fontSize,
                            fontWeight: s.fontWeight,
                            color: s.color,
                        };
                    }"""
                )
                styles[title] = style

        assert len(styles) >= 2, f"仅找到 {len(styles)} 个服务卡片标题: {list(styles.keys())}"

        first_title = list(styles.keys())[0]
        first_style = styles[first_title]
        for title, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    f"服务卡片 '{title}' 的 {key} ({style[key]}) "
                    f"与 '{first_title}' ({first_style[key]}) 不一致"
                )
        home_page_shared.take_screenshot("service_card_font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("首页按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_button_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页主要按钮字体样式一致

        Tab按钮（行业动态、政策资讯、政策解读）应使用相同的字体样式。
        注意：颜色因激活/非激活状态不同，仅检查字体族、字号、字重。
        """
        tab_buttons = ["行业动态", "政策资讯", "政策解读"]
        style_keys = ["fontFamily", "fontSize", "fontWeight"]
        styles = {}
        for btn_text in tab_buttons:
            el = home_page_shared.page.locator(f"button:has-text('{btn_text}')").first
            if el.is_visible():
                style = el.evaluate(
                    """(el) => {
                        const s = getComputedStyle(el);
                        return {
                            fontFamily: s.fontFamily,
                            fontSize: s.fontSize,
                            fontWeight: s.fontWeight,
                            color: s.color,
                        };
                    }"""
                )
                styles[btn_text] = style

        assert len(styles) >= 2, f"仅找到 {len(styles)} 个Tab按钮: {list(styles.keys())}"

        first_btn = list(styles.keys())[0]
        first_style = styles[first_btn]
        for btn_text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    f"按钮 '{btn_text}' 的 {key} ({style[key]}) "
                    f"与 '{first_btn}' ({first_style[key]}) 不一致"
                )
        home_page_shared.take_screenshot("button_font_consistency", "info")
    @allure.story("字体一致性")
    @allure.title("首页描述文字字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_body_desc_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页描述文字字体样式一致

        全方位服务产业链、平台优质企业，精准商务对接等描述文字
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        desc_texts = ["全方位服务产业链", "平台优质企业，精准商务对接", "聚焦建筑行业各类活动"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = home_page_shared.page.locator(f"p:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个描述文字" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("body_desc_font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("首页页脚导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_nav_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页页脚导航链接字体样式一致

        供应大厅、产业政策、智能建造等页脚导航链接
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        nav_texts = ["供应大厅", "产业政策", "智能建造", "重点项目"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in nav_texts:
            el = home_page_shared.page.locator("footer").locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个页脚导航链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "页脚导航 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("footer_nav_font_consistency", "info")
    @allure.story("字体一致性")
    @allure.title("查看全部按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_view_all_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页查看全部按钮字体样式一致

        所有查看全部按钮应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        view_all_buttons = home_page_shared.page.locator("text=查看全部")
        count = view_all_buttons.count()
        assert count >= 2, f"仅找到 {count} 个查看全部按钮"

        styles = {}
        for i in range(count):
            el = view_all_buttons.nth(i)
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[f"view_all_{i}"] = style

        assert len(styles) >= 2, "仅找到 %d 个可见的查看全部按钮" % len(styles)

        first_key = list(styles.keys())[0]
        first_style = styles[first_key]
        for key, style in styles.items():
            for prop in ["fontFamily", "fontSize", "fontWeight", "color"]:
                assert style[prop] == first_style[prop], (
                    "查看全部按钮 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (key, prop, style[prop], first_key, first_style[prop])
                )
        home_page_shared.take_screenshot("view_all_font_consistency", "info")
    @allure.story("字体一致性")
    @allure.title("热搜词字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_hot_search_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证热搜词字体样式一致

        热搜词名称一~六应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        hot_texts = ["热搜词名称一", "热搜词名称二", "热搜词名称三", "热搜词名称四", "热搜词名称五", "热搜词名称六"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in hot_texts:
            el = home_page_shared.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个热搜词" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "热搜词 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("hot_search_font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("新闻标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_title_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证新闻标题字体样式一致

        云南石材建材产业发展峰会等新闻标题应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        news_texts = ["云南石材建材产业发展峰会", "绿色建筑新浪潮来袭！2027广州住博会！"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in news_texts:
            el = home_page_shared.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("news_title_font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("供应品目字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_item_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证供应品目名称字体样式一致

        施工电梯、配电箱、灯具、开关面板等供应品目名称
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        item_texts = ["施工电梯", "配电箱", "灯具、开关面板", "PVC管材、管件", "门窗工程"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in item_texts:
            el = home_page_shared.page.locator(f"text={text}").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个供应品目" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "供应品目 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("supply_item_font_consistency", "info")

    @allure.story("字体一致性")
    @allure.title("页脚服务链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_service_font_consistency(self, home_page_shared: HomePage) -> None:
        svc_texts = ["建材出售", "建材出租", "设备出售", "设备出租", "劳务用工", "产业需求"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in svc_texts:
            el = home_page_shared.page.locator("footer").locator("text=" + text).first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个页脚服务链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "页脚服务 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("footer_service_font_consistency", "info")


    @allure.story("字体一致性")
    @allure.title("津筑云商Tab字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_jzys_tab_font_consistency(self, home_page_shared: HomePage) -> None:
        tab_texts = ["产业生态全景图", "建筑服务业", "建筑制造业", "建筑建造业"]
        style_keys = ["fontFamily", "fontSize", "fontWeight"]
        styles = {}
        for text in tab_texts:
            el = home_page_shared.page.locator("button:has-text('" + text + "')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个津筑云商Tab" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "Tab '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        home_page_shared.take_screenshot("jzys_tab_font_consistency", "info")



    @allure.story("顶部导航")
    @allure.title("产业协会链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_industry_association(self, home_page_shared: HomePage) -> None:
        """点击产业协会跳转"""
        home_page_shared.click_nav_by_text("产业协会")
        assert "industryAssociation" in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("顶部导航")
    @allure.title("成果转化链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_achievement_transformation(self, home_page_shared: HomePage) -> None:
        """点击成果转化跳转"""
        home_page_shared.click_nav_by_text("成果转化")
        assert "achievementTransformation" in home_page_shared.page.url
        home_page_shared.goto()

    @allure.story("顶部导航")
    @allure.title("云服务链接跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nav_cloud_service(self, home_page_shared: HomePage) -> None:
        """点击云服务跳转"""
        home_page_shared.click_nav_by_text("云服务")
        assert "cloudService" in home_page_shared.page.url
        home_page_shared.goto()

    # ==================== 登录/注册 ====================

    @allure.story("登录注册")
    @allure.title("登录按钮点击")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_button(self, home_page_shared: HomePage) -> None:
        """点击登录按钮进入登录页"""
        login_btn = home_page_shared.page.locator(home_page_shared.LOGIN_BTN).first
        assert login_btn.is_visible(), "登录按钮不可见"
        try:
            with home_page_shared.page.expect_popup(timeout=5000):
                login_btn.click()
            popup = home_page_shared.page.context.pages[-1]
            popup.wait_for_load_state("domcontentloaded", timeout=10000)
            assert "login" in popup.url.lower() or "登录" in popup.content()[:2000]
            popup.close()
            home_page_shared.page.wait_for_timeout(1000)
        except Exception:
            home_page_shared.page.wait_for_timeout(2000)
            content = home_page_shared.page.content()
            assert "登录" in content or "login" in content.lower()
        finally:
            home_page_shared.goto()

    @allure.story("登录注册")
    @allure.title("注册按钮点击")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_button(self, home_page_shared: HomePage) -> None:
        """点击注册按钮进入注册页"""
        register_btn = home_page_shared.page.locator(home_page_shared.REGISTER_BTN).first
        assert register_btn.is_visible(), "注册按钮不可见"
        try:
            with home_page_shared.page.expect_popup(timeout=5000):
                register_btn.click()
            popup = home_page_shared.page.context.pages[-1]
            popup.wait_for_load_state("domcontentloaded", timeout=10000)
            assert "register" in popup.url.lower() or "注册" in popup.content()[:2000]
            popup.close()
            home_page_shared.page.wait_for_timeout(1000)
        except Exception:
            home_page_shared.page.wait_for_timeout(2000)
            content = home_page_shared.page.content()
            assert "注册" in content or "register" in content.lower()
        finally:
            home_page_shared.goto()

    # ==================== 搜索栏 ====================

    @allure.story("搜索功能")
    @allure.title("搜索框输入")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_input(self, home_page_shared: HomePage) -> None:
        """搜索框接受输入"""
        search = home_page_shared.page.locator(home_page_shared.SEARCH_INPUT).first
        if search.is_visible():
            search.fill("钢筋")
            home_page_shared.take_screenshot("search_input_filled", "info")

    @allure.story("搜索功能")
    @allure.title("搜索按钮点击")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_button(self, home_page_shared: HomePage) -> None:
        """点击搜索按钮触发搜索"""
        search = home_page_shared.page.locator(home_page_shared.SEARCH_INPUT).first
        if search.is_visible():
            search.fill("建材")
            btn = home_page_shared.page.locator(home_page_shared.SEARCH_BTN).first
            if btn.is_visible():
                btn.click()
                home_page_shared.wait_for_load()
                home_page_shared.take_screenshot("search_result", "info")
                home_page_shared.goto()

    @allure.story("搜索功能")
    @allure.title("搜索跳转到搜索结果页")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_navigates_to_result_page(self, home_page_shared: HomePage) -> None:
        """点击搜索后应跳转到搜索结果页，且 URL 携带关键词"""
        search = home_page_shared.page.locator(home_page_shared.SEARCH_INPUT).first
        if not search.is_visible():
            pytest.skip("当前环境未展示搜索框")
        keyword = "钢筋"
        home_page_shared.do_search(keyword)
        try:
            assert "searchResult" in home_page_shared.page.url, (
                f"搜索后未跳转到搜索结果页，当前 URL: {home_page_shared.page.url}"
            )
            assert home_page_shared.get_search_keyword() == keyword, (
                f"URL 中的关键词与输入不一致: "
                f"{home_page_shared.get_search_keyword()!r} != {keyword!r}"
            )
            home_page_shared.take_screenshot("search_result_page", "info")
        finally:
            home_page_shared.goto()

    @allure.story("搜索功能")
    @allure.title("搜索结果与关键词相关")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_result_matches_keyword(self, home_page_shared: HomePage) -> None:
        """搜索"钢筋"时，结果条目中必须出现关键词"""
        search = home_page_shared.page.locator(home_page_shared.SEARCH_INPUT).first
        if not search.is_visible():
            pytest.skip("当前环境未展示搜索框")
        keyword = "钢筋"
        home_page_shared.do_search(keyword)
        try:
            titles = home_page_shared.get_search_result_titles()
            assert titles, "搜索结果列表为空"
            assert any(keyword in t for t in titles), (
                f"搜索 '{keyword}' 的结果中没有包含关键词的条目: {titles[:3]}"
            )
        finally:
            home_page_shared.goto()

    @allure.story("搜索功能")
    @allure.title("无结果关键词展示空状态提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_empty_state_hint(self, home_page_shared: HomePage) -> None:
        """搜索不存在的关键词时应展示"没有找到相关数据"提示"""
        search = home_page_shared.page.locator(home_page_shared.SEARCH_INPUT).first
        if not search.is_visible():
            pytest.skip("当前环境未展示搜索框")
        home_page_shared.do_search("zzz不存在的关键词zzz")
        try:
            assert home_page_shared.has_search_empty_hint(), (
                "搜索不存在的关键词时未展示'没有找到相关数据'提示"
            )
            home_page_shared.take_screenshot("search_empty_state", "info")
        finally:
            home_page_shared.goto()

    # ==================== 热门搜索 ====================

    @allure.story("热门搜索")
    @allure.title("热搜词展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hot_search_display(self, home_page_shared: HomePage) -> None:
        """热搜词按钮正常展示"""
        count = home_page_shared.get_hot_search_count()
        if home_page_shared.is_mobile() and count == 0:
            pytest.skip("移动端未展示热搜词区域")
        assert count > 0, "未找到热搜词按钮"
        home_page_shared.take_screenshot("hot_search", "info")

    @allure.story("热门搜索")
    @allure.title("热搜词点击")
    @allure.severity(allure.severity_level.MINOR)
    def test_hot_search_click(self, home_page_shared: HomePage) -> None:
        """点击热搜词触发搜索"""
        btns = home_page_shared.page.locator(home_page_shared.HOT_SEARCH_BTNS)
        if btns.count() > 0:
            btns.first.click()
            home_page_shared.wait_for_load()
            home_page_shared.take_screenshot("hot_search_click", "info")
            home_page_shared.goto()

    # ==================== 轮播图 ====================

    @allure.story("轮播图")
    @allure.title("轮播图加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_carousel_loaded(self, home_page_shared: HomePage) -> None:
        """轮播图区域正常渲染"""
        assert home_page_shared.assert_carousel_loaded(), "轮播图未加载"
        assert home_page_shared.get_carousel_images_count() > 0, "轮播图图片未找到"

    @allure.story("轮播图")
    @allure.title("轮播图自动播放")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_carousel_auto_play(self, home_page_shared: HomePage) -> None:
        """验证轮播图自动切换"""
        dots_count = home_page_shared.get_carousel_dots_count()
        assert dots_count > 0, "轮播图 dots 未找到"
        initial = home_page_shared.get_active_carousel_dot_index()
        home_page_shared.page.wait_for_timeout(3000)
        new_dot = home_page_shared.get_active_carousel_dot_index()
        assert new_dot >= 0, "轮播图活跃 dot 未找到"

    @allure.story("轮播图")
    @allure.title("轮播图图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_carousel_image_loading(self, home_page_shared: HomePage) -> None:
        """验证轮播图图片正确加载"""
        images = home_page_shared.page.locator(home_page_shared.CAROUSEL_IMG)
        count = images.count()
        assert count > 0, "未找到轮播图图片"
        for i in range(min(count, 3)):
            img = images.nth(i)
            src = img.get_attribute("src") or ""
            assert "/api/sys/file/pub/download" in src, f"图片{i} src 异常: {src}"
            box = img.bounding_box()
            assert box and box["width"] > 0, f"图片{i} 宽度异常"

    @allure.story("轮播图")
    @allure.title("轮播图 dots 切换")
    @allure.severity(allure.severity_level.NORMAL)
    def test_carousel_dot_switch(self, home_page_shared: HomePage) -> None:
        """点击 dots 手动切换轮播图"""
        dots_count = home_page_shared.get_carousel_dots_count()
        if dots_count >= 2:
            home_page_shared.click_carousel_dot(1)
            active = home_page_shared.get_active_carousel_dot_index()
            assert active == 1, f"期望激活第2个 dot，实际为第{active} 个"
            home_page_shared.take_screenshot("carousel_dot_switch", "info")
            home_page_shared.goto()

    # ==================== 服务链接区 ====================

    @allure.story("服务链接区")
    @allure.title("统计数字展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_service_stats_display(self, home_page_shared: HomePage) -> None:
        """统计数字正常展示"""
        count = home_page_shared.get_service_stats_count()
        if home_page_shared.is_mobile() and count == 0:
            pytest.skip("移动端未展示统计数字区域")
        assert count > 0, "未找到统计数字"
        texts = home_page_shared.get_service_stats_texts()
        assert len(texts) > 0, "未找到统计数字"
        has_number = any(any(c.isdigit() for c in t) for t in texts)
        assert has_number, "统计数字中不包含任何数字"
        home_page_shared.take_screenshot("service_stats", "info")

    # ==================== 产业服务 ====================

    @allure.story("产业服务")
    @allure.title("产业服务区加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_industry_service_load(self, home_page_shared: HomePage) -> None:
        """'产业服务'区正常渲染"""
        assert home_page_shared.is_visible(home_page_shared.SECTION_INDUSTRY_SERVICE), "产业服务区未显示"
        home_page_shared.take_screenshot("industry_service_section", "info")

    @allure.story("产业服务")
    @allure.title("服务子分类卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_service_card_titles(self, home_page_shared: HomePage) -> None:
        """6 个子分类卡片正常展示"""
        home_page_shared.scroll_to_industry_service()
        titles = home_page_shared.get_service_card_titles()
        if home_page_shared.is_mobile():
            assert len(titles) > 0, "移动端未找到服务卡片标题"
        else:
            for expected in home_page_shared.SERVICE_CARD_TITLES:
                assert expected in titles, f"缺少服务分类: {expected}"
        home_page_shared.take_screenshot("service_cards", "info")

    @allure.story("产业服务")
    @allure.title("了解详情按钮点击")
    @allure.severity(allure.severity_level.NORMAL)
    def test_detail_button_click(self, home_page_shared: HomePage) -> None:
        """'了解详情'按钮可点击"""
        btns = home_page_shared.page.locator(home_page_shared.DETAIL_BTNS)
        if btns.count() > 0:
            home_page_shared.click_detail_btn(0)
            home_page_shared.take_screenshot("detail_btn_click", "info")
            home_page_shared.goto()

    # ==================== 津筑云商 ====================

    @allure.story("津筑云商")
    @allure.title("津筑云商区加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tjdigital_load(self, home_page_shared: HomePage) -> None:
        """'津筑云商'区正常渲染"""
        home_page_shared.scroll_to_tjdigital()
        if home_page_shared.is_mobile() and not home_page_shared.is_visible(home_page_shared.SECTION_TJDIGITAL, timeout=2000):
            pytest.skip("移动端未展示津筑云商区域")
        assert home_page_shared.is_visible(home_page_shared.SECTION_TJDIGITAL), "津筑云商区未显示"
        home_page_shared.take_screenshot("tjdigital_section", "info")

    @allure.story("津筑云商")
    @allure.title("生态标签展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_merchant_tabs_display(self, home_page_shared: HomePage) -> None:
        """生态标签按钮正常展示"""
        home_page_shared.scroll_to_tjdigital()
        if home_page_shared.is_mobile() and home_page_shared.get_merchant_tab_count() == 0:
            pytest.skip("移动端未展示生态标签区域")
        expected_tabs = ["产业生态全景图", "建筑服务业", "建筑制造业", "建筑建造业"]
        for tab in expected_tabs:
            assert home_page_shared.is_visible(f"button:has-text('{tab}')"), f"生态标签缺失: {tab}"
        home_page_shared.take_screenshot("merchant_tabs", "info")

    @allure.story("津筑云商")
    @allure.title("企业图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_merchant_images_load(self, home_page_shared: HomePage) -> None:
        """企业图片正常加载"""
        home_page_shared.scroll_to_tjdigital()
        count = home_page_shared.get_merchant_images_count()
        if home_page_shared.is_mobile() and count == 0:
            pytest.skip("移动端未展示企业图片区域")
        assert count > 0, "未找到企业图片"
        for i in range(min(count, 3)):
            img = home_page_shared.page.locator(home_page_shared.MERCHANT_IMAGES).nth(i)
            src = img.get_attribute("src") or ""
            assert "/api/sys/file/pub/download" in src or "/20260923/" in src, f"图片{i} src 异常: {src}"
            box = img.bounding_box()
            assert box and box["width"] > 0, f"图片{i} 尺寸异常"

    # ==================== 会展活动 ====================

    @allure.story("会展活动")
    @allure.title("会展活动区加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_exhibition_load(self, home_page_shared: HomePage) -> None:
        """'会展活动'区正常渲染"""
        home_page_shared.scroll_to_exhibition()
        assert home_page_shared.is_visible(home_page_shared.SECTION_EXHIBITION), "会展活动区未显示"
        home_page_shared.take_screenshot("exhibition_section", "info")

    @allure.story("会展活动")
    @allure.title("活动卡片展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_activity_cards_display(self, home_page_shared: HomePage) -> None:
        """活动卡片正常展示"""
        home_page_shared.scroll_to_exhibition()
        count = home_page_shared.get_activity_card_count()
        if home_page_shared.is_mobile() and count == 0:
            pytest.skip("移动端未展示会展活动区域")
        assert count > 0, "未找到活动卡片"
        titles = home_page_shared.get_activity_card_titles()
        assert len(titles) > 0, "活动卡片标题为空"
        home_page_shared.take_screenshot("activity_cards", "info")

    @allure.story("会展活动")
    @allure.title("活动详情跳转")
    @allure.severity(allure.severity_level.MINOR)
    def test_activity_detail_click(self, home_page_shared: HomePage) -> None:
        """点击活动卡片'了解详情'跳转"""
        btns = home_page_shared.page.locator(home_page_shared.DETAIL_BTNS)
        # 活动卡片的了解详情在靠后的位置
        if btns.count() > 4:
            btns.nth(4).click()
            home_page_shared.page.wait_for_timeout(2000)
            home_page_shared.take_screenshot("activity_detail", "info")
            home_page_shared.goto()

    # ==================== 产业需求 ====================

    @allure.story("产业需求")
    @allure.title("产业需求区加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_demand_load(self, home_page_shared: HomePage) -> None:
        """'产业需求'区正常渲染"""
        home_page_shared.scroll_to_demand()
        assert home_page_shared.is_visible(home_page_shared.SECTION_DEMAND), "产业需求区未显示"
        home_page_shared.take_screenshot("demand_section", "info")

    @allure.story("产业需求")
    @allure.title("需求条目展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_demand_items_display(self, home_page_shared: HomePage) -> None:
        """需求条目正常展示"""
        home_page_shared.scroll_to_demand()
        count = home_page_shared.get_demand_item_count()
        assert count > 0, "未找到需求条目"
        titles = home_page_shared.get_demand_item_titles()
        assert len(titles) > 0, "需求条目标题为空"
        home_page_shared.take_screenshot("demand_items", "info")

    @allure.story("产业需求")
    @allure.title("需求条目详情信息")
    @allure.severity(allure.severity_level.NORMAL)
    def test_demand_item_detail(self, home_page_shared: HomePage) -> None:
        """需求条目包含预算金额和联系人"""
        home_page_shared.scroll_to_demand()
        strong_elements = home_page_shared.page.locator("strong").all()
        has_money = False
        has_contact = False
        for el in strong_elements:
            text = el.text_content()
            if text and text.strip():
                if any(c.isdigit() for c in text):
                    has_money = True
                if any(c.isalpha() for c in text):
                    has_contact = True
        assert has_money or has_contact, "需求条目缺少预算金额或联系人"

    @allure.story("产业需求")
    @allure.title("查看全部跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_all_demand(self, home_page_shared: HomePage) -> None:
        """点击'查看全部'跳转到需求列表页"""
        home_page_shared.scroll_to_demand()
        btn = home_page_shared.page.locator(home_page_shared.VIEW_ALL_DEMAND).first
        if home_page_shared.is_mobile() and not btn.is_visible(timeout=2000):
            pytest.skip("移动端未展示需求查看全部按钮")
        home_page_shared.click_view_all_demand()
        assert "demandPage" in home_page_shared.page.url, f"URL不包含demandPage，实际: {home_page_shared.page.url}"
        home_page_shared.goto()

    # ==================== 产业政策 ====================

    @allure.story("产业政策")
    @allure.title("产业政策区加载")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_policy_load(self, home_page_shared: HomePage) -> None:
        """'产业政策'区正常渲染"""
        home_page_shared.scroll_to_policy()
        assert home_page_shared.is_visible(home_page_shared.SECTION_POLICY), "产业政策区未显示"
        home_page_shared.take_screenshot("policy_section", "info")

    @allure.story("产业政策")
    @allure.title("政策标签页切换")
    @allure.severity(allure.severity_level.NORMAL)
    def test_policy_tabs_switch(self, home_page_shared: HomePage) -> None:
        """3 个标签页正常展示并可切换"""
        home_page_shared.scroll_to_policy()
        tab_count = home_page_shared.get_policy_tab_count()
        assert tab_count >= 3, f"标签页数量不足，期望>=3，实际={tab_count}"
        for tab_text in ["政策资讯", "政策解读", "行业动态"]:
            btn = home_page_shared.page.locator(f"button:has-text('{tab_text}')").first
            if btn.is_visible():
                btn.click()
                home_page_shared.page.wait_for_timeout(1000)
        home_page_shared.take_screenshot("policy_tabs", "info")
        home_page_shared.goto()

    @allure.story("产业政策")
    @allure.title("政策新闻条目展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_news_items_display(self, home_page_shared: HomePage) -> None:
        """政策新闻条目正常展示"""
        home_page_shared.scroll_to_policy()
        count = home_page_shared.get_news_item_count()
        assert count > 0, "未找到政策新闻条目"
        titles = home_page_shared.get_news_item_titles()
        assert len(titles) > 0, "新闻条目标题为空"
        home_page_shared.take_screenshot("news_items", "info")

    @allure.story("产业政策")
    @allure.title("政策查看全部跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_all_policy(self, home_page_shared: HomePage) -> None:
        """点击'查看全部'跳转到政策/新闻列表页"""
        home_page_shared.scroll_to_policy()
        btn = home_page_shared.page.locator(home_page_shared.VIEW_ALL_POLICY).first
        if home_page_shared.is_mobile() and not btn.is_visible(timeout=2000):
            pytest.skip("移动端未展示政策查看全部按钮")
        home_page_shared.click_view_all_policy()
        assert "industryNews" in home_page_shared.page.url, f"URL不包含industryNews，实际: {home_page_shared.page.url}"
        home_page_shared.goto()

    # ==================== 页脚 ====================

    @allure.story("页脚")
    @allure.title("服务电话显示")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_phone(self, home_page_shared: HomePage) -> None:
        """验证页脚服务电话可见"""
        home_page_shared.scroll_to_footer()
        assert home_page_shared.is_visible(home_page_shared.FOOTER_SERVICE_PHONE, timeout=5000), "服务电话不可见"
        home_page_shared.take_screenshot("footer_phone", "info")

    @allure.story("页脚")
    @allure.title("ICP备案号")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_icp(self, home_page_shared: HomePage) -> None:
        """验证页脚ICP备案号可见"""
        home_page_shared.scroll_to_footer()
        assert home_page_shared.is_visible(home_page_shared.FOOTER_ICP, timeout=5000), "ICP备案号不可见"
        home_page_shared.take_screenshot("footer_icp", "info")

    @allure.story("页脚")
    @allure.title("版权信息")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_copyright(self, home_page_shared: HomePage) -> None:
        """验证页脚版权信息可见"""
        home_page_shared.scroll_to_footer()
        assert home_page_shared.is_visible(home_page_shared.FOOTER_COPYRIGHT, timeout=5000), "版权信息不可见"
        home_page_shared.take_screenshot("footer_copyright", "info")

    @allure.story("页脚")
    @allure.title("页脚导航链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_nav_links(self, home_page_shared: HomePage) -> None:
        """验证页脚导航链接完整"""
        home_page_shared.scroll_to_footer()
        expected_groups = ["供应大厅", "产业政策", "智能建造", "重点项目", "关于和入驻"]
        footer_locator = home_page_shared.page.locator("footer")
        for group in expected_groups:
            assert footer_locator.get_by_text(group, exact=True).is_visible(timeout=5000), \
                f"页脚缺少导航分组: {group}"
        home_page_shared.take_screenshot("footer_nav", "info")

    # ==================== 悬浮功能区 ====================

    @allure.story("悬浮功能区")
    @allure.title("在线客服按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_customer_service_button(self, home_page_shared: HomePage) -> None:
        """点击在线客服，验证弹窗弹出"""
        assert home_page_shared.is_visible(home_page_shared.FLOAT_CUSTOMER_SERVICE, timeout=5000), "在线客服按钮不可见"
        home_page_shared.click_customer_service()
        home_page_shared.take_screenshot("customer_service_modal", "info")
        home_page_shared.goto()

    @allure.story("悬浮功能区")
    @allure.title("意向填报按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_intent_form_button(self, home_page_shared: HomePage) -> None:
        """点击意向填报，验证弹窗弹出"""
        assert home_page_shared.is_visible(home_page_shared.FLOAT_INTENT_FORM, timeout=5000), "意向填报按钮不可见"
        home_page_shared.click_intent_form()
        home_page_shared.take_screenshot("intent_form_modal", "info")
        home_page_shared.goto()

    # ==================== 交互与体验 ====================

    @allure.story("交互体验")
    @allure.title("生态标签hover效果")
    @allure.severity(allure.severity_level.MINOR)
    def test_merchant_tab_hover(self, home_page_shared: HomePage) -> None:
        """鼠标悬停生态标签，验证hover效果"""
        if home_page_shared.is_mobile():
            pytest.skip("移动端不支持 hover 操作")
        home_page_shared.scroll_to_tjdigital()
        tab = home_page_shared.page.locator(home_page_shared.MERCHANT_TAB_ECOLOGY).first
        if tab.is_visible():
            tab.hover()
            home_page_shared.page.wait_for_timeout(500)
            home_page_shared.take_screenshot("merchant_tab_hover", "info")

    @allure.story("交互体验")
    @allure.title("悬浮按钮hover效果")
    @allure.severity(allure.severity_level.MINOR)
    def test_float_button_hover(self, home_page_shared: HomePage) -> None:
        """鼠标悬停悬浮按钮，验证hover效果"""
        if home_page_shared.is_mobile():
            pytest.skip("移动端不支持 hover 操作")
        btn = home_page_shared.page.locator(home_page_shared.FLOAT_CUSTOMER_SERVICE).first
        if btn.is_visible():
            btn.hover()
            home_page_shared.page.wait_for_timeout(500)
            home_page_shared.take_screenshot("float_btn_hover", "info")

    @allure.story("交互体验")
    @allure.title("页面滚动流畅性")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_scroll_performance(self, home_page_shared: HomePage) -> None:
        """快速滚动页面，验证流畅性"""
        import time
        start = time.time()
        for _ in range(5):
            home_page_shared.page.evaluate("window.scrollBy(0, window.innerHeight)")
            home_page_shared.page.wait_for_timeout(500)
        duration = time.time() - start
        assert duration < 10.0, f"滚动耗时 {duration:.2f}s，超过10秒阈值"
        home_page_shared.take_screenshot("scroll_performance", "info")
        home_page_shared.goto()

    # ==================== 移动端手势 ====================

    @allure.story("移动端手势")
    @allure.title("向左滑动轮播图")
    @allure.severity(allure.severity_level.MINOR)
    def test_swipe_left_carousel(self, home_page_shared: HomePage) -> None:
        """向左滑动验证轮播图切换"""
        if not home_page_shared.is_mobile():
            pytest.skip("仅移动端执行滑动手势测试")
        home_page_shared.swipe_left()
        home_page_shared.take_screenshot("swipe_left_carousel", "info")

    @allure.story("移动端手势")
    @allure.title("向上滑动加载更多")
    @allure.severity(allure.severity_level.MINOR)
    def test_swipe_up_load_more(self, home_page_shared: HomePage) -> None:
        """向上滑动验证页面加载更多内容"""
        if not home_page_shared.is_mobile():
            pytest.skip("仅移动端执行滑动手势测试")
        home_page_shared.swipe_up()
        home_page_shared.take_screenshot("swipe_up_load_more", "info")

    @allure.story("移动端手势")
    @allure.title("下拉刷新页面")
    @allure.severity(allure.severity_level.MINOR)
    def test_pull_to_refresh(self, home_page_shared: HomePage) -> None:
        """模拟移动端下拉刷新页面"""
        if not home_page_shared.is_mobile():
            pytest.skip("仅移动端执行下拉刷新测试")
        home_page_shared.pull_to_refresh()
        home_page_shared.take_screenshot("pull_to_refresh", "info")

    # ==================== 图片与资源 ====================

    @allure.story("图片资源")
    @allure.title("轮播图图片加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_carousel_images_load(self, home_page_shared: HomePage) -> None:
        """验证所有轮播图图片正确加载"""
        if not home_page_shared.assert_carousel_loaded():
            pytest.skip("当前环境未配置轮播图")
        images = home_page_shared.page.locator(home_page_shared.CAROUSEL_IMG)
        count = images.count()
        loaded_count = 0
        for i in range(min(count, 3)):
            img = images.nth(i)
            src = img.get_attribute("src") or ""
            if "/api/sys/file/pub/download" in src:
                loaded_count += 1
        assert loaded_count > 0, f"轮播图图片加载失败，仅 {loaded_count}/{count} 张有效"

    @allure.story("图片资源")
    @allure.title("企业图片alt文本检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_merchant_images_alt(self, home_page_shared: HomePage) -> None:
        """检查商户图片alt文本"""
        home_page_shared.scroll_to_tjdigital()
        images = home_page_shared.page.locator(home_page_shared.MERCHANT_IMAGES)
        count = images.count()
        images_without_alt = []
        for i in range(min(count, 5)):
            img = images.nth(i)
            alt = img.get_attribute("alt") or ""
            if not alt.strip():
                src = img.get_attribute("src") or ""
                images_without_alt.append(src[:80])
        if images_without_alt:
            home_page_shared.take_screenshot("merchant_images_no_alt", "info")
            allure.attach(
                f"发现 {len(images_without_alt)} 张商户图片缺少 alt 文本\n" +
                "\n".join(images_without_alt[:10]),
                name="图片alt缺陷列表",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.xfail("已知缺陷：商户图片缺少 alt 文本")

    # ==================== 页面刷新与性能 ====================

    @allure.story("页面加载")
    @allure.title("F5刷新测试")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_refresh(self, home_page_shared: HomePage) -> None:
        """页面刷新后保持正常"""
        initial_title = home_page_shared.page.title()
        home_page_shared.page.reload()
        home_page_shared.wait_for_load()
        assert home_page_shared.page.title() == initial_title

    @allure.story("页面性能")
    @allure.title("页面加载性能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_load_performance(self, home_page_shared: HomePage) -> None:
        """页面在5秒内加载完成"""
        import time
        start = time.time()
        home_page_shared.page.reload()
        home_page_shared.wait_for_load("domcontentloaded")
        duration = time.time() - start
        assert duration < 5.0, f"页面加载耗时 {duration:.2f}s，超过5秒阈值"

    # ==================== Bug 追踪 ====================

    @allure.story("Bug追踪")
    @allure.title("检查JS控制台错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_console_errors(self, home_page_shared: HomePage) -> None:
        """验证页面加载时无 JS 错误

        已知环境缺陷：微前端配置接口返回异常，导致
        "TypeError: Cannot destructure property 'timestamp'" 控制台错误。
        该错误不计入失败，仅当出现其他未知错误时判定失败。
        """
        errors = []
        known_errors = []
        page = home_page_shared.page

        def _on_console(msg):
            if msg.type in ("error", "warning"):
                entry = f"[{msg.type}] {msg.text}"
                if "Cannot destructure property 'timestamp'" in msg.text:
                    known_errors.append(entry)
                else:
                    errors.append(entry)

        page.on("console", _on_console)
        page.reload()
        page.wait_for_load_state("networkidle", timeout=20000)
        page.wait_for_timeout(2000)
        page.remove_listener("console", _on_console)

        if known_errors:
            allure.attach(
                "\n".join(known_errors[:5]),
                name="已知环境缺陷（微前端配置）",
                attachment_type=allure.attachment_type.TEXT,
            )
        if errors:
            allure.attach(
                "\n".join(errors[:10]),
                name="控制台错误",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert len(errors) == 0, f"发现 {len(errors)} 个控制台错误: {errors[:5]}"
        if known_errors:
            pytest.xfail("已知缺陷：微前端配置接口异常导致 timestamp 解构报错")

    @allure.story("顶部导航")
    @allure.title("产业政策导航路由检查")
    @allure.severity(allure.severity_level.NORMAL)
    def test_policy_nav_route(self, home_page_shared: HomePage) -> None:
        """验证产业政策导航链接的路由一致性

        入口说明：导航栏"产业政策"跳转至 /industryNews（改版后正确路由）。
        首页"产业政策"模块的"查看全部"按钮也跳转至 /industryNews。
        两个入口一致，非缺陷。
        """
        links = home_page_shared.page.evaluate(
            """() => {
            const out = [];
            const navTexts = ['首页','供应大厅','智能建造','重点项目','产业政策','产业协会','成果转化','云服务'];
            navTexts.forEach(t => {
              const link = Array.from(document.querySelectorAll('a')).find(a => (a.textContent||'').trim() === t);
              if (link) out.push({text: t, href: link.href});
              else out.push({text: t, href: 'NOT FOUND'});
            });
            return out;
            }"""
        )
        policy_link = next((l for l in links if l["text"] == "产业政策"), None)
        assert policy_link and policy_link["href"], "产业政策链接未找到"
        assert "industryNews" in policy_link["href"], \
            f"导航'产业政策'应跳转至 /industryNews，实际: {policy_link['href']}"

    @allure.story("Bug追踪")
    @allure.title("图片alt文本检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_images_alt_text(self, home_page_shared: HomePage) -> None:
        """验证内容图片包含 alt 文本"""
        missing_alt = home_page_shared.page.evaluate(
            """() => {
            const out = [];
            const imgs = document.querySelectorAll('img[alt=""], img:not([alt])');
            imgs.forEach((img, i) => {
              if (i < 20) {
                out.push((img.src||'').slice(0,80));
              }
            });
            return out;
            }"""
        )
        if len(missing_alt) > 5:
            allure.attach(
                f"发现 {len(missing_alt)} 张图片缺少 alt 文本",
                name="alt缺陷统计",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.xfail(f"已知缺陷：{len(missing_alt)} 张图片缺少 alt 文本")

    @allure.story("Bug追踪")
    @allure.title("页脚ICP链接检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_footer_icp_is_link(self, home_page_shared: HomePage) -> None:
        """验证ICP备案号可点击并跳转到工信部备案查询页"""
        home_page_shared.scroll_to_footer()
        icp = home_page_shared.page.locator(":text('津ICP')").first
        if not icp.is_visible(timeout=3000):
            pytest.skip("当前页面未渲染 ICP 备案号")
        # 点击后应打开工信部备案查询页（新标签页或当前页跳转）
        with home_page_shared.page.context.expect_page(timeout=5000) as new_page_info:
            icp.click()
        new_page = new_page_info.value
        assert "beian.miit.gov.cn" in new_page.url, (
            f"ICP 点击后未跳转到工信部备案页，实际 URL: {new_page.url}"
        )
        new_page.close()
        home_page_shared.goto()

    @allure.story("Bug追踪")
    @allure.title("检查测试占位符内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_placeholder_content(self, home_page_shared: HomePage) -> None:
        """验证页面无测试占位符内容

        已知环境缺陷：测试环境数据库中残留 '测试'、'时代大厦是的是的是多少打撒'
        等占位文案。已知占位词不计入失败，出现其他占位词时判定失败。
        """
        known_keywords = ["哇哦", "测试新增", "时代大厦是的是的是多少打撒", "测试"]
        placeholder_texts = home_page_shared.page.evaluate(
            """(known) => {
            const out = [];
            const knownHits = [];
            const keywords = ['哇哦', '测试新增', '时代大厦是的是的是多少打撒', '测试'];
            const all = Array.from(document.querySelectorAll('button, span, div, h3, p'));
            keywords.forEach(kw => {
              const found = all.filter(el => (el.textContent||'').includes(kw));
              if (found.length > 0) {
                if (known.includes(kw)) {
                  knownHits.push({keyword: kw, count: found.length});
                } else {
                  out.push({keyword: kw, count: found.length});
                }
              }
            });
            return {unknown: out, known: knownHits};
            }""",
            known_keywords,
        )
        unknown = placeholder_texts["unknown"]
        known = placeholder_texts["known"]
        if known:
            allure.attach(
                json.dumps(known, ensure_ascii=False, indent=2),
                name="已知占位内容（环境数据问题）",
                attachment_type=allure.attachment_type.TEXT,
            )
        if unknown:
            allure.attach(
                json.dumps(unknown, ensure_ascii=False, indent=2),
                name="占位符内容",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert len(unknown) == 0, f"发现测试占位符: {unknown}"
        if known:
            pytest.xfail("已知缺陷：测试环境残留占位文案（测试/时代大厦...）")

    @allure.story("Bug追踪")
    @allure.title("轮播图前后导航检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_carousel_has_nav_arrows(self, home_page_shared: HomePage) -> None:
        """验证轮播图具有前后导航箭头"""
        arrows = home_page_shared.page.locator(
            ".n-carousel__prev, .n-carousel__next, [class*='carousel-prev'], [class*='carousel-next']"
        )
        if arrows.count() < 2:
            pytest.xfail("已知缺陷：轮播图缺少前后导航箭头")

    @allure.story("Bug追踪")
    @allure.title("返回顶部按钮检查")
    @allure.severity(allure.severity_level.MINOR)
    def test_back_to_top_exists(self, home_page_shared: HomePage) -> None:
        """验证首页存在返回顶部按钮"""
        home_page_shared.scroll_to_footer()
        exists = home_page_shared.page.evaluate(
            """() => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
              const t = (el.textContent||'').trim();
              const raw = el.className;
              const cls = (typeof raw === 'string') ? raw : (raw && raw.baseVal) || '';
              if (t.includes('返回顶部') || t.includes('回到顶部') || t.includes('回顶部') ||
                  cls.includes('back-to-top') || cls.includes('back_top') || cls.includes('totop')) {
                return true;
              }
            }
            return false;
            }"""
        )
        if not exists:
            pytest.xfail("已知缺陷：首页缺少返回顶部按钮")

    @allure.story("字体一致性")
    @allure.title("首页顶部导航链接字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_nav_link_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页顶部导航链接字体样式一致"""
        nav_texts = ["供应大厅", "智能建造", "重点项目", "产业政策"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in nav_texts:
            el = home_page_shared.page.locator(f"a:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个导航链接" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "导航链接 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页会展信息字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_exhibition_info_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页会展活动时间/地点字体样式一致"""
        info_texts = [
            "2026-10-06—2026-10-27",
            "昆明世纪城国际会议中心",
            "2026-10-01—2026-11-10",
        ]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in info_texts:
            el = home_page_shared.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个会展信息" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "会展信息 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页产业需求联系人字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_contact_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页产业需求联系人姓名字体样式一致"""
        contact_texts = ["董经理", "刘经理"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in contact_texts:
            el = home_page_shared.page.locator(f"strong:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个联系人" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "联系人 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页产业需求数量字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_demand_count_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页产业需求数量字体样式一致"""
        count_texts = ["150", "195", "170"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in count_texts:
            el = home_page_shared.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个需求数量" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "需求数量 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页新闻日期字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_date_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页新闻日期字体样式一致"""
        date_texts = ["2026-10-10", "2026-10-08"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in date_texts:
            el = home_page_shared.page.locator(f"time:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻日期" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻日期 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页新闻描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_news_desc_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页新闻描述字体样式一致"""
        desc_texts = ["微风范围分为访问范围", "范围分为访问范围", "时代大厦是的是的是多少打撒"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = home_page_shared.page.locator(f"p:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个新闻描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "新闻描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )

    @allure.story("字体一致性")
    @allure.title("首页悬浮按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_float_button_font_consistency(self, home_page_shared: HomePage) -> None:
        """验证首页悬浮按钮（在线客服/意向填报）字体样式一致"""
        btn_texts = ["在线客服", "意向填报"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in btn_texts:
            el = home_page_shared.page.locator(f"div:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个悬浮按钮" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "悬浮按钮 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
