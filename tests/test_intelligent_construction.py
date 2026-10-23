"""
智能建造页面测试用例

URL: https://dev.tj.gongrenle.com/intelligentConstruction

"""
from __future__ import annotations

import allure

from tests.base_page_test import BasePageTest
from pages.intelligent_construction_page import IntelligentConstructionPage


@allure.feature("智能建造页面")
class TestIntelligentConstruction(BasePageTest):
    """智能建造页面测试用例"""

    page_name = "智能建造"
    page_fixture_name = "intelligent_construction_page"

    # ==================== 通用测试（BasePageTest 自动继承） ====================

    # ==================== 建造筛选测试 ===================

    @allure.story("建造筛选")
    @allure.title("全部建造筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("建造筛选")
    @allure.title("推荐建造筛选")
    @allure.severity(allure.severity_level.CRITICAL)

    @allure.story("建造列表")
    @allure.title("建造卡片展示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_construction_cards_display(self) -> None:
        """验证建造卡片正常展示"""
        self.page_obj.open()
        self.page_obj.assert_constructions_exist(min_count=1)
        titles = self.page_obj.get_construction_titles()
        assert len(titles) > 0, "未找到建造标题"
        self.page_obj.take_screenshot("construction_cards", "info")

    @allure.story("建造列表")
    @allure.title("建造卡片点击跳转")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_construction_click(self) -> None:
        """点击建造卡片跳转至详情页"""
        self.page_obj.open()
        self.page_obj.click_first_construction()
        self.page_obj.take_screenshot("construction_detail", "info")

    @allure.story("建造详情")
    @allure.title("查看全部建造按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_all_button(self) -> None:
        """点击查看全部建造按钮"""
        self.page_obj.open()
        self.page_obj.click_view_all()
        self.page_obj.take_screenshot("view_all", "info")

    # ==================== 分页测试 ===================

    @allure.story("分页")
    @allure.title("分页跳转")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_jump(self) -> None:
        """测试分页跳转功能"""
        self.page_obj.open()
        self.page_obj.go_to_page(2)
        self.page_obj.take_screenshot("pagination_jump", "info")

    # ==================== 申报入口测试 ===================

    @allure.story("申报入口")
    @allure.title("智能建造新技术新产品申报")
    @allure.severity(allure.severity_level.NORMAL)
    def test_declaration_new_tech(self) -> None:
        """点击智能建造新技术新产品申报"""
        self.page_obj.open()
        self.page_obj.click_new_tech_declaration()
        self.page_obj.take_screenshot("declaration_new_tech", "info")

    @allure.story("申报入口")
    @allure.title("智能建造种子企业申报")
    @allure.severity(allure.severity_level.NORMAL)
    def test_declaration_seed_enterprise(self) -> None:
        """点击智能建造种子企业申报"""
        self.page_obj.open()
        self.page_obj.click_seed_enterprise_declaration()
        self.page_obj.take_screenshot("declaration_seed_enterprise", "info")

    # ==================== 标准规范测试 ===================

    @allure.story("标准规范")
    @allure.title("查看京津冀标准")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_standard_京津冀(self) -> None:
        """查看京津冀智能建造技术规程"""
        self.page_obj.open()
        self.page_obj.view_standard("京津冀")
        self.page_obj.take_screenshot("standard_jjj", "info")

    # ==================== 平台产品测试 ===================

    @allure.story("平台产品")
    @allure.title("查看BIM产品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_view_bim_product(self) -> None:
        """查看基于BIM的挂篮设计软件"""
        self.page_obj.open()
        self.page_obj.view_platform("BIM")
        self.page_obj.take_screenshot("product_bim", "info")