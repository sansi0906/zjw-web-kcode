# -*- coding: utf-8 -*-
"""
跨页面交互测试：筛选切换 + 分页翻页

设计要点：
- 筛选断言采用"切换后列表内容必须不同"的强断言，杜绝 `count >= 0` 永真断言；
- 分页断言校验激活页码切换与列表内容变化，能捕获"分页控件存在但点击无效"；
- 所有用例都基于页面真实存在的筛选项（FILTER_TABS），不存在的一律 skip 而非假装通过。
"""
from __future__ import annotations

import allure
import pytest

from pages.achievement_transformation_page import AchievementTransformationPage
from pages.demand_page import DemandPage
from pages.industry_news_page import IndustryNewsPage
from pages.industry_policy_page import IndustryPolicyPage
from pages.key_project_page import KeyProjectsPage
from pages.supply_hall_page import SupplyHallPage


# ==================== 筛选切换强断言 ====================

# (用例名, 页面类, 筛选项 A, 筛选项 B, 页面中文名)
FILTER_SWITCH_CASES = [
    ("重点项目", KeyProjectsPage, "房建项目", "市政项目"),
    ("产业政策", IndustryPolicyPage, "政策资讯", "政策解读"),
    ("产业新闻", IndustryNewsPage, "行业动态", "政策资讯"),
    ("产业需求", DemandPage, "建筑建材", "机械设备"),
    ("成果转化", AchievementTransformationPage, "课题", "成果"),
    ("供应大厅", SupplyHallPage, "土建", "电气"),
]


@allure.feature("跨页面交互")
class TestFilterSwitch:
    """筛选切换强断言"""

    @pytest.mark.parametrize(
        "page_name,page_cls,label_a,label_b",
        FILTER_SWITCH_CASES,
        ids=[f"{c[0]}-{c[2]}-vs-{c[3]}" for c in FILTER_SWITCH_CASES],
    )
    @allure.story("筛选切换")
    @allure.title("切换筛选项后列表内容必须变化")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filter_switch_changes_list(
        self, page, page_name, page_cls, label_a, label_b
    ) -> None:
        """两个筛选项切换后列表内容必须不同

        若筛选点击无响应、筛选后列表为空、或多个筛选项返回同一份数据，
        本用例都会失败。
        """
        allure.dynamic.title(f"{page_name} - 筛选 {label_a} / {label_b} 列表必须不同")
        page_obj = page_cls(page)
        page_obj.open()
        page.wait_for_timeout(1500)

        titles_a = page_obj.apply_filter(label_a)
        page.wait_for_timeout(800)
        titles_b = page_obj.apply_filter(label_b)
        page.wait_for_timeout(800)

        assert titles_a, f"筛选 '{label_a}' 后列表为空"
        assert titles_b, f"筛选 '{label_b}' 后列表为空"
        assert titles_a != titles_b, (
            f"筛选 '{label_a}' 与 '{label_b}' 的列表内容完全相同，筛选未生效"
        )

    @pytest.mark.parametrize(
        "page_name,page_cls,label_a,label_b",
        FILTER_SWITCH_CASES,
        ids=[f"{c[0]}-active" for c in FILTER_SWITCH_CASES],
    )
    @allure.story("筛选切换")
    @allure.title("选中项高亮状态可识别")
    @allure.severity(allure.severity_level.NORMAL)
    def test_active_filter_is_detectable(
        self, page, page_name, page_cls, label_a, label_b
    ) -> None:
        """点击筛选项后，应能识别出当前选中的项"""
        allure.dynamic.title(f"{page_name} - 选中项高亮可识别")
        page_obj = page_cls(page)
        page_obj.open()
        page.wait_for_timeout(1500)

        page_obj.apply_filter(label_a)
        page.wait_for_timeout(800)
        active = page_obj.get_active_filter_label()
        assert active == label_a, (
            f"点击 '{label_a}' 后识别到的选中项为 {active!r}"
        )

        page_obj.apply_filter(label_b)
        page.wait_for_timeout(800)
        active = page_obj.get_active_filter_label()
        assert active == label_b, (
            f"点击 '{label_b}' 后识别到的选中项为 {active!r}"
        )


