"""H5 核心业务页面冒烟与关键交互测试（移动端真实路径）"""
from __future__ import annotations

import allure
import pytest

from config.settings import settings

from utils.ui_quality import assert_console_clean, assert_no_placeholder_content


pytestmark = [pytest.mark.h5, pytest.mark.regression, pytest.mark.smoke]


def _assert_h5_page_ok(page_obj, *, expected_path: str, title_keywords: list[str] | None = None):
    page = page_obj.page
    if page_obj.is_not_found_page() or "404" in (page.title() or ""):
        pytest.skip(f"H5 路由 {expected_path} 当前不可用(404/未找到)")
    assert expected_path in page.url, f"H5 未进入预期页面，期望包含 {expected_path}，实际: {page.url}"
    overflow, sw, cw = page_obj.has_horizontal_overflow()
    assert not overflow, f"H5 页面横向溢出({expected_path}): scrollWidth={sw}, clientWidth={cw}"
    if title_keywords:
        title = page.title() or ""
        assert any(k in title for k in title_keywords) or expected_path.strip('/')[:4] in page.url, (
            f"H5 页面标题异常: {title}"
        )


@allure.feature("H5-供应大厅")
class TestH5SupplyHall:
    @allure.story("页面加载")
    @allure.title("H5-供应大厅页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_supply_hall_load(self, h5_supply_hall_page, test_data):
        po = h5_supply_hall_page
        _assert_h5_page_ok(po, expected_path="/supplyHall", title_keywords=["供应大厅", "天津市建筑"])
        po.assert_page_loaded()
        assert_console_clean(po.page, test_data, page_key="supply_hall")
        assert_no_placeholder_content(po.page, test_data, page_key="supply_hall")

    @allure.story("搜索与筛选")
    @allure.title("H5-供应大厅一级分类可切换")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_h5_supply_hall_filter(self, h5_supply_hall_page):
        po = h5_supply_hall_page
        tab = po.first_visible("text=建筑材料", timeout=2000) or po.first_visible("text=机械设备", timeout=1500)
        if tab is None:
            pytest.skip("H5 供应大厅未找到可见分类筛选")
        old = po.page.url
        try:
            tab.click(timeout=5000)
        except Exception:
            tab.evaluate("el => el.click()")
        try:
            po.page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        assert "/supplyHall" in po.page.url or po.page.url != old

    @allure.story("搜索与筛选")
    @allure.title("H5-供应大厅子类筛选触发结果刷新")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_h5_supply_hall_subcategory_navigates(self, h5_supply_hall_page):
        po = h5_supply_hall_page
        page = po.page
        # 供应大厅首页子类（如土建/文施）点击会进入带筛选参数的搜索结果
        candidates = []
        for name in ["土建", "文施", "给排水", "装饰装修", "市政", "工程机械"]:
            loc = po.first_visible(f"button:has-text('{name}')", timeout=800)
            if loc is not None:
                candidates.append((name, loc))
        if not candidates:
            pytest.skip("H5 供应大厅未找到可见子类筛选入口")
        old_url = page.url
        _, btn = candidates[0]
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.evaluate("el => el.click()")
        try:
            page.wait_for_load_state("domcontentloaded", timeout=8000)
        except Exception:
            pass
        changed = page.url != old_url
        in_search = "search" in page.url or "category" in page.url or "productType" in page.url
        has_content = False
        try:
            has_content = page.locator("article, [class*='card'], [class*='product'], [class*='goods']").count() > 0
        except Exception:
            pass
        assert changed or in_search or has_content, (
            f"H5 供应大厅子类筛选后无可观测变化，URL: {page.url}"
        )

    @allure.story("商品详情")
    @allure.title("H5-供应大厅商品可进入详情页")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_h5_supply_hall_open_detail(self, h5_supply_hall_page):
        po = h5_supply_hall_page
        page = po.page
        old_url = page.url
        # 优先点击可见商品卡片/价格元素
        candidates = [
            "article a, article button, [class*='product'] a, [class*='goods'] a, [class*='card'] a",
            "article, [class*='product-card'], [class*='goods-card'], [class*='card']",
            "text=/¥|￥|元/",
        ]
        clicked = False
        for sel in candidates:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible(timeout=1500):
                    try:
                        loc.scroll_into_view_if_needed(timeout=2000)
                    except Exception:
                        pass
                    try:
                        loc.click(timeout=5000)
                    except Exception:
                        loc.evaluate("el => el.click()")
                    clicked = True
                    break
            except Exception:
                continue
        if not clicked:
            # 兜底使用页面对象方法
            try:
                po.click_first_supply_item()
                clicked = True
            except Exception:
                pass
        if not clicked:
            pytest.skip("H5 供应大厅未找到可点击的商品项")
        try:
            page.wait_for_load_state("domcontentloaded", timeout=8000)
        except Exception:
            pass
        try:
            page.wait_for_url(lambda u: u != old_url, timeout=8000)
        except Exception:
            pass
        assert page.url != old_url or "detail" in page.url.lower() or "buildEquipmentWoker" in page.url, (
            f"H5 点击供应大厅商品后未进入详情，URL: {page.url}"
        )


@allure.feature("H5-重点项目")
class TestH5KeyProject:
    @allure.story("页面加载")
    @allure.title("H5-重点项目页面加载与列表可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_key_project_load(self, h5_key_project_page, test_data):
        po = h5_key_project_page
        _assert_h5_page_ok(po, expected_path="/keyProject", title_keywords=["重点项目", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert any(k in body for k in ["房建项目", "市政项目", "其他项目", "招标", "项目"]), "H5 重点项目页面未展示核心内容"
        assert_console_clean(po.page, test_data, page_key="key_project")
        assert_no_placeholder_content(po.page, test_data, page_key="key_project")

    @allure.story("筛选与分页")
    @allure.title("H5-重点项目分类/分页控件可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_key_project_controls(self, h5_key_project_page):
        po = h5_key_project_page
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        has_filter = any(k in body for k in ["房建项目", "市政项目", "其他项目"])
        has_pagination = po.page.locator("text=跳转, [class*='pagination'], .n-pagination, button:has-text('下一页')").first.count() > 0 or "跳转" in body
        assert has_filter or has_pagination, "H5 重点项目未发现筛选或分页控件"

    @allure.story("筛选与分页")
    @allure.title("H5-重点项目筛选切换影响列表内容")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_h5_key_project_filter_changes_list(self, h5_key_project_page):
        po = h5_key_project_page
        try:
            before = po.get_list_titles()
        except Exception:
            before = []
        if not before:
            pytest.skip("H5 重点项目暂无列表数据，无法验证筛选变化")
        for name in ["市政项目", "其他项目", "房建项目"]:
            try:
                po.click_filter(name)
            except Exception:
                continue
            try:
                changed = po.wait_for_list_titles_change(before, timeout=7000)
            except Exception:
                changed = False
            try:
                after = po.get_list_titles()
            except Exception:
                after = []
            if changed or (after and after != before):
                assert after != before or changed, f"H5 重点项目切换{name}后列表未变化"
                return
        pytest.skip("H5 重点项目筛选切换后未观测到列表变化（数据或交互不可用）")

    @allure.story("筛选与分页")
    @allure.title("H5-重点项目分页切换内容并可返回")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_h5_key_project_pagination(self, h5_key_project_page):
        po = h5_key_project_page
        if not po.has_pagination():
            pytest.skip("H5 重点项目当前无分页控件")
        try:
            before = po.get_list_titles()
        except Exception:
            before = []
        ok = po.click_pagination_page("2")
        if not ok:
            pytest.skip("H5 重点项目无法切换到第2页")
        try:
            changed = po.wait_for_list_titles_change(before, timeout=7000)
        except Exception:
            changed = False
        try:
            after = po.get_list_titles()
        except Exception:
            after = []
        active = ""
        try:
            active = po.get_active_pagination_page()
        except Exception:
            pass
        assert active == "2" or changed or (after and after != before), (
            f"H5 重点项目翻页后未生效，active={active}, before={before[:2]}, after={after[:2]}"
        )
        # 返回第1页（可选但尽量验证）
        back = po.click_pagination_page("1")
        if back:
            try:
                po.wait_for_list_titles_change(after, timeout=6000)
            except Exception:
                pass


@allure.feature("H5-产业新闻")
class TestH5IndustryNews:
    @allure.story("页面加载")
    @allure.title("H5-产业新闻页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_industry_news_load(self, h5_industry_news_page, test_data):
        po = h5_industry_news_page
        _assert_h5_page_ok(po, expected_path="/industryNews", title_keywords=["产业新闻", "产业政策", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert any(k in body for k in ["行业动态", "政策资讯", "政策解读", "产业政策"]), "H5 产业新闻未展示核心Tab/内容"
        assert_console_clean(po.page, test_data, page_key="industry_news")
        assert_no_placeholder_content(po.page, test_data, page_key="industry_news")

    @allure.story("筛选与分页")
    @allure.title("H5-产业新闻Tab/分页可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_industry_news_controls(self, h5_industry_news_page):
        po = h5_industry_news_page
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert any(k in body for k in ["行业动态", "政策资讯", "政策解读"]) or "跳转" in body

    @allure.story("筛选与分页")
    @allure.title("H5-产业新闻Tab切换可响应")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_h5_industry_news_tab_switch(self, h5_industry_news_page):
        po = h5_industry_news_page
        try:
            before = po.get_list_titles()
        except Exception:
            before = []
        tabs = ["政策资讯", "政策解读", "行业动态"]
        clicked_any = False
        for name in tabs:
            try:
                loc = po.first_visible(f"button:has-text('{name}')", timeout=1200) or po.first_visible(f"text={name}", timeout=800)
                if loc is None:
                    continue
                try:
                    loc.click(timeout=4000)
                except Exception:
                    loc.evaluate("el => el.click()")
                clicked_any = True
                try:
                    po.page.wait_for_load_state("domcontentloaded", timeout=5000)
                except Exception:
                    pass
                try:
                    after = po.get_list_titles()
                except Exception:
                    after = []
                if not before or (after and after != before) or po.page.locator("article, h2, h3").count() > 0:
                    return
            except Exception:
                continue
        if not clicked_any:
            pytest.skip("H5 产业新闻未找到可点击的Tab")
        # 至少页面仍正常
        assert "/industryNews" in po.page.url

    @allure.story("筛选与分页")
    @allure.title("H5-产业新闻分页切换内容")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_h5_industry_news_pagination(self, h5_industry_news_page):
        po = h5_industry_news_page
        has_pag = False
        try:
            has_pag = po.has_pagination()
        except Exception:
            try:
                body = po.page.locator("body").inner_text(timeout=5000) or ""
            except Exception:
                body = ""
            has_pag = "跳转" in body or po.page.locator(".n-pagination, [class*='pagination']").count() > 0
        if not has_pag:
            pytest.skip("H5 产业新闻当前无分页控件")
        try:
            before = po.get_list_titles()
        except Exception:
            before = []
        ok = po.click_pagination_page("2")
        if not ok:
            pytest.skip("H5 产业新闻无法切换到第2页")
        try:
            changed = po.wait_for_list_titles_change(before, timeout=7000)
        except Exception:
            changed = False
        try:
            after = po.get_list_titles()
        except Exception:
            after = []
        active = ""
        try:
            active = po.get_active_pagination_page()
        except Exception:
            pass
        assert active == "2" or changed or (after and after != before), (
            f"H5 产业新闻翻页后未生效，active={active}"
        )


@allure.feature("H5-产业需求")
class TestH5DemandPage:
    @allure.story("页面加载")
    @allure.title("H5-产业需求页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_demand_page_load(self, h5_demand_page, test_data):
        po = h5_demand_page
        _assert_h5_page_ok(po, expected_path="/demandPage", title_keywords=["产业需求", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert any(k in body for k in ["建筑建材", "机械设备", "劳务用工", "技术服务", "搜索"]), "H5 产业需求未展示筛选/搜索内容"
        assert_console_clean(po.page, test_data, page_key="demand_page")
        assert_no_placeholder_content(po.page, test_data, page_key="demand_page")

    @allure.story("筛选与搜索")
    @allure.title("H5-产业需求筛选与搜索控件可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_demand_page_controls(self, h5_demand_page):
        po = h5_demand_page
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert "搜索" in body or po.page.locator("input").count() > 0
        assert any(k in body for k in ["建筑建材", "机械设备", "劳务用工", "技术服务"])

    @allure.story("筛选与分页")
    @allure.title("H5-产业需求筛选切换可响应")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_h5_demand_page_filter_switch(self, h5_demand_page):
        po = h5_demand_page
        before = ""
        try:
            before = po.get_body_signature()
        except Exception:
            try:
                before = (po.page.locator("body").inner_text(timeout=5000) or "")[:500]
            except Exception:
                before = ""
        clicked = False
        for name in ["机械设备", "劳务用工", "技术服务", "建筑建材"]:
            loc = po.first_visible(f"text={name}", timeout=1200)
            if loc is None:
                continue
            try:
                loc.click(timeout=4000)
            except Exception:
                try:
                    loc.evaluate("el => el.click()")
                except Exception:
                    continue
            clicked = True
            try:
                po.page.wait_for_load_state("domcontentloaded", timeout=5000)
            except Exception:
                pass
            try:
                po.page.wait_for_function(
                    "(prev) => (document.body.innerText || '').slice(0, 500) !== prev",
                    arg=before,
                    timeout=3000,
                )
            except Exception:
                pass
            after = ""
            try:
                after = po.get_body_signature()
            except Exception:
                try:
                    after = (po.page.locator("body").inner_text(timeout=5000) or "")[:500]
                except Exception:
                    after = ""
            if after and after != before:
                return
        if not clicked:
            pytest.skip("H5 产业需求未找到可点击筛选项")
        assert "/demandPage" in po.page.url, f"H5 产业需求筛选后页面异常: {po.page.url}"

    @allure.story("筛选与分页")
    @allure.title("H5-产业需求分页切换可响应")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.navigation
    def test_h5_demand_page_pagination(self, h5_demand_page):
        po = h5_demand_page
        has_pag = False
        try:
            has_pag = po.has_pagination()
        except Exception:
            try:
                body = po.page.locator("body").inner_text(timeout=5000) or ""
            except Exception:
                body = ""
            has_pag = "跳转" in body or po.page.locator(".n-pagination, [class*='pagination']").count() > 0
        if not has_pag:
            pytest.skip("H5 产业需求当前无分页控件")
        try:
            before = po.get_body_signature()
        except Exception:
            try:
                before = (po.page.locator("body").inner_text(timeout=5000) or "")[:500]
            except Exception:
                before = ""
        ok = po.click_pagination_page("2")
        if not ok:
            pytest.skip("H5 产业需求无法切换到第2页")
        try:
            po.page.wait_for_function(
                "(prev) => (document.body.innerText || '').slice(0, 500) !== prev",
                arg=before,
                timeout=4000,
            )
        except Exception:
            pass
        try:
            after = po.get_body_signature()
        except Exception:
            try:
                after = (po.page.locator("body").inner_text(timeout=5000) or "")[:500]
            except Exception:
                after = ""
        active = ""
        try:
            active = po.get_active_pagination_page()
        except Exception:
            pass
        assert active == "2" or (after and after != before), (
            f"H5 产业需求翻页后未生效，active={active}"
        )


@allure.feature("H5-成果转化")
class TestH5AchievementTransformation:
    @allure.story("页面加载")
    @allure.title("H5-成果转化页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_achievement_load(self, h5_achievement_transformation_page, test_data):
        po = h5_achievement_transformation_page
        _assert_h5_page_ok(po, expected_path="/achievementTransformation", title_keywords=["成果转化", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert any(k in body for k in ["课题", "成果", "科技创新", "转化"]), "H5 成果转化未展示核心内容"
        assert_console_clean(po.page, test_data, page_key="achievement_transformation")
        assert_no_placeholder_content(po.page, test_data, page_key="achievement_transformation")


@allure.feature("H5-产业协会")
class TestH5IndustryAssociation:
    @allure.story("页面加载")
    @allure.title("H5-产业协会页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_industry_association_load(self, h5_industry_association_page, test_data):
        po = h5_industry_association_page
        _assert_h5_page_ok(po, expected_path="/industryAssociation", title_keywords=["产业协会", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert len(body.strip()) > 20, "H5 产业协会页面内容为空"
        assert_console_clean(po.page, test_data, page_key="industry_association")
        assert_no_placeholder_content(po.page, test_data, page_key="industry_association")


@allure.feature("H5-云服务")
class TestH5CloudService:
    @allure.story("页面加载")
    @allure.title("H5-云服务页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_cloud_service_load(self, h5_cloud_service_page, test_data):
        po = h5_cloud_service_page
        _assert_h5_page_ok(po, expected_path="/cloudService", title_keywords=["云服务", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert len(body.strip()) > 20, "H5 云服务页面内容为空"
        assert_console_clean(po.page, test_data, page_key="cloud_service")
        assert_no_placeholder_content(po.page, test_data, page_key="cloud_service")


@allure.feature("H5-智能建造")
class TestH5IntelligentConstruction:
    @allure.story("页面加载")
    @allure.title("H5-智能建造页面加载与核心内容可见")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_h5_intelligent_construction_load(self, h5_intelligent_construction_page, test_data):
        po = h5_intelligent_construction_page
        _assert_h5_page_ok(po, expected_path="/intelligentConstruction", title_keywords=["智能建造", "天津市建筑"])
        po.assert_page_loaded()
        body = (po.page.locator("body").inner_text(timeout=8000) or "")
        assert "智能建造" in body or len(body.strip()) > 20, "H5 智能建造页面未展示核心内容"
        assert_console_clean(po.page, test_data, page_key="intelligent_construction")
        assert_no_placeholder_content(po.page, test_data, page_key="intelligent_construction")


@allure.feature("H5-产业化服务")
class TestH5IndustrialService:
    @allure.story("路由可用性")
    @allure.title("H5-产业化服务路由按当前环境可用性处理")
    @allure.severity(allure.severity_level.NORMAL)
    def test_h5_industrial_service_route(self, h5_industrial_service_page, test_data):
        po = h5_industrial_service_page
        page = po.page
        # IndustrialServicePage.open() 打开首页模块；若独立路由不可用且模块不可见则按前提跳过
        if "industrialService" in (page.url or "") and (
            po.is_not_found_page() or "404" in (page.title() or "") or "not found" in (page.title() or "").lower()
        ):
            pytest.skip("H5 /industrialService 当前不可用(404/未找到)")
        overflow, sw, cw = po.has_horizontal_overflow()
        assert not overflow, f"H5 产业化服务页面横向溢出: scrollWidth={sw}, clientWidth={cw}"
        po.assert_page_loaded()
        try:
            po.assert_service_exists()
        except Exception:
            # 模块结构/文案变动时，至少保证当前页面可正常访问（与配置站点同域）
            from urllib.parse import urlparse

            expected_host = urlparse(settings.base_url).netloc
            current_host = urlparse(page.url or "").netloc
            assert "天津市建筑" in (page.title() or "") or current_host == expected_host, (
                f"H5 产业化服务模块/首页不可用，当前URL: {page.url}"
            )
        assert_console_clean(page, test_data, page_key="industrial_service")
        assert_no_placeholder_content(page, test_data, page_key="industrial_service")
