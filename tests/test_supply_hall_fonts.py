# -*- coding: utf-8 -*-
import allure
import pytest
from pages.base_page import BasePage
from pages.supply_hall_page import SupplyHallPage


@allure.feature("字体一致性")
@allure.story("供应大厅页面")
class TestSupplyHallFonts:
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page_obj = SupplyHallPage(page)
        self.page_obj.open()

    @allure.story("字体一致性")
    @allure.title("供应大厅分类标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_category_title_font_consistency(self) -> None:
        """验证供应大厅 H2 分类标题字体样式一致

        建筑材料、水电暖通、机械设备、工程机械、劳务用工
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        title_texts = ["建筑材料", "水电暖通", "机械设备", "工程机械", "劳务用工"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"h2:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个分类标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "分类标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_category_title_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅子分类标题字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_subcategory_title_font_consistency(self) -> None:
        """验证供应大厅 H3 子分类标题字体样式一致

        土建、装饰装修、给排水、电气、智能设备、专业设备、起重机械、混凝土机械
        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        title_texts = ["土建", "装饰装修", "给排水", "电气", "智能设备", "专业设备", "起重机械", "混凝土机械"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in title_texts:
            el = self.page_obj.page.locator(f"h3:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个子分类标题" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "子分类标题 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_subcategory_title_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅查看全部按钮字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_view_all_font_consistency(self) -> None:
        """验证供应大厅页面所有'查看全部'按钮字体样式一致

        应使用相同的 fontFamily、fontSize、fontWeight、color。
        """
        view_all_texts = ["查看全部", "查看全部", "查看全部", "查看全部"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for i, text in enumerate(view_all_texts):
            el = self.page_obj.page.locator(f"button:has-text('{text}')").nth(i)
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[f"{text}_{i}"] = style

        assert len(styles) >= 2, "仅找到 %d 个'查看全部'按钮" % len(styles)

        first_key = list(styles.keys())[0]
        first_style = styles[first_key]
        for key, style in styles.items():
            for sk in style_keys:
                assert style[sk] == first_style[sk], (
                    "'查看全部'按钮 %s 的 %s (%s) 与 %s (%s) 不一致"
                    % (key, sk, style[sk], first_key, first_style[sk])
                )
        self.page_obj.take_screenshot("supply_hall_view_all_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅统计数字字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_stats_number_font_consistency(self) -> None:
        num_texts = ["500+", "10万+", "3分钟", "1万+"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in num_texts:
            el = self.page_obj.page.locator(f"strong:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个统计数字" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "统计数字 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_stats_number_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅统计标签字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_stats_label_font_consistency(self) -> None:
        label_texts = ["商品种类", "在售商品", "求购响应", "供需对接"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in label_texts:
            el = self.page_obj.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个统计标签" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "统计标签 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_stats_label_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅分类描述字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_category_desc_font_consistency(self) -> None:
        desc_texts = ["覆盖项目主体与装饰全流程的各类建材供应", "水、电、暖、消防一站式机电材料采购", "各类大型施工机械设备整机、租赁与维保服务"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in desc_texts:
            el = self.page_obj.page.locator(f"p:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个分类描述" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "分类描述 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_category_desc_font", "info")

    @allure.story("字体一致性")
    @allure.title("供应大厅服务标签字体一致性")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_service_tag_font_consistency(self) -> None:
        tag_texts = ["服务好", "老师傅", "性价比高", "效率高"]
        style_keys = ["fontFamily", "fontSize", "fontWeight", "color"]
        styles = {}
        for text in tag_texts:
            el = self.page_obj.page.locator(f"span:has-text('{text}')").first
            if el.is_visible():
                style = el.evaluate(
                    "(el) => { const s = getComputedStyle(el); return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, color: s.color }; }"
                )
                styles[text] = style

        assert len(styles) >= 2, "仅找到 %d 个服务标签" % len(styles)

        first_text = list(styles.keys())[0]
        first_style = styles[first_text]
        for text, style in styles.items():
            for key in style_keys:
                assert style[key] == first_style[key], (
                    "服务标签 '%s' 的 %s (%s) 与 '%s' (%s) 不一致"
                    % (text, key, style[key], first_text, first_style[key])
                )
        self.page_obj.take_screenshot("supply_hall_service_tag_font", "info")