# ==================== 分页翻页 ====================

# (用例名, 页面类, 期望最小页数)
PAGINATION_CASES = [
    ("重点项目", KeyProjectsPage, 2),
    ("产业政策", IndustryPolicyPage, 2),
    ("产业新闻", IndustryNewsPage, 2),
]


@allure.feature("跨页面交互")
class TestPagination:
    """分页翻页强断言"""

    @pytest.mark.parametrize(
        "page_name,page_cls,min_pages",
        PAGINATION_CASES,
        ids=[c[0] for c in PAGINATION_CASES],
    )
    @allure.story("分页")
    @allure.title("点击第 2 页后列表内容必须变化")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pagination_switches_content(
        self, page, page_name, page_cls, min_pages
    ) -> None:
        """翻页后激活页码变为 2，且列表内容必须不同"""
        allure.dynamic.title(f"{page_name} - 翻页后列表内容必须变化")
        page_obj = page_cls(page)
        page_obj.open()
        page.wait_for_timeout(2000)

        pages = page_obj.get_pagination_pages()
        if len([p for p in pages if p.isdigit()]) < min_pages:
            pytest.skip(f"当前数据不足以翻页，实际页码: {pages}")

        titles_p1 = page_obj.get_list_titles()
        assert titles_p1, "第 1 页列表为空"

        assert page_obj.click_pagination_page("2"), "点击第 2 页失败"
        page.wait_for_timeout(1500)

        active = page_obj.get_active_pagination_page()
        assert active == "2", f"翻页后激活页应为 2，实际 {active!r}"

        titles_p2 = page_obj.get_list_titles()
        assert titles_p2, "第 2 页列表为空"
        assert titles_p1 != titles_p2, "翻页后列表内容未变化（分页未生效）"

    @pytest.mark.parametrize(
        "page_name,page_cls,min_pages",
        PAGINATION_CASES,
        ids=[c[0] for c in PAGINATION_CASES],
    )
    @allure.story("分页")
    @allure.title("翻到第 2 页后可返回第 1 页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_back_to_first(
        self, page, page_name, page_cls, min_pages
    ) -> None:
        """翻页后应能点击页码回到第 1 页，且列表内容恢复"""
        allure.dynamic.title(f"{page_name} - 返回第 1 页")
        page_obj = page_cls(page)
        page_obj.open()
        page.wait_for_timeout(2000)

        pages = page_obj.get_pagination_pages()
        if len([p for p in pages if p.isdigit()]) < min_pages:
            pytest.skip(f"当前数据不足以翻页，实际页码: {pages}")

        titles_p1 = page_obj.get_list_titles()
        assert page_obj.click_pagination_page("2"), "点击第 2 页失败"
        page.wait_for_timeout(1500)
        titles_p2 = page_obj.get_list_titles()
        assert titles_p1 != titles_p2, "翻页后列表内容未变化（分页未生效）"

        assert page_obj.click_pagination_page("1"), "点击第 1 页失败"
        page.wait_for_timeout(1500)
        active = page_obj.get_active_pagination_page()
        assert active == "1", f"返回后激活页应为 1，实际 {active!r}"
        titles_back = page_obj.get_list_titles()
        assert titles_back == titles_p1, "返回第 1 页后列表内容与初始不一致"

    @pytest.mark.parametrize(
        "page_name,page_cls,min_pages",
        PAGINATION_CASES,
        ids=[c[0] for c in PAGINATION_CASES],
    )
    @allure.story("分页")
    @allure.title("分页页码默认选中第 1 页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination_default_active_page(
        self, page, page_name, page_cls, min_pages
    ) -> None:
        """进入页面时默认激活第 1 页"""
        allure.dynamic.title(f"{page_name} - 分页默认选中第 1 页")
        page_obj = page_cls(page)
        page_obj.open()
        page.wait_for_timeout(2000)

        pages = page_obj.get_pagination_pages()
        assert pages, "未找到分页页码"
        assert "1" in pages, f"分页缺少第 1 页，实际: {pages}"
        active = page_obj.get_active_pagination_page()
        assert active == "1", f"默认激活页应为 1，实际 {active!r}"
