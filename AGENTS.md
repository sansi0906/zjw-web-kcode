# AGENTS / 项目运行与维护约定

## 目标
天津市建筑产业互联网平台 UI 自动化（Playwright + pytest，POM/mixins）。

## 常用命令
- 预检（推荐 CI/本地先跑）：`python scripts/precheck.py`（`--quick` 跳过 compileall）
- YAML 校验：`python scripts/validate_test_data.py`
- 收集测试：`python -m pytest --collect-only -q -p no:rerunfailures`
- 全量运行：`python run_tests.py ...` 或 `python -m pytest`
- xdist 隔离并行（仅无状态子集）：`python -m pytest -n auto -m "not serial"`
- 串行/有状态：`python -m pytest -m serial`（或不加 `-n`）
- 设备/浏览器矩阵（无状态冒烟子集）：`python scripts/matrix_run.py --list` / `--quick` / `--full` / `--matrix web_1366,ipad`（汇总写 `reports/matrix/matrix_*.md|json`）
- 视觉回归：`python -m pytest -m visual --visual`（首次生成基线后跳过，再次运行按 `--visual-threshold` 对比；基线在 `reports/visual/baseline`）
- a11y 基础：`python -m pytest -m a11y`
- 异常/韧性：`python -m pytest tests/test_error_pages.py tests/test_resilience.py`

## Marker 策略
- `smoke`：核心门禁（含各页继承 `test_page_load` + 关键首页导航/搜索）
- `regression`：回归主集
- `serial`：**必须串行**；依赖 `shared_page/home_page_shared`（module）或有状态页面跳转/共享上下文。**不要**与 xdist 混跑，除非 `-m "not serial"`
- `fonts` / `interaction` / `homepage` / `navigation` / `search` / `h5`：按场景筛选（H5/移动端用例必须标记 `h5`，推荐同时带 `smoke`/`regression`/`navigation`/`search` 等业务 marker）
- `a11y`：可访问性基础检查；`visual`：视觉回归（默认跳过，需 `--visual`）；`matrix`：设备/浏览器矩阵（`scripts/matrix_run.py` 使用）
- `--strict-markers` 已启用；新增 marker 请同步 `pytest.ini`

## 等待策略（硬等待治理）
- 禁止批量替换 `wait_for_timeout`；按文件/方法逐步改为可观察等待：`expect` / `wait_for_url` / `wait_for_load_state` / `wait_for_function` / 轮询。
- 仅在**无可靠 DOM/状态事件**且有注释说明时保留极短兜底（当前仅 `tests/test_homepage_full.py` 中 hover 截图前 200ms）。
- 轮询间隔（如 `tests/test_key_projects.py` 翻页后比对列表文本的 200ms 间隔）属于显式轮询循环，不算硬等待兜底。
- 已知破损图白名单：`data/test_data.yaml.ui_quality.default.broken_images.allow_src_substrings`（子串匹配 src），`BasePage._broken_image_allowlist()` 读取；新增已知破损图优先配置而非硬编码。
- 导航完整性断言：`tests/base_page_test.py.test_nav_completeness` 默认从 `data/test_data.yaml.navigation.home_page.nav_links` 读取预期导航文本（站点配置驱动），不再硬编码「云服务」；页面对象可通过 `EXPECTED_NAV_TEXTS` 显式覆盖。

## 数据与防漂移
- 集中数据：`data/test_data.yaml`（含 `schema_version`）。易变站点文案使用 `min_visible` / `optional` / `scroll_into_view`。
- 字体检查优先复用 `utils/font_assert.run_font_check` + YAML；新增页面字体项按 `font_tests.<page>` 扩展。
- UI 质量检查优先复用 `utils/ui_quality` + `data/test_data.yaml.ui_quality`（`default` + 页面覆盖）：控制台已知错误白名单/xfail、图片 alt 阈值、占位文案白名单、轮播箭头/返回顶部等已知缺陷条件均配置驱动；新增页面检查时优先配置 `page_key` 覆盖而非硬编码。
- `conftest.load_test_data()` 启动时做结构校验；CI 以 `scripts/precheck.py` 为准。

