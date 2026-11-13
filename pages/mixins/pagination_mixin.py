from playwright.sync_api import Page

class PaginationMixin:
    page: Page

    def get_pagination_pages(self) -> list[str]:
        """获取分页组件中的页码列表（Naive UI .n-pagination）"""
        items = self.page.locator(
            ".n-pagination .n-pagination-item, .n-pagination [class*='pagination-item']"
        )
        pages = []
        for i in range(items.count()):
            text = (items.nth(i).text_content() or "").strip()
            # 上一页/下一页按钮的文本为空，需过滤
            if text:
                pages.append(text)
        return pages

    def get_active_pagination_page(self) -> str:
        """获取当前激活的页码（兼容 Naive UI / Element Plus 等）"""
        import re

        selectors = [
            ".n-pagination .n-pagination-item--active",
            ".n-pagination .n-pagination-item.n-pagination-item--active",
            ".n-pagination button.n-pagination-item--active",
            ".n-pagination [class*='pagination-item'][class*='--active']",
            ".n-pagination [aria-current='page']",
            ".el-pagination .is-active",
            ".el-pager li.active",
            "[class*='pagination'] .active",
            "[class*='pagination'] [aria-current='page']",
        ]
        for sel in selectors:
            try:
                loc = self.page.locator(sel)
                if loc.count() == 0:
                    continue
                el = loc.first
                if not el.is_visible(timeout=800):
                    continue
                text = (el.text_content(timeout=1500) or "").strip()
                m = re.search(r"\d+", text)
                if m:
                    return m.group()
            except Exception:
                continue
        # 兜底：遍历页码项，按 class/aria 推断激活态
        try:
            items = self.page.locator(".n-pagination .n-pagination-item")
            for i in range(items.count()):
                el = items.nth(i)
                try:
                    cls = (el.get_attribute("class") or "")
                    aria = (el.get_attribute("aria-current") or "")
                    if "--active" in cls or "active" in cls.split() or aria == "page":
                        text = (el.text_content(timeout=1000) or "").strip()
                        m = re.search(r"\d+", text)
                        if m:
                            return m.group()
                except Exception:
                    continue
        except Exception:
            pass
        return ""

    def wait_for_active_page(self, page_no: str, timeout: int = 5000) -> bool:
        """等待分页激活页变为指定页码"""
        target = str(page_no)
        try:
            self.page.wait_for_function(
                r"""(n) => {
                    const norm = (t) => ((t || '').replace(/\s+/g, '').trim());
                    const isActive = (el) => {
                        if (!el) return false;
                        const cls = (el.className || '').toString();
                        const aria = (el.getAttribute('aria-current') || '').toLowerCase();
                        return /--active/.test(cls) || /\bactive\b/.test(cls) || aria === 'page';
                    };
                    const items = Array.from(document.querySelectorAll('.n-pagination .n-pagination-item, .n-pagination [class*="pagination-item"], .el-pager li, [class*="pagination"] [class*="item"]'));
                    for (const el of items) {
                        const text = norm(el.textContent);
                        if (text !== String(n)) continue;
                        if (isActive(el)) return true;
                    }
                    const active = document.querySelector('.n-pagination .n-pagination-item--active, .n-pagination [aria-current="page"], .el-pagination .is-active, .el-pager li.active, [class*="pagination"] [aria-current="page"]');
                    return !!(active && norm(active.textContent) === String(n));
                }""",
                arg=target,
                timeout=timeout,
            )
            return True
        except Exception:
            return self.get_active_pagination_page() == target

    def wait_for_list_titles_change(self, before: list[str], timeout: int = 6000) -> bool:
        """等待列表标题发生变化（用于翻页/筛选后内容刷新判定）"""
        getter = getattr(self, "get_list_titles", None)
        if not callable(getter):
            return False
        import time

        deadline = time.time() + timeout / 1000.0
        while time.time() < deadline:
            try:
                now = getter()
                if now and now != before:
                    return True
            except Exception:
                pass
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=300)
            except Exception:
                time.sleep(0.2)
        try:
            now = getter()
            return bool(now) and now != before
        except Exception:
            return False

    def wait_for_list_titles_stable(self, expected: list[str] | None = None, timeout: int = 5000) -> list[str]:
        """等待列表标题稳定（可选要求与 expected 一致）"""
        getter = getattr(self, "get_list_titles", None)
        if not callable(getter):
            return []
        import time

        deadline = time.time() + timeout / 1000.0
        last = None
        stable_count = 0
        while time.time() < deadline:
            try:
                now = getter()
            except Exception:
                now = []
            if now:
                if now == last:
                    stable_count += 1
                else:
                    stable_count = 0
                    last = now
                if stable_count >= 2 and (expected is None or now == expected):
                    return now
                if expected is not None and now == expected:
                    return now
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=250)
            except Exception:
                time.sleep(0.2)
        try:
            return getter()
        except Exception:
            return last or []

    def click_pagination_page(self, page_no: str) -> bool:
        """点击指定页码，返回是否点击成功

        使用精确文本匹配，避免 `has-text('2')` 误命中 '12' / '20' 等页码。
        """
        items = self.page.locator(".n-pagination .n-pagination-item")
        target = None
        for i in range(items.count()):
            el = items.nth(i)
            if (el.text_content() or "").strip() != str(page_no):
                continue
            if el.is_visible(timeout=2000):
                target = el
                break
        if target is None:
            return False
        try:
            target.scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass
        try:
            target.click()
        except Exception:
            try:
                target.evaluate("el => el.click()")
            except Exception:
                return False
        # 等待激活页切换与内容刷新（站点可能异步请求）
        self.wait_for_active_page(str(page_no), timeout=5000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=2000)
            except Exception:
                pass
        return True

    def get_list_signature(self, selector: str) -> str:
        """获取列表区域的内容指纹（用于判断筛选/翻页后内容是否变化）"""
        return self.page.evaluate(
            """(sel) => {
                const el = document.querySelector(sel);
                if (!el) return '';
                return (el.innerText || '').replace(/\\s+/g, ' ').trim();
            }""",
            selector,
        )

    def get_body_signature(self) -> str:
        """获取页面主体文本指纹（用于判断内容是否变化）"""
        return self.page.evaluate(
            """() => (document.body.innerText || '').replace(/\\s+/g, ' ').trim()"""
        )

    # ==================== 筛选 ====================

