# 测试维护指南

> 适用项目：zjw-web-kcode（天津市建筑产业互联网平台官网，Playwright + Pytest）
> 测试环境：http://172.16.1.165:3200/

---

## 一、快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行全量测试（默认测试环境 + 无头模式）
python -m pytest -q

# 运行单个文件
python -m pytest tests/test_homepage_full.py -v

# 按用例名过滤
python -m pytest -k "font_consistency" -v

# H5 端（390x844）
python -m pytest --platform h5

# 生成 Allure 报告
python run_tests.py --tester "姓名" --remark "备注"

# 跑生产环境（谨慎：会真实操作生产数据）
python run_tests.py --env prod
```

---

## 二、环境配置

### 2.1 环境只有两套（不存在第三套）

| 环境名 | 地址 | 说明 |
|--------|------|------|
| `test` | `http://172.16.1.165:3200/` | 默认，测试环境 |
| `prod` | `https://www.tjjzcy.com/` | 生产环境 |

环境注册表定义在 `config/settings.py` 的 `ENV_URLS`，是**唯一事实来源**：

```python
ENV_URLS = {
    "test": "http://172.16.1.165:3200/",
    "prod": "https://www.tjjzcy.com/",
}
```

`TEST_ENV` 传了非法值会**直接报错**（`ValidationError: 未知环境 'xxx'`），
不会静默回落到测试地址。

### 2.2 配置优先级

```
命令行参数  >  环境变量 / .env 文件  >  config/settings.py 默认值
```

所有可覆盖配置项的命令行默认值均为 `None`，含义是「**不覆盖，沿用配置**」。
这是保证 `.env` 真正生效的关键 —— 早期版本 CLI 默认值写死为 `1920`/`false`，
把环境变量的值全部覆盖掉了。

### 2.3 环境变量清单（`.env` / `.env.example`，共 13 项）

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `TEST_ENV` | `test` | 选择环境（`test` / `prod`） |
| `TEST_BASE_URL` | 空 | 可选，临时覆盖环境默认地址；留空则用 `ENV_URLS[TEST_ENV]` |
| `BROWSER_HEADLESS` | `true` | 无头模式；`false` 为有头 |
| `BROWSER_SLOW_MO` | `0` | 每个动作额外延迟毫秒数；本地可视化调试可设 `200~500`，CI 建议 `0` |
| `BROWSER_TIMEOUT` | `30000` | 单次操作超时（毫秒） |
| `BROWSER_TYPE` | `chromium` | `chromium` / `firefox` / `webkit` |
| `VIEWPORT_WIDTH` | `1920` | 视口宽 |
| `VIEWPORT_HEIGHT` | `1080` | 视口高 |
| `SCREENSHOT_ON_FAILURE` | `true` | 失败用例是否截图 |
| `RERUNS` | `1` | 失败重试次数 |
| `RERUNS_DELAY` | `2` | 重试间隔（秒） |
| `PARALLEL_WORKERS` | `1` | 并行进程数，`1` 为不并行 |
| `REPORTS_DIR` | `reports` | 报告根目录（相对路径按项目根解析） |
| `LOGS_DIR` | `logs` | 日志目录（相对路径按项目根解析） |
| `PLATFORM` | `web` | `web` / `h5` / `mobile` |
| `DEVICE` | 空 | Playwright 设备名，如 `iPhone 12` |
| `TESTER` / `REMARK` | 空 | 写入 Allure 环境信息 |

截图目录不再单独配置，固定为 `<REPORTS_DIR>/screenshots`。

### 2.4 命令行参数

| 参数 | 说明 |
|------|------|
| `--env test\|prod` | 切换环境 |
| `--test-url URL` | 覆盖测试地址（优先级最高） |
| `--headless` / `--no-headless` | 强制无头 / 有头（覆盖 `BROWSER_HEADLESS`） |
| `--viewport-width` / `--viewport-height` | 覆盖视口 |
| `--platform web\|h5\|mobile` | 切换平台 |
| `--device-name NAME` | Playwright 设备仿真 |
| `--mobile` | 等价 `--platform h5` |
| `--screenshot-all` | 所有用例都截图 |
| `--tester` / `--remark` | 写入 Allure 环境信息 |

