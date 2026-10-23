# 测试环境缺陷清单

> 采集环境：`http://172.16.1.165:3200/`（dev）
> 采集方式：Playwright 全站采集（首页 / 供应大厅 / 供应大厅搜索页 / 智能建造 / 重点项目 / 产业政策 / 产业新闻 / 产业协会 / 成果转化 / 云服务 / 产业需求）
> 采集日期：2026-10-22

本清单记录**被测站点（前端）**在测试环境存在的问题。自动化用例对已知缺陷采用 `pytest.xfail` 标注，
待站点修复后用例会自动恢复为 PASSED，无需改测试代码。

---

## DEF-001 微信分享配置读取 timestamp 报错（阻塞级）

| 项 | 内容 |
|---|---|
| 严重级别 | 严重（阻断级，全站复现） |
| 影响范围 | 全部 11 个页面均复现 |
| 复现步骤 | 打开任意页面 → 等待页面加载完成 → 查看浏览器控制台 |
| 实际结果 | `微信分享配置失败: TypeError: Cannot destructure property 'timestamp' of '(intermediate value)' as it is undefined.`<br>`at Object.config (/_nuxt/entry.3189a29e.js:34:49813)` |
| 期望结果 | 微信分享配置读取时应有兜底判断，读取不到配置不应抛出未捕获异常 |
| 初步定位 | 分享配置接口返回体中缺少 `timestamp` 字段，前端直接解构导致异常；或接口未按非 200 状态返回，被当作成功处理 |
| 用例处理 | `tests/test_homepage_full.py::TestHomePage::test_no_console_errors` — 已知错误 `xfail`，出现新的未知错误仍然 FAIL |
| 建议 | ① 接口未返回时增加空值兜底；② 补充 `timestamp` 字段；③ 前端对分享能力做降级（失败时静默跳过） |

---

## DEF-002 测试数据残留占位内容

| 项 | 内容 |
|---|---|
| 严重级别 | 一般（数据质量） |
| 影响范围 | 产业新闻、成果转化、产业协会等模块的列表数据 |
| 实际结果 | 列表中出现如下占位文本：<br>• 产业新闻：`这是标题这是标题这是标题…`、`饿飞飞飞我分为`、`成为成为分为访问为访问…`、`测试新增`<br>• 产业新闻简介：`时代大厦是的是的是多少打撒`<br>• 产业协会：`泥嚎哇` |
| 期望结果 | 正式环境不应出现无意义占位文本 |
| 用例处理 | `tests/test_homepage_full.py::TestHomePage::test_no_placeholder_content` — 已知占位词 `xfail`，新增未知占位词仍 FAIL |
| 建议 | 清理演示/压测数据，或按环境隔离测试库数据 |

---

## DEF-003 图片缺少 alt 属性（无障碍）

| 项 | 内容 |
|---|---|
| 严重级别 | 轻微（无障碍 / SEO） |
| 影响范围 | 全站 | 
| 实际结果 | 首页 86 张图片中 77 张无 `alt`；供应大厅 85 张中 32 张无 `alt`；重点项目 19 张中 18 张无 `alt`；产业政策 10 张中 9 张无 `alt`；云服务 14 张中 13 张无 `alt`；成果转化 14 张中 13 张无 `alt`；产业需求 18 张中 17 张无 `alt`；智能建造 22 张中 21 张无 `alt`；产业新闻 13 张中 4 张无 `alt`；产业协会 17 张中 6 张无 `alt`；供应大厅搜索页 41 张中 10 张无 `alt` |
| 期望结果 | 装饰性图片使用 `alt=""`，语义图片应有描述性 `alt` |
| 用例处理 | 暂未写成硬断言，避免大面积噪声；建议修复后补充 |
| 建议 | 前端模板补齐 `alt` 属性，装饰图统一 `alt=""` |

---

## DEF-004 存在无可访问名称的表单控件

| 项 | 内容 |
|---|---|
| 严重级别 | 轻微（无障碍） |
| 影响范围 | 供应大厅搜索页、智能建造、重点项目、产业政策、产业新闻、产业需求 |
| 实际结果 | 各存在 1 个 `<input>`，无 `id`+`label[for]` 关联、无 `aria-label`、无 `placeholder`、无 `title` |
| 期望结果 | 表单控件应有可访问名称 |
| 用例处理 | 暂未写成硬断言 |
| 建议 | 为搜索框 / 隐藏分页输入框补充 `aria-label` 或 `title` |

---

## DEF-005 重点项目 / 产业政策 导航激活态 class 拼写错误（次要）

