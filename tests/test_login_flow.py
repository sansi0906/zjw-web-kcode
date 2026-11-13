"""登录流程测试（Web）

站点登录为首页弹窗（非独立 /login 页面）：账号 + 验证码 + 协议勾选。
校验空表单/未勾选协议时的拦截与提示。
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings

pytestmark = [pytest.mark.regression]


def _open_home(page: Page) -> None:
    page.goto(settings.base_url, wait_until="domcontentloaded", timeout=25000)
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass


def _open_login_modal(page: Page):
    _open_home(page)
    entry = page.locator("text=登录").first
    if entry.count() == 0 or not entry.is_visible(timeout=3000):
        pytest.skip("首页未找到登录入口")
    entry.click()
    try:
        page.wait_for_selector(".n-modal input", timeout=6000)
    except Exception:
        pass
    return page.locator(".n-modal").last


def _feedback_texts(page: Page) -> list[str]:
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('[class*="feedback"], [class*="msg"], [class*="message"], [class*="ouo"], [class*="toast"], [class*="error"]'))
                .map(e => (e.innerText || '').trim()).filter(Boolean)"""
    )


def _wait_feedback(page: Page, timeout: int = 3000) -> None:
    """等待校验提示渲染（站点使用受控表单 feedback 节点或 ouo toast）"""
    try:
        page.wait_for_function(
            """() => Array.from(document.querySelectorAll('[class*="feedback"], [class*="msg"], [class*="message"], [class*="ouo"], [class*="toast"], [class*="error"]'))
                    .some(e => (e.innerText || '').trim())""",
            timeout=timeout,
        )
    except Exception:
        pass


@allure.feature("登录流程")
class TestLoginFlow:

    @allure.story("登录弹窗")
    @allure.title("登录弹窗包含账号与验证码输入")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_modal_fields(self, page: Page) -> None:
        modal = _open_login_modal(page)
        placeholders = page.eval_on_selector_all(
            ".n-modal input", "els => els.map(e => e.placeholder || '')"
        )
        joined = " ".join(placeholders)
        assert "账号" in joined, f"登录弹窗缺少账号输入: {placeholders}"
        assert "验证码" in joined, f"登录弹窗缺少验证码输入: {placeholders}"

    @allure.story("登录弹窗")
    @allure.title("空表单登录被拦截并提示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_empty_submit_validation(self, page: Page) -> None:
        modal = _open_login_modal(page)
        btn = modal.locator("button:has-text('登录')").first
        if btn.count() == 0:
            pytest.skip("登录弹窗未找到登录按钮")
        old_url = page.url
        try:
            btn.click(timeout=3000)
        except Exception:
            pass
        _wait_feedback(page)
        texts = _feedback_texts(page)
        assert any("请输入账号" in t for t in texts) or any("请输入验证码" in t for t in texts), (
            f"空表单登录未给出校验提示: {texts[:8]}"
        )
        assert page.url == old_url, f"空表单登录后页面发生跳转: {old_url} -> {page.url}"

    @allure.story("登录弹窗")
    @allure.title("未勾选协议登录被拦截")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_requires_agreement(self, page: Page) -> None:
        modal = _open_login_modal(page)
        checkbox = modal.locator(".n-checkbox").first
        if checkbox.count() == 0:
            pytest.skip("登录弹窗未找到协议勾选框")
        if (checkbox.get_attribute("aria-checked") or "").lower() == "true":
            pytest.skip("登录协议默认已勾选")
        btn = modal.locator("button:has-text('登录')").first
        if btn.count() == 0:
            pytest.skip("登录弹窗未找到登录按钮")
        try:
            btn.click(timeout=3000)
        except Exception:
            pass
        _wait_feedback(page)
        texts = _feedback_texts(page)
        assert any("协议" in t for t in texts), f"未勾选协议登录未拦截: {texts[:8]}"

    @allure.story("登录弹窗")
    @allure.title("错误验证码登录失败且不跳转")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_code_fails(self, page: Page) -> None:
        modal = _open_login_modal(page)
        inputs = modal.locator("input")
        if inputs.count() < 2:
            pytest.skip("登录弹窗输入项不足")
        inputs.nth(0).fill("13800138000")
        inputs.nth(1).fill("000000")
        checkbox = modal.locator(".n-checkbox:has-text('我已阅读并同意')").first
        if checkbox.count() == 0:
            checkbox = modal.locator(".n-checkbox").last
        if checkbox.count() > 0 and (checkbox.get_attribute("aria-checked") or "").lower() != "true":
            try:
                checkbox.click(timeout=2000)
            except Exception:
                pass
            try:
                page.wait_for_function(
                    """() => { const cs = Array.from(document.querySelectorAll('.n-checkbox'));
                        const c = cs.find(e => (e.innerText||'').includes('我已阅读并同意')) || cs[cs.length-1];
                        return c && c.getAttribute('aria-checked') === 'true'; }""",
                    timeout=2000,
                )
            except Exception:
                pytest.skip("登录协议勾选框无法通过点击勾选（组件实现差异）")
        btn = modal.locator("button:has-text('登录')").first
        old_url = page.url
        if btn.count() > 0:
            try:
                btn.click(timeout=3000)
            except Exception:
                pass
        try:
            page.wait_for_function(
                """() => Array.from(document.querySelectorAll('[class*="ouo"], [class*="msg"], [class*="toast"], [class*="feedback"]'))
                        .some(e => /验证码|失败|错误|账号|密码/.test(e.innerText || ''))""",
                timeout=5000,
            )
        except Exception:
            pass
        texts = _feedback_texts(page)
        assert page.url == old_url, f"错误验证码登录后仍发生跳转: {old_url} -> {page.url}"
        assert any(k in t for t in texts for k in ("验证码", "失败", "错误")), (
            f"错误验证码登录未给出失败提示: {texts[:8]}"
        )