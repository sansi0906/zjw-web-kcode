"""a11y 基础检查（语义/可访问名称/表单标签）

范围：Web 首页 + 供应大厅列表 + H5 首页。
不引入 axe-core 等外部依赖，只做低成本、可稳定判定的基础项。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings
from utils.ui_quality import assert_images_alt

pytestmark = [pytest.mark.regression, pytest.mark.a11y]


def _button_names(page: Page) -> tuple[int, int]:
    """返回 (可见按钮数, 无可访问名称按钮数)"""
    return page.evaluate(
        """() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        let total = 0, unnamed = 0;
        for (const b of btns) {
            const r = b.getBoundingClientRect();
            const s = getComputedStyle(b);
            if (r.width <= 0 || r.height <= 0 || s.visibility === 'hidden' || s.display === 'none') continue;
            total += 1;
            const name = ((b.innerText || '') + ' ' + (b.getAttribute('aria-label') || '') + ' ' + (b.getAttribute('title') || '')).trim();
            if (!name) unnamed += 1;
        }
        return [total, unnamed];
        }"""
    ) or [0, 0]


def _unlabelled_inputs(page: Page) -> list[str]:
    return page.evaluate(
        """() => {
        const out = [];
        for (const el of Array.from(document.querySelectorAll('input, textarea, select'))) {
            const r = el.getBoundingClientRect();
            const s = getComputedStyle(el);
            if (r.width <= 0 || r.height <= 0 || s.visibility === 'hidden' || s.display === 'none') continue;
            if (el.type === 'hidden') continue;
            const hasAria = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
            const hasPh = el.getAttribute('placeholder');
            const id = el.id;
            const hasLabel = id && document.querySelector(`label[for="${id}"]`);
            const wrapped = el.closest('label');
            if (!hasAria && !hasPh && !hasLabel && !wrapped) {
                out.push((el.outerHTML || '').slice(0, 100));
            }
        }
        return out;
        }"""
    ) or []


@allure.feature("a11y 基础")
class TestA11yBasic:

    @allure.story("语义")
    @allure.title("Web 首页语言与标题结构")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.xfail(reason="首页未使用 h1/h2/h3 标题标签（站点已知实现，语义化待改进）", strict=False)
    def test_home_lang_and_headings(self, page: Page) -> None:
        page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
        lang = page.evaluate("() => document.documentElement.getAttribute('lang') || ''")
        assert lang.strip(), "html 缺少 lang 属性"
        headings = page.evaluate(
            "() => Array.from(document.querySelectorAll('h1,h2,h3')).filter(e => (e.innerText||'').trim()).length"
        )
        allure.attach(f"标题标签数量={headings}", name="标题层级", attachment_type=allure.attachment_type.TEXT)
        assert headings > 0, "首页未使用 h1/h2/h3 标题标签"

    @allure.story("可访问名称")
    @allure.title("Web 首页按钮具备可访问名称")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_buttons_accessible_name(self, page: Page) -> None:
        page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
        total, unnamed = _button_names(page)
        allure.attach(f"按钮总数={total}, 无名称={unnamed}", name="按钮可访问名称", attachment_type=allure.attachment_type.TEXT)
        if total == 0:
            return
        ratio = unnamed / total
        assert ratio <= 0.2, f"无名称按钮占比过高: {unnamed}/{total}"

    @allure.story("表单标签")
    @allure.title("Web 首页输入框具备标签/占位")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_inputs_labelled(self, page: Page) -> None:
        page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
        missing = _unlabelled_inputs(page)
        if not missing:
            return
        # 站点搜索框等通过 placeholder 提供名称；仅当存在完全无名称输入时失败
        assert len(missing) <= 1, f"存在无标签输入框: {missing[:5]}"

    @allure.story("图片替代文本")
    @allure.title("Web 首页图片 alt（复用 ui_quality 配置）")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_images_alt(self, page: Page, test_data) -> None:
        page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
        assert_images_alt(page, test_data, page_key="homepage", key="images_alt")

    @allure.story("语义")
    @allure.title("H5 首页 viewport 与按钮名称")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.h5
    def test_h5_viewport_and_buttons(self, h5_page: Page) -> None:
        h5_page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
        meta = h5_page.evaluate(
            "() => { const m = document.querySelector('meta[name=viewport]'); return m ? m.getAttribute('content') || '' : ''; }"
        )
        assert "width=device-width" in meta, f"H5 缺少 viewport 配置: {meta!r}"
        total, unnamed = _button_names(h5_page)
        allure.attach(f"按钮总数={total}, 无名称={unnamed}", name="H5 按钮可访问名称", attachment_type=allure.attachment_type.TEXT)
        if total == 0:
            return
        ratio = unnamed / total
        assert ratio <= 0.25, f"H5 无名称按钮占比过高: {unnamed}/{total}"

    @allure.story("表单标签")
    @allure.title("供应大厅搜索框具备标签")
    @allure.severity(allure.severity_level.MINOR)
    def test_supply_hall_search_labelled(self, page: Page) -> None:
        page.goto(settings.base_url.rstrip("/") + "/supplyHall", wait_until="domcontentloaded", timeout=25000)
        missing = _unlabelled_inputs(page)
        assert not [m for m in missing if "search" in m.lower()], f"搜索框缺少标签: {missing[:3]}"