| 项 | 内容 |
|---|---|
| 严重级别 | 轻微（样式实现瑕疵） |
| 影响范围 | 重点项目、产业政策 |
| 实际结果 | 选中项 class 为 `text[#1653FF]`（缺少中括号），非标准 Tailwind 语法，浏览器不会解析，因此选中项文字颜色与未选中项一致（均为 `rgb(51, 51, 51)`），仅靠子元素 `.active-border`（下划线）区分 |
| 期望结果 | 应为 `text-[#1653FF]`，选中项文字高亮为品牌蓝 |
| 用例处理 | `tests/base_page_test.py::BasePageTest::test_no_horizontal_overflow` 等不受影响；筛选选中态通过 `.active-border` 可见性识别，已在 `BasePage.get_active_filter_label()` 中兼容 |
| 建议 | 修正 class 拼写为 `text-[#1653FF]`，同步检查其他页面是否存在同类写法 |

---

## DEF-006 产业新闻 / 产业政策 / 成果转化 存在无意义文案

| 项 | 内容 |
|---|---|
| 严重级别 | 一般（数据质量） |
| 影响范围 | 产业新闻、成果转化 |
| 实际结果 | 产业新闻列表含 `饿飞飞飞我分为`、`成为成为分为访问为访问…`；成果转化列表首条为 `复杂环境下适应性深基坑智能建造技术的研发` 的重复占位 |
| 期望结果 | 列表内容为真实业务数据 |
| 用例处理 | 见 DEF-002 |
| 建议 | 与 DEF-002 一并处理 |

---

## 已修复（测试代码侧）

| 编号 | 说明 |
|---|---|
| FIX-001 | `pages/industry_policy_page.py` 的 `get_active_filter()` 引用了不存在的 `FILTER_政策咨询`（实际为 `FILTER_政策资讯`），调用即抛 `AttributeError` |
| FIX-002 | `pages/key_project_page.py` 中 `assert_filter_works` 被重复定义，后定义的弱断言（`count >= 0`）覆盖了强断言，导致筛选用例形同虚设 |
| FIX-003 | `BasePage.click_pagination_page()` 使用 `has-text()` 匹配页码，会误命中 `12` / `20` 等页码，改为精确文本匹配 |
| FIX-004 | `BasePage.get_pagination_pages()` 未过滤上一页/下一页按钮的空文本，导致页码列表混入空字符串 |
| FIX-005 | 供应大厅原筛选定位 `li[class*='mx-[12px]'] span` 命中的是首页分类入口（点击后跳转 `/supplyHall/search`），并非 in-place 筛选；改为搜索页"一级分类"行按钮（带 `aria-pressed`） |
| FIX-006 | `BasePage.get_active_filter_label()` 原按 class 少数派推断选中项，在 2 个筛选项时必然误判；改为按 `aria-pressed` → `.active-border` 可见 → 品牌蓝样式三级判定 |
| FIX-007 | `tests/base_page_test.py` 编辑时 `def` 行与 docstring 被合并到同一行，导致 `IndentationError` 使整个测试集无法收集 |
| FIX-008 | 配置项 `TEST_ENV` / `BROWSER_TYPE` / `RERUNS` / `PARALLEL_WORKERS` / `VIEWPORT_*` / `PLATFORM` / `DEVICE` 等定义后**完全未生效**：CLI 默认值写死并覆盖了配置，`env_urls` 映射是死代码。已改为「CLI 默认 None = 不覆盖」，并让 `BROWSER_TYPE` 真正选择浏览器内核、`RERUNS` 真正驱动重试 |
| FIX-009 | `.env.example` 的 `TEST_BASE_URL` 指向**生产**地址，照抄即打生产站点。已改回测试环境并改为可选覆盖项 |
| FIX-010 | `settings.base_url` 是可写字段且有非空默认值，导致 `--env staging/prod` 无法切换地址。已改为只读属性（由 `TEST_ENV` + `TEST_BASE_URL` 共同决定），并对非法环境名快速报错 |
| FIX-011 | `page` fixture 每个用例都先 `goto(base_url)` 加载首页，随后页面对象又 `open()` 一次，重复加载。全量耗时因此多出约 13 分钟。已去掉初始导航，改由 `BasePage.goto()` 等待网络空闲 |
| FIX-012 | `BasePage.assert_text_visible()` 直接 `locator.count()`，冷加载时接口数据尚未渲染，断言抢跑失败。已改为先 `wait_for(state="attached")` 再判断可见性 |
| FIX-013 | `BROWSER_SLOW_MO` 默认 500ms（每个动作额外延迟 0.5s），是全量耗时第二大来源。默认改为 0，本地可视化调试时再调高 |
| FIX-014 | 死配置项清理：删除 `api_url`（全项目未使用）、`EnvConfig`（`base_url` 的多余包装）、`SCREENSHOT_ON_PASS`（与 `--screenshot-all` 重复）、`ALLURE_RESULTS_DIR`（pytest-allure 不读该变量）、`SCREENSHOTS_DIR`（改为由 `REPORTS_DIR` 派生） |

---

## 复现脚本

本次采集使用的探针脚本位于仓库根目录的 `tmp_probe_*.py`（临时文件，收尾时已删除）。
如需重新采集，可参考 `docs/test_maintenance_guide.md` 中的"全站健康度巡检"章节自行编写。