## 并行/隔离与 H5 规范
- function-scope `page` 为默认隔离路径；`home_page_shared`/`shared_page` 为 module-scope，仅用于 `serial`/共享页快速遍历。
- H5 用例优先使用 `h5_page` / `h5_*_page` fixture（强制移动端设备仿真）并标记 `@pytest.mark.h5`；`h5` 测试可通过 `-m h5` 单独收集/执行。`test_homepage_h5_fonts.py` 当前为 `serial` 且内部设置 viewport，后续新增 H5 功能用例优先复用统一 fixture。
- 元素定位需兼容 PC/H5 双套 DOM：优先使用 `BasePage.first_visible()` / `BasePage.visible_locator()` 或页面对象封装的可见元素方法，避免 `locator(...).first` 命中隐藏节点；H5 搜索/入口等控件需在可见节点上操作。
- 路由门禁：页面对象可实现 `is_not_found_page()` 保护（404/Nuxt 未找到页）并 `pytest.skip`，基类通用用例也会对 404 做前提跳过；路由下线/未上线应作为“前提不满足”处理，不误报为元素缺陷。

## 可观测性与报告分层
- Allure：`reports/allure-results/`；`environment.properties` 含环境/浏览器/平台/视口/`xdist_workers`/`marker_expr`。
- 失败附件：截图 + 失败时 URL；字体断言失败附 `font_diagnostics` JSON（`utils/font_assert.py`）。
- 报告/BUG 清单分层（`run_tests.py`）：`failed/broken` 为失败，`skipped` 区分 **已知缺陷(xfail)** 与 **前提/环境跳过**（404 路由未上线、移动端专属、页面不要求导航高亮/映射、无数据/无分页等）。
- 路由可用性矩阵：`python -c "import run_tests; run_tests.generate_route_matrix('reports')"` 生成 `reports/route_availability_matrix.md`（基于页面对象 `PAGE_URL`/`ROUTE_STATUS`/`SKIP_NAV_ACTIVE_ASSERT`/404 门禁元数据）；BUG 清单生成时会尝试同步刷新。
- 产物目录：`reports/`、`reports/screenshots/`、`logs/`。

## 站点实现约定（新增用例需遵循）
- 首页轮播：Web 端无 `<a>` 包裹，点击当前 slide 由前端路由跳转（实测 `/robot`）；自动轮播实测约 5s，阈值由 `data/test_data.yaml.carousel.web.auto_rotate_timeout_ms`（8000）控制；图片未配置链接时用例按前提 `skip`。
- 会展活动：列表 → `/exhibitionActivity/detail/<id>` 为同页路由跳转，由“了解详情”按钮驱动（卡片不可点）；`pages/exhibition_page.py` 按按钮→卡片标题映射断言一致性。
- 登录：为首页弹窗（非 `/login`），账号 + 验证码 + 协议勾选；未勾选协议/空表单由受控组件拦截并提示。注册：`/register`，必填项/协议未满足时“提交注册”禁用。
- H5 菜单：全屏遮罩 `div[class*='top-[48px]']` + 导航列表；遮罩点击可关闭，**Esc 关闭未实现**（`test_h5_menu_escape_close` 按前提 skip）。
- 404：Nuxt 未匹配路由返回 `404 / Page not found: <path> / Go back home`，Web/H5 一致。
- 产业金融：`/finance`，H1 产业金融发展/平台支持企业融资；卡片 `.finance-card`（标题 h3：支持融资/合同融资/农务工支持融资，按钮 查看详情/申请融资）；顶部功能按钮（平台支持企业融资/企业融资/查看全部/申请融资）；悬浮 在线客服/意向填报。

## 修改后验证（最小集）
1. `python -m compileall -q <changed>`
2. 受影响 `python -m pytest --collect-only -q <paths> -p no:rerunfailures`
3. 全量 `python -m pytest --collect-only -q -p no:rerunfailures`（或 `scripts/precheck.py --quick`）
