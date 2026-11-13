"""
会展活动 Page Object
"""
from __future__ import annotations

from config.settings import settings
from pages.base_page import BasePage


class ExhibitionPage(BasePage):
    """会展活动列表/详情页"""

    PAGE_URL = "/exhibitionActivity"
    DETAIL_URL_FRAGMENT = "/exhibitionActivity/detail/"

    # 列表卡片（站点使用 div 卡片 + 内部 h3 标题）
    CARD = "div[class*='card'], article, [class*='exhibition']"
    TITLE = "h3, h2, [class*='title']"
    DETAIL_BTN = "text=了解详情"

    def open(self) -> "ExhibitionPage":
        base = settings.base_url.rstrip("/")
        self.goto(url=f"{base}{self.PAGE_URL}")
        return self

    def get_activity_titles(self) -> list[str]:
        """获取会展活动标题列表（与“了解详情”按钮一一对应，避免命中页面标题）"""
        try:
            return self.page.evaluate(
                """() => {
                const isDetailBtn = (e) => (e.textContent || '').trim() === '了解详情';
                const btns = Array.from(document.querySelectorAll('button, a, div, span')).filter(isDetailBtn);
                const out = [];
                for (const b of btns) {
                    let p = b;
                    let title = '';
                    for (let i = 0; i < 6 && p; i++) {
                        p = p.parentElement;
                        if (!p) break;
                        const h = p.querySelector('h3, h2');
                        if (h && (h.innerText || '').trim()) { title = (h.innerText || '').trim(); break; }
                    }
                    if (title) out.push(title);
                }
                return out;
                }"""
            ) or []
        except Exception:
            return []

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（供筛选/分页断言使用）"""
        return self.get_activity_titles()

    def open_first_detail(self) -> str:
        """点击第一个'了解详情'，返回详情页 URL

        站点详情为同页路由跳转（非新标签页）。
        """
        btn = self.page.locator("text=了解详情").first
        if not btn.is_visible(timeout=3000):
            raise AssertionError("未找到'了解详情'按钮")
        old_url = self.page.url
        btn.click()
        try:
            self.page.wait_for_url(lambda u: u != old_url, timeout=8000)
        except Exception:
            pass
        return self.page.url

    def has_pagination(self) -> bool:
        """是否存在分页控件"""
        return self.page.locator(".n-pagination, [class*='pagination'], [class*='pager']").count() > 0

    def assert_page_loaded(self) -> None:
        """断言会展活动页面加载完成"""
        if self.is_not_found_page():
            raise AssertionError("会展活动页面返回 404/未找到页")
        self.assert_text_visible("会展活动", partial=True)

    def scroll_to_footer(self) -> None:
        """滚动到页脚"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=3000)
        except Exception:
            pass