`run_tests.py` 额外支持：`--parallel`（并行数）、`--reports-dir`、`--clean-old`、
`--keep-days`、`--no-open`。

> 注意：`--headed` 与 pytest-playwright 内置选项冲突，统一使用 `--no-headless`。

### 2.5 路径解析

`REPORTS_DIR` / `LOGS_DIR` 的相对路径按**项目根目录**解析（`PROJECT_ROOT`），
不受当前工作目录影响。

---

## 三、目录结构

| 路径 | 说明 |
|------|------|
| `pages/` | Page Object 层，每个页面一个类，继承 `BasePage` |
| `tests/` | 测试用例层，功能测试 `test_<页面>.py`，字体一致性 `test_<页面>_fonts.py`，跨页面交互 `test_page_interaction.py` |
| `tests/base_page_test.py` | 通用测试基类，页面级测试类继承后自动获得导航/页脚/悬浮按钮/页面健康度等通用用例 |
| `tests/conftest.py` | fixture 定义（`page`、`shared_page`、各页面对象 fixture） |
| `config/settings.py` | 环境配置（ENV_URLS 环境注册表 + 全部可覆盖项） |
| `docs/` | 测试用例清单、缺陷记录、维护指南 |
| `run_tests.py` | 测试执行 + 报告生成入口 |

---

## 四、编写规范

### 4.1 页面对象（Page Object）

- 所有页面类继承 `BasePage`，公共能力（跳转、滚动、截图、导航点击、断言）一律放基类，**不要在页面类里重复实现**。
- 页面类只保留：**本页独有的选择器常量** + **本页独有的操作方法**。
- 选择器常量统一放在类顶部，使用大写下划线命名（`PAGE_URL`、`SECTION_POLICY`、`VIEW_ALL_BTN`）。
- `open()` 必须返回 `self`，便于链式调用。
- 页面专属的 `open()` 写法：

```python
def open(self) -> "XxxPage":
    base = settings.base_url.rstrip("/")
    self.goto(url=f"{base}{self.PAGE_URL}")
    return self
```

### 4.2 测试用例

- 通用用例（页面加载 / 导航完整性 / 导航高亮 / 在线客服 / 意向填报 / 页脚电话 / 页脚备案 / 横向溢出 / 图片加载）由 `BasePageTest` 继承获得，**不要重复写**。
- 页面专属用例写在页面专属测试类中，用例名以 `test_` 开头，必须有中文 docstring。
- 断言使用 `assert` + 明确的中文失败信息，失败信息要能直接定位问题。
- 每个用例必须能被**单独执行**（不允许依赖前一个用例的页面状态）。

### 4.3 Allure 标签

```python
@allure.feature("页面名")
class TestXxx(BasePageTest):
    @allure.story("业务分组")
    @allure.title("用例标题")
    @allure.severity(allure.severity_level.CRITICAL)  # CRITICAL / NORMAL / MINOR
    def test_xxx(self) -> None:
        ...
```

---

## 五、站点关键事实（踩坑记录）

