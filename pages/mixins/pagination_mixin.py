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
        """获取当前激活的页码"""
        active = self.page.locator(
            ".n-pagination .n-pagination-item--active, .n-pagination [class*='--active']"
        )
        if active.count() == 0:
            return ""
        return (active.first.text_content() or "").strip()

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
            target.click()
        except Exception:
            try:
                target.evaluate("el => el.click()")
            except Exception:
                return False
        self.page.wait_for_timeout(2000)
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

