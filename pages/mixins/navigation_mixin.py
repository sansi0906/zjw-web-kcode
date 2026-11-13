from typing import Optional
from urllib.parse import urlparse
from playwright.sync_api import Page

class NavigationMixin:
    page: Page

    def get_active_nav_class(self) -> Optional[str]:
        """获取当前路由对应的顶部导航链接的 class/激活状态

        站点顶部导航可能使用 router-link-active/active 类、aria-current，
        或仅通过高亮样式（如品牌蓝文字）表示选中。
        :return: 表示激活的字符串；当前路由不在顶部导航中时返回 None
        """
        try:
            current = self.page.url or ""
        except Exception:
            current = ""
        path = urlparse(current).path.rstrip("/") or "/"

        selectors = [
            ".nav-left a[href]",
            ".header-title a[href]",
            ".nav-cneter a[href]",
            ".nav a[href]",
            "header nav a[href]",
            "header a[href]",
            "nav a[href]",
            "a[href]",
        ]

        def _norm_href(href: str) -> str:
            href = (href or "").strip()
            try:
                return urlparse(href).path.rstrip("/") or "/"
            except Exception:
                return href.rstrip("/") or "/"

        def _matches_current(hpath: str) -> bool:
            if not hpath:
                return False
            if hpath == "/":
                return path == "/"
            if path == hpath:
                return True
            if path.startswith(hpath + "/"):
                return True
            if path.endswith(hpath):
                return True
            return False

        matched = None
        seen = set()
        for sel in selectors:
            try:
                loc = self.page.locator(sel)
                count = loc.count()
            except Exception:
                continue
            for i in range(min(count, 80)):
                try:
                    el = loc.nth(i)
                    href = el.get_attribute("href") or ""
                    hpath = _norm_href(href)
                    if not _matches_current(hpath):
                        continue
                    key = (hpath, (el.inner_text(timeout=500) or "").strip())
                    if key in seen:
                        continue
                    seen.add(key)
                    matched = el
                    break
                except Exception:
                    continue
            if matched is not None:
                break

        if matched is None:
            return None

        try:
            cls = (matched.get_attribute("class") or "").strip()
            aria = (matched.get_attribute("aria-current") or "").strip().lower()
            if "router-link-active" in cls or "active" in cls.split() or aria == "page":
                return cls or "active"
            # 样式高亮（品牌蓝等）
            is_style_active = bool(
                matched.evaluate(
                    """el => {
                        const cs = getComputedStyle(el);
                        const c = cs.color || '';
                        const activeColors = ['rgb(22, 83, 255)', 'rgb(24, 144, 255)', 'rgb(64, 158, 255)'];
                        if (activeColors.includes(c)) return true;
                        const fw = parseInt(cs.fontWeight || '400', 10);
                        if (!Number.isNaN(fw) && fw >= 600) return true;
                        if ((el.getAttribute('aria-current') || '').toLowerCase() === 'page') return true;
                        return false;
                    }"""
                )
            )
            if is_style_active:
                return cls + " active-by-style" if cls else "active-by-style"
            # 找到当前路由对应导航项但未命中高亮：返回 class 供断言诊断
            return cls
        except Exception:
            return ""
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
                    try:
                        self.page.wait_for_load_state("domcontentloaded", timeout=2000)
                    except Exception:
                        pass
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
                    try:
                        self.page.wait_for_load_state("domcontentloaded", timeout=1500)
                    except Exception:
                        pass
                    return True
            except Exception:
                continue
        try:
            self.page.keyboard.press("Escape")
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=1500)
            except Exception:
                pass
            return True
        except Exception:
            return False

    def _nav_link_selectors(self, nav_text: str, prefer_button: bool = False) -> list[str]:
        """返回匹配导航项的候选选择器列表

        优先限定在 nav/header 区域内，避免正文同名链接被误点。
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

    def get_nav_texts(self) -> list[str]:
        """获取顶部导航可见链接文本（去重、保序）。"""
        selectors = [
            ".nav-left a",
            ".header-title a",
            ".nav-cneter a",
            ".nav a",
            "header nav a",
            "header a",
            "nav a",
        ]
        seen = set()
        texts: list[str] = []
        for sel in selectors:
            try:
                loc = self.page.locator(sel)
                for i in range(min(loc.count(), 30)):
                    el = loc.nth(i)
                    try:
                        if not el.is_visible(timeout=300):
                            continue
                        t = (el.inner_text() or "").strip()
                    except Exception:
                        continue
                    if not t or t in seen:
                        continue
                    seen.add(t)
                    texts.append(t)
            except Exception:
                continue
        return texts

    def _click_nav_candidate(self, nav_text: str, prefer_button: bool = False) -> bool:
        """按候选选择器依次尝试点击导航项，返回是否点击成功"""
        for sel in self._nav_link_selectors(nav_text, prefer_button):
            try:
                nav = self.first_visible(sel, timeout=1500)
                if nav is None:
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
                if self.first_visible(ds, timeout=800) is None:
                    continue
                link = self.first_visible(f"{ds} a:has-text('{nav_text}')", timeout=1000)
                if link is None:
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
            self.wait_for_load()
            self.wait_for_url_change(old_url)
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=2000)
            except Exception:
                pass
        except Exception:
            pass