| 事实 | 说明 |
|------|------|
| 顶部导航容器类名是 `.nav-cneter` | 源码拼写错误（应为 center），选择器必须按此写 |
| 导航"产业政策"指向 `/industryNews` | `/industryPolicy` 只能直接 URL 访问 |
| 商品条目用 `<article>` 渲染 | 供应大厅商品卡片选择器需包含 `article` |
| 供应大厅分类按钮描述含"智能建造" | 点击"智能建造"会误点分类按钮，必须限定导航区选择器 |
| 首页"查看全部"共 3 个 | href 分别为 `/exhibitionActivity`、`/demandPage`、`/industryNews`，需按 href 精确定位 |
| 微前端配置接口异常 | 控制台必报 `Cannot destructure property 'timestamp'`，属环境缺陷 |
| 页面滚动容器 | 首页滚动发生在 `div.relative.w-full.overflow-y-scroll` 内 |
| 重点项目 / 产业政策筛选激活态 class 拼写错误 | 选中项 class 为 `text[#1653FF]`（缺中括号），浏览器不解析，只能靠 `.active-border` 下划线识别 |
| 供应大厅真正筛选在 `/supplyHall/search` | 首页 `/supplyHall` 上的分类项是跳转入口，不是 in-place 筛选 |
| 产业政策 / 产业新闻列表结构不同 | 产业政策用 `div` 列表，产业新闻用 `<article>` 列表 |

### Playwright 选择器坑

1. **逗号列表不能混用 `text=` 与 CSS 引擎**：
   `"text=400-, text=电话, [class*='phone']"` 恒为 0 个匹配。
   统一写成单个 `text=400-115-0629` 形式。
2. **`.first` 可能命中隐藏元素**：站点同时渲染 PC / 移动端两套页脚与悬浮按钮，
   隐藏的那套在 DOM 中排在前。取元素时用「遍历找第一个可见元素」，不要直接 `.first`。
3. **SVG 元素的 `className` 不是字符串**：JS 里判断 class 前先做
   `typeof raw === 'string' ? raw : (raw && raw.baseVal) || ''`。
4. **SPA 路由跳转不会触发 `load` 事件**：点击导航后要显式等待 URL 变化
   （`wait_for_url_change`），否则断言 URL 会竞态失败。
5. **首页共享 page 会被前一个用例污染**：`home_page_shared` 是 module 级 fixture，
   首页测试类用 autouse fixture 在每个用例前 `goto()` 重置。
6. **页码匹配不要用 `has-text()`**：`has-text('2')` 会同时命中 `12` / `20`，
   分页点击必须逐个比对 `text_content()` 做精确匹配。
7. **`:has-text()` 不能传给 `page.evaluate()`**：它不是合法 CSS 选择器，
   只能用 `locator` 系列 API，或改用 `querySelector` 可识别的选择器。

---

## 六、缺陷处理约定

| 场景 | 处理方式 |
|------|---------|
| 站点真实缺陷 | 用 `pytest.xfail("已知缺陷：具体描述")` 标记，缺陷描述要能直接提给开发 |
| 环境数据问题 | 已知问题关键词从失败判定中剔除，仅对未知问题失败；再 `xfail` 说明 |
| 功能已下线 | 整类加 `@pytest.mark.skip(reason="...")`，文件头注明「已废弃，仅作历史参考」 |
| 用例本身写错 | 修用例，不要用 skip 掩盖 |

**原则**：`xfail` 的用例仍需能捕获"新问题"——已知问题剔除后仍要断言，否则等于没测。

---

## 七、字体一致性测试

详见 `docs/font_consistency_test_cases.md`（62 个用例）。

策略要点：
- 按**视觉分组**做同组比对（标题组 / 描述组 / 标签组 / 统计组），不逐元素写死期望值。
- Tab 类元素因激活态颜色不同，比对时排除 `color`。
- 每个用例至少要求找到 2 个可见元素，避免页面改版后用例空跑。
- PC 与 H5 字号为等比缩放关系，不跨端硬比较，只在端内做组内一致性校验。

---

## 八、当前基线（2026-10-22）

| 指标 | 数值 |
|------|------|
| 用例总数 | 446 |
| 通过 | 393 |
| 失败 | 0 |
| 跳过 | 46 |
| 预期失败（xfail） | 7 |
| 全量耗时 | 约 25 分钟（配置优化前约 38 分钟） |

### 跳过用例分布（均为有意跳过）

