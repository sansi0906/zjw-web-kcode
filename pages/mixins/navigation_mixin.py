from typing import Optional
from urllib.parse import urlparse
from playwright.sync_api import Page

class NavigationMixin:
    page: Page

    def get_active_nav_class(self) -> Optional[str]:
        """获取当前路由对应的顶部导航链接的 class

        站点顶部导航容器类名为 .nav-cneter（源码拼写如此），
        导航项与路由通过 href 关联，因此按 href 匹配比按文本匹配更可靠。
        :return: class 字符串；当前路由不在顶部导航中时返回 None
        """




    def _open_mobile_nav_if_needed(self) -> bool:
        """H5：如导航在抽屉中，尝试展开汉堡菜单"""
        if not self.is_mobile():
            return False
        hamburger_selectors = [
            ".hamburger",
            "button[aria-label*='菜单']",
            "button[aria-label*='menu']",
            "[class*='menu-toggle']",
            ".nav-toggle",
            "[class*='hamburger']",
            "button[class*='menu']",
            "[class*='burger']",
            ".menu-btn",
            ".nav-menu-btn",
            ".mobile-menu-toggle",
            "[class*='navbar-toggle']",
            ".header-menu",
            "button:has-text('菜单')",
            "button:has-text('≡')",
            "[class*='mobile-nav-toggle']",
            "[class*='drawer-toggle']",
        ]
        for sel in hamburger_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    self.page.wait_for_timeout(800)
                    return True
            except Exception:
                continue
        return False

    def _close_mobile_nav_if_needed(self) -> bool:
        """H5：尝试关闭抽屉/导航"""
        if not self.is_mobile():
            return False
        close_selectors = [
            ".n-drawer__close",
            ".ant-drawer-close",
            "button[aria-label*='关闭']",
            "[class*='drawer-close']",
            ".drawer-close",
        ]
        for sel in close_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    self.page.wait_for_timeout(300)
                    return True
            except Exception:
                continue
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(300)
            return True
        except Exception:
            return False

    def _nav_link_selectors(self, nav_text: str, prefer_button: bool = False) -> list[str]:
        """生成导航链接候选选择器（按优先级）

        顶部导航区域的选择器优先，避免误点正文中同名的分类按钮/描述文本。
        """
        nav_scoped = [
            f".nav-left a:has-text('{nav_text}')",
            f".header-title a:has-text('{nav_text}')",
            f".nav-cneter a:has-text('{nav_text}')",
            f".nav a:has-text('{nav_text}')",
            f"header a:has-text('{nav_text}')",
            f"nav a:has-text('{nav_text}')",
        ]
        if prefer_button:
            return [f"button:has-text('{nav_text}')"] + nav_scoped + [
                f"a:has-text('{nav_text}')",
                f"text={nav_text}",
            ]
        return nav_scoped + [f"a:has-text('{nav_text}')", f"text={nav_text}"]

    def _click_nav_candidate(self, nav_text: str, prefer_button: bool = False) -> bool:
        """按候选选择器依次尝试点击导航项，返回是否点击成功"""
        for sel in self._nav_link_selectors(nav_text, prefer_button):
            try:
                nav = self.page.locator(sel).first
                if not nav.is_visible(timeout=1500):
                    continue
                old_url = self.page.url
                nav.click()
                self.wait_for_load()
                self.wait_for_url_change(old_url)
                return True
            except Exception:
                continue
        # 抽屉内部兜底（H5 折叠菜单）
        for ds in [".n-drawer", ".ant-drawer", ".drawer", "[class*='drawer']", ".nav-collapse"]:
            try:
                if not self.page.locator(ds).first.is_visible(timeout=800):
                    continue
                link = self.page.locator(f"{ds} a:has-text('{nav_text}')").first
                if not link.is_visible(timeout=1000):
                    continue
                old_url = self.page.url
                link.click()
                self.wait_for_load()
                self.wait_for_url_change(old_url)
                return True
            except Exception:
                continue
        return False

    def click_nav_by_text(self, nav_text: str) -> None:
        """根据文本点击导航链接（支持 H5 抽屉导航）"""
        if self.is_mobile():
            # 先尝试打开抽屉（若导航项在抽屉内）
            self._open_mobile_nav_if_needed()
            if self._click_nav_candidate(nav_text, prefer_button=True):
                return
            self._close_mobile_nav_if_needed()
            return

        if self._click_nav_candidate(nav_text):
            return

        # 兜底：JS 点击文本完全匹配的元素
        try:
            old_url = self.page.url
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
            self.wait_for_url_change(old_url)
        except Exception:
            pass

