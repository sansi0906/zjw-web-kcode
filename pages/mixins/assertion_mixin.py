from playwright.sync_api import Page, expect

class AssertionMixin:
    page: Page

    def assert_text_visible(self, text: str, partial: bool = True) -> None:
        """断言页面包含指定文本（等待渲染完成，再取第一个可见元素）

        Nuxt SPA 的 'load' 事件早于接口数据渲染，元素可能稍晚才出现，
        因此这里先等待元素挂载，再判断可见性。
        """
        locator = self.page.locator(f"text={text}")
        try:
            locator.first.wait_for(state="attached", timeout=10000)
        except Exception:
            pass
        count = locator.count()
        for i in range(count):
            el = locator.nth(i)
            try:
                if el.is_visible():
                    if partial:
                        expect(el).to_be_visible(timeout=10000)
                    else:
                        expect(el).to_have_text(text, timeout=10000)
                    return
            except Exception:
                continue
        raise AssertionError(f"页面未找到可见文本: {text}")

    def assert_url_contains(self, fragment: str) -> None:
        """断言 URL 包含指定片段"""
        url = self.page.url
        assert fragment in url, f"URL 不包含 '{fragment}'，实际 URL: {url}"

    def assert_element_count(
        self, selector: str, min_count: int = 1
    ) -> None:
        """断言元素数量 >= min_count"""
        count = self.page.locator(selector).count()
        assert count >= min_count, (
            f"期望元素 [{selector}] 数量 >= {min_count}，实际为 {count}"
        )

    def assert_page_loaded(self) -> None:
        """断言页面加载完成（基类默认实现，子类可Override）"""
        self.assert_text_visible("首页", partial=True)

    # ==================== 页面健康度 / 交互 ====================

