from playwright.sync_api import Page

class FilterMixin:
    page: Page

    def get_filter_labels(self) -> list[str]:
        """获取本页真实存在的筛选项文案"""
        return list(self.FILTER_TABS.keys())

    def get_list_titles(self) -> list[str]:
        """获取列表条目标题（子类覆盖，用于筛选/分页断言）"""
        return []

    def apply_filter(self, label: str) -> list[str]:
        """点击筛选项并返回筛选后的列表标题

        :raises AssertionError: 筛选项在页面上不存在
        """
        self._prepare_filter(label)
        selector = self.FILTER_TABS.get(label, f"text={label}")
        el = self.page.locator(selector).first
        if not el.is_visible(timeout=3000):
            raise AssertionError(f"筛选项 '{label}' 在页面上不存在（选择器 {selector}）")
        el.click()
        self.page.wait_for_timeout(1500)
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        return self.get_list_titles()

    def _prepare_filter(self, label: str) -> None:
        """确保筛选项所在页面已加载（筛选入口在子页面时重新打开）"""
        selector = self.FILTER_TABS.get(label, f"text={label}")
        try:
            el = self.page.locator(selector).first
            if el.count() > 0 and el.is_visible(timeout=2000):
                return
        except Exception:
            pass
        self.open_filter_source()
        self.page.wait_for_timeout(1500)

    def open_filter_source(self) -> None:
        """打开筛选所在页面（子类可覆盖，例如供应大厅筛选在搜索页）"""
        self.open()

    def get_active_filter_label(self) -> str:
        """推断当前选中的筛选项

        判定顺序（逐个筛选项检查，命中即返回）：
        1. aria-pressed="true"
        2. 子元素 .active-border 可见（重点项目 / 产业政策的下划线标记）
        3. 品牌蓝文字色 rgb(22, 83, 255)（产业需求 / 成果转化）
        4. 选中底色 rgb(228, 241, 255)
        5. 渐变背景 + 白色文字（产业新闻）
        无法区分时返回空字符串（调用方据此放宽断言）。
        """
        labels = self.get_filter_labels()
        if len(labels) < 2:
            return ""

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            if (el.get_attribute("aria-pressed") or "").lower() == "true":
                return label

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            border = el.locator(".active-border")
            if border.count() and border.first.is_visible():
                return label

        for label in labels:
            el = self._filter_element(label)
            if el is None:
                continue
            if self._is_styled_active(el):
                return label

        return ""

    def _filter_element(self, label: str):
        """获取筛选项元素（不可见时返回 None）"""
        selector = self.FILTER_TABS.get(label, f"text={label}")
        try:
            el = self.page.locator(selector).first
            if el.count() == 0 or not el.is_visible(timeout=2000):
                return None
            return el
        except Exception:
            return None

    @staticmethod
    def _is_styled_active(el) -> bool:
        """根据计算样式判断筛选项是否为选中态

        站点使用品牌蓝 #1653FF 文字、浅蓝 #E4F1FF 底色、蓝色渐变底 + 白字
        三种方式标记选中项。
        """
        try:
            return bool(el.evaluate(
                """el => {
                    const cs = getComputedStyle(el);
                    const activeBlue = 'rgb(22, 83, 255)';
                    const activeBg = 'rgb(228, 241, 255)';
                    if (cs.color === activeBlue) return true;
                    if (cs.backgroundColor === activeBg) return true;
                    const bgImage = cs.backgroundImage || '';
                    if (bgImage.includes('gradient') && cs.color === 'rgb(255, 255, 255)') return true;
                    return false;
                }"""
            ))
        except Exception:
            return False

    def assert_filter_effective(self, filter_name: str) -> list[str]:
        """断言筛选生效

        1. 筛选项必须真实存在
        2. 筛选后列表不能为空
        3. 若该筛选项原本不是选中项，筛选后列表内容必须发生变化
        :return: 筛选后的列表标题
        """
        if filter_name not in self.FILTER_TABS:
            raise AssertionError(
                f"筛选项 '{filter_name}' 未在页面登记，实际可选项: {self.get_filter_labels()}"
            )
        self._prepare_filter(filter_name)
        active_before = self.get_active_filter_label()
        before = self.get_list_titles()
        self.apply_filter(filter_name)
        after = self.get_list_titles()
        assert after, f"筛选 '{filter_name}' 后列表为空"
        if active_before and active_before != filter_name:
            assert after != before, (
                f"筛选 '{filter_name}' 后列表内容未变化（筛选未生效）"
            )
        return after

    def assert_filter_switches_list(self, label_a: str, label_b: str) -> None:
        """断言两个筛选项切换后列表内容不同（证明筛选真正生效）

        相比"数量 >= 0"这类永真断言，本方法能捕获：
        - 筛选点击无响应
        - 筛选后列表为空
        - 多个筛选项返回同一份数据
        """
        titles_a = self.apply_filter(label_a)
        titles_b = self.apply_filter(label_b)
        assert titles_a, f"筛选 '{label_a}' 后列表为空"
        assert titles_b, f"筛选 '{label_b}' 后列表为空"
        assert titles_a != titles_b, (
            f"筛选 '{label_a}' 与 '{label_b}' 的列表内容完全相同，筛选可能未生效"
        )

    # ==================== 移动端手势 ====================

