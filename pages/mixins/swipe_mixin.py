from playwright.sync_api import Page

class SwipeMixin:
    page: Page

    def swipe_left(self, x: int = 300, y: int = 400, distance: int = 200) -> None:
        """向左滑动（模拟移动端滑动手势）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x - distance, y)
        self.page.mouse.up()
        self.page.wait_for_timeout(800)

    def swipe_right(self, x: int = 100, y: int = 400, distance: int = 200) -> None:
        """向右滑动"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x + distance, y)
        self.page.mouse.up()
        self.page.wait_for_timeout(800)

    def swipe_up(self, x: int = 200, y: int = 600, distance: int = 400) -> None:
        """向上滑动（模拟移动端上滑加载更多）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y - distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1000)

    def swipe_down(self, x: int = 200, y: int = 200, distance: int = 400) -> None:
        """向下滑动"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y + distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1000)

    def pull_to_refresh(self, x: int = 200, y: int = 100, distance: int = 300) -> None:
        """模拟移动端下拉刷新（从页面顶部下拉）"""
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y + distance)
        self.page.mouse.up()
        self.page.wait_for_timeout(1500)
