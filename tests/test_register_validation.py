"""注册页表单校验矩阵（Web）

站点注册表单为受控组件：必填项/协议未满足时“提交注册”按钮保持禁用；
填写非法手机号后失焦应给出字段级错误提示。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings

pytestmark = [pytest.mark.regression]


def _open_register(page: Page) -> None:
    page.goto(settings.base_url.rstrip("/") + "/register", wait_until="domcontentloaded", timeout=25000)
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass


def _submit_button(page: Page):
    return page.locator("button:has-text('提交注册'), button:has-text('提交')").first


@allure.feature("注册校验")
class TestRegisterValidation:

    @allure.story("页面加载")
    @allure.title("注册页加载且提交按钮默认禁用")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_page_load_and_submit_disabled(self, page: Page) -> None:
        _open_register(page)
        assert "register" in page.url.lower(), f"未进入注册页: {page.url}"
        submit = _submit_button(page)
        assert submit.count() > 0, "未找到提交注册按钮"
        assert submit.is_disabled(), "空表单时提交注册按钮应禁用"

    @allure.story("表单校验")
    @allure.title("必填项标记完整")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_required_markers(self, page: Page) -> None:
        """注册表单应包含多项必填标记（*），避免必填校验缺失"""
        _open_register(page)
        body = (page.locator("body").inner_text(timeout=8000) or "")
        required = body.count("*")
        assert required >= 5, f"必填标记过少: {required}"

    @allure.story("表单校验")
    @allure.title("非法手机号给出字段级错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_invalid_phone_error(self, page: Page) -> None:
        _open_register(page)
        phone = page.locator("input[placeholder='请输入联系电话']").first
        if phone.count() == 0:
            pytest.skip("注册页未找到联系电话输入框")
        phone.fill("abc123")
        phone.blur()
        try:
            page.wait_for_function(
                """() => Array.from(document.querySelectorAll('[class*="feedback"], [class*="error"]'))
                        .some(e => (e.innerText || '').includes('正确的联系电话'))""",
                timeout=4000,
            )
        except Exception:
            pass
        feedback = page.evaluate(
            """() => Array.from(document.querySelectorAll('[class*="feedback"], [class*="error"]'))
                    .map(e => (e.innerText || '').trim()).filter(Boolean)"""
        )
        assert any("正确的联系电话" in t for t in feedback), f"未提示手机号格式错误: {feedback[:5]}"

    @allure.story("表单校验")
    @allure.title("空表单提交被拦截")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_empty_submit_blocked(self, page: Page) -> None:
        _open_register(page)
        submit = _submit_button(page)
        if submit.is_disabled():
            return
        old = page.url
        try:
            submit.click(timeout=3000)
        except Exception:
            pass
        try:
            page.wait_for_url(lambda u: "register" not in u.lower(), timeout=3000)
        except Exception:
            pass
        assert "register" in page.url.lower(), f"空表单提交后离开注册页: {old} -> {page.url}"

    @allure.story("表单校验")
    @allure.title("协议勾选校验")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_agreement_required(self, page: Page) -> None:
        """未勾选协议时不应完成注册（按钮禁用或点击后停留注册页）"""
        _open_register(page)
        checkbox = page.locator(".n-checkbox").first
        if checkbox.count() == 0:
            pytest.skip("注册页未找到协议勾选框")
        checked = checkbox.get_attribute("aria-checked")
        submit = _submit_button(page)
        if checked == "true":
            pytest.skip("协议默认已勾选，无法验证未勾选拦截")
        if submit.is_disabled():
            return
        old = page.url
        try:
            submit.click(timeout=3000)
        except Exception:
            pass
        try:
            page.wait_for_url(lambda u: "register" not in u.lower(), timeout=3000)
        except Exception:
            pass
        assert "register" in page.url.lower(), "未勾选协议仍可提交注册"

    @allure.story("表单校验")
    @allure.title("注册字段完整性")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_field_coverage(self, page: Page) -> None:
        """注册表单应覆盖企业/联系人/验证码等关键信息字段"""
        _open_register(page)
        body = (page.locator("body").inner_text(timeout=8000) or "")
        placeholders = page.eval_on_selector_all(
            "input, textarea", "els => els.map(e => e.placeholder || '')"
        )
        joined = " ".join(placeholders)
        for key in ("企业名称", "统一社会信用代码", "通讯地址"):
            assert key in body, f"注册页缺少字段标签: {key}"
        for key in ("详细地址", "联系人", "联系电话", "验证码"):
            assert key in joined, f"注册页缺少字段输入: {key}（placeholders={placeholders[:8]}）"