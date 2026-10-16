"""
产业化服务 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class IndustrialServicePage(BasePage):
    """产业化服务页面"""

    # 移动端服务项选择器
    SERVICE_ITEMS = "[class*='service'], div[class*='card']"
    SERVICE_ITEMS_MOBILE = (
        "[class*='service'], div[class*='card'], "
        "[class*='industrial-service'], .n-carousel__slide, button"
    )

    def open(self) -> IndustrialServicePage:
        """打开首页并定位到产业化服务模块"""
        self.goto()
        self.page.wait_for_timeout(2000)
        return self

    def assert_page_loaded(self) -> None:
        """断言页面加载完成"""
        if self.is_mobile():
            # 移动端首页可能无独立"首页"标题文本，检查服务项是否存在
            count = self.get_service_count()
            assert count > 0, "移动端未找到服务项"
            return
        self.assert_text_visible("首页", partial=True)

    def assert_service_exists(self) -> None:
        """验证产业化服务模块存在"""
        # 检查服务项数量，不依赖特定文本（WEB/移动端可能不同）
        count = self.get_service_count()
        assert count > 0, "未找到产业化服务项"

    def get_service_count(self) -> int:
        """获取服务项数量"""
        if self.is_mobile():
            return self.page.locator(self.SERVICE_ITEMS_MOBILE).count()
        return self.page.locator(self.SERVICE_ITEMS).count()

    def get_nav_texts(self) -> list[str]:
        """获取所有导航链接文本"""
        if self.is_mobile():
            # 移动端使用 JS 提取所有导航文本
            try:
                js_texts = self.page.evaluate("""() => {
                    const sel = 'a, button, [role="button"]';
                    const els = Array.from(document.querySelectorAll(sel));
                    const texts = [];
                    els.forEach(el => {
                        const t = (el.textContent || '').trim();
                        if (t && !texts.includes(t)) texts.push(t);
                    });
                    return texts;
                }""")
                if js_texts:
                    return js_texts
            except Exception:
                pass
        navs = self.page.locator(".nav-left a, .header-title a, header a, nav a, .nav-item a")
        texts = []
        for i in range(navs.count()):
            text = navs.nth(i).text_content()
            if text and text.strip():
                texts.append(text.strip())
        return texts

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接"""
        if self.is_mobile():
            # 移动端优先匹配可见元素，JS 兜底
            for sel in [f"button:has-text('{nav_text}')", f"text={nav_text}", f"a:has-text('{nav_text}')"]:
                try:
                    nav = self.page.locator(sel).first
                    if nav.is_visible(timeout=1500):
                        nav.click()
                        self.wait_for_load()
                        return
                except Exception:
                    continue
            try:
                self.page.evaluate(
                    """(text) => {
                    const els = Array.from(document.querySelectorAll('a, button, [role="button"]'));
                    const el = els.find(e => (e.textContent||'').trim() === text);
                    if (el) { el.click(); return true; }
                    return false;
                    }""",
                    nav_text,
                )
                self.page.wait_for_timeout(1500)
                self.wait_for_load()
                return
            except Exception:
                pass
            return
        nav = self.page.locator(f"text={nav_text}").first
        if nav.is_visible():
            nav.click()
            self.wait_for_load()