| 分类 | 数量 | 原因 |
|------|------|------|
| `test_all_products.py` | 12 | 「全部商品」模块改版下线，文件保留作历史参考 |
| `test_supply_chain_map.py` | 13 | 「产业链地图」页面已下线 |
| `test_supply_hall_page.py` | 2 | 旧版供应大厅的统计卡片 / 分页组件已改版 |
| `test_industry_demand.py` 通用用例 | 6 | `/industryDemand` 为旧版页面，无页脚 / 悬浮按钮 / 顶部导航 |
| 导航高亮 | 5 | `/demandPage`、`/industryPolicy` 不在顶部导航中 |
| 移动端手势（首页） | 3 | 仅 H5 端可执行 |
| 供应大厅价格 | 1 | 供应条目未渲染价格元素，属数据现状 |
| 客服 / 意向填报按钮 | 4 | 部分页面未渲染对应悬浮按钮 |

### 预期失败（xfail）用例

| 用例 | 缺陷 |
|------|------|
| `test_no_console_errors` | 微前端配置接口异常导致 `timestamp` 解构报错 |
| `test_no_placeholder_content` | 测试环境残留占位文案 |
| `test_images_alt_text` | 部分内容图片缺少 alt |
| `test_merchant_images_alt` | 商家图片缺少 alt |
| `test_footer_icp_is_link` | 页脚 ICP 备案号为纯文本，缺少超链接 |
| `test_carousel_has_nav_arrows` | 轮播图缺少前后导航箭头 |
| `test_back_to_top_exists` | 首页缺少返回顶部按钮 |

---

## 九、筛选与分页的强断言约定

筛选与分页最容易写出"永真断言"（如 `assert count >= 0`），本项目统一使用以下 API：

### 9.1 筛选

```python
page_obj.assert_filter_effective("房建项目")   # 单项筛选：列表非空 + 切换后内容变化
page_obj.assert_filter_switches_list("房建项目", "市政项目")  # 两项筛选：内容必须不同
```

- `BasePage.apply_filter(label)`：点击筛选项并返回筛选后的列表标题；
  筛选项不存在时直接 `AssertionError`，不会静默跳过。
- `BasePage.get_active_filter_label()`：识别当前选中项，三级判定
  ① `aria-pressed="true"` → ② 子元素 `.active-border` 可见 → ③ 品牌蓝样式
  （文字 `rgb(22, 83, 255)` / 底色 `rgb(228, 241, 255)` / 渐变底 + 白字）。
- `BasePage._prepare_filter(label)`：筛选项不在当前页面时（如供应大厅筛选在搜索页），
  自动调用 `open_filter_source()` 跳到筛选所在页面。子类可覆盖 `open_filter_source()`。

### 9.2 页面类必须登记真实筛选项

```python
FILTER_TABS = {
    "房建项目": ".nav-item:has-text('房建项目')",
    "市政项目": ".nav-item:has-text('市政项目')",
}
```

只登记页面上**确实存在**的筛选项。页面没有筛选时保持 `FILTER_TABS = {}`，
测试用例应直接 `pytest.skip` 而不是写永真断言。

### 9.3 分页

```python
pages = page_obj.get_pagination_pages()      # ['1', '2', '3']
active = page_obj.get_active_pagination_page()  # '1'
page_obj.click_pagination_page("2")           # 精确文本匹配，不会误命中 '12'
```

分页断言必须同时校验 **激活页码变化** 和 **列表内容变化**，两者缺一都可能被"假翻页"骗过。

### 9.4 跨页面交互用例

`tests/test_page_interaction.py` 用 `parametrize` 覆盖 6 个页面的筛选切换与 3 个页面的分页，
新增页面时在 `FILTER_SWITCH_CASES` / `PAGINATION_CASES` 中登记即可。

---

## 十、站点缺陷记录

见 `docs/known_issues.md`（含 6 项站点缺陷 + 7 项测试代码侧已修复问题）。
