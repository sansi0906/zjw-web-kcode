# 天津市建筑产业互联网平台 - Web UI 自动化测试框架 (zjw-web-kcode)

一个基于 **Playwright + pytest** 的 Web UI 自动化测试框架，专注于[天津市建筑产业互联网平台](http://172.16.1.165:3200/)的功能测试、回归测试和质量保障。

## 架构总览

```
zjw-web-kcode/
├── config/                      # 配置管理（多环境、pydantic-settings）
│   ├── __init__.py
│   └── settings.py              # TestConfig - 集中管理浏览器、环境、报告等配置
├── pages/                       # Page Object Model（POM）
│   ├── __init__.py
│   ├── base_page.py             # 基础页面类（通用操作封装）
│   ├── home_page.py             # 首页
│   ├── supply_hall_page.py      # 供应大厅
│   ├── supply_chain_map_page.py # 供应链地图
│   ├── industry_demand_page.py  # 产业需求
│   ├── industry_news_page.py    # 产业资讯/政策
│   ├── key_project_page.py      # 重点项目
│   ├── all_products_page.py     # 全部商品
│   ├── intelligent_construction_page.py  # 智能建造
│   ├── industry_policy_page.py  # 产业政策
│   ├── industry_association_page.py     # 产业协会
│   ├── achievement_transformation_page.py # 成果转化
│   ├── cloud_service_page.py    # 云服务
│   └── industrial_service_page.py       # 产业化服务
├── tests/                       # 测试用例
│   ├── __init__.py
│   ├── conftest.py              # Fixtures & Hooks（全局）
│   ├── base_page_test.py        # 页面通用测试基类
│   ├── test_homepage_full.py    # 首页全量测试
│   ├── test_supply_hall.py      # 供应大厅测试
│   ├── test_industry_demand.py  # 产业需求测试
│   ├── test_key_projects.py     # 重点项目测试
│   ├── test_industry_news.py    # 产业资讯测试
│   ├── test_all_products.py     # 全部商品测试
│   ├── test_intelligent_construction.py  # 智能建造测试
│   ├── test_industry_policy.py  # 产业政策测试
│   ├── test_industry_association.py     # 产业协会测试
│   ├── test_achievement_transformation.py # 成果转化测试
│   ├── test_cloud_service.py    # 云服务测试
│   ├── test_industrial_service.py       # 产业化服务测试
│   └── test_supply_chain_map.py # 供应链地图测试
├── utils/                       # 工具函数
│   ├── __init__.py
│   └── browser_helpers.py       # 浏览器辅助（跳转、安全点击、网络等待等）
├── data/                        # 测试数据
│   └── test_data.yaml           # YAML 测试数据（环境、用户、筛选关键词等）
├── docs/                        # 文档资料
│   ├── test_cases_homepage.md   # 首页测试用例设计文档
│   ├── bug_review_homepage.md   # 首页缺陷评审
│   └── h5_test_result.md        # H5 测试结果记录
├── scripts/                     # 辅助脚本
│   ├── generate_bug_list.py     # 从 Allure 结果生成缺陷清单（Markdown）
│   ├── export_test_cases_xlsx.py # 导出测试用例到 Excel
│   └── (元素提取、深入分析等生成文件 - 已忽略提交)
├── run_tests.py                 # 测试运行入口
├── generate_report.py           # 自定义 HTML 报告生成器
├── pytest.ini                   # Pytest 配置
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量模板
├── .gitignore                   # Git 忽略规则
└── README.md                    # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

> **可选**：安装 Allure 命令行工具用于报告查看
```bash
# Windows
choco install allure

# macOS
brew install allure

# Linux
snap install allure
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，设置测试地址等
```

默认支持三个环境：`dev` / `staging` / `prod`，在 `.env.example` 中可查看和修改。

### 3. 运行测试

```bash
# 基本运行
python run_tests.py

# 指定环境和测试人员
python run_tests.py --env staging --tester "张三" --remark "冒烟测试"

# 无头模式 + 截图
python run_tests.py --env dev --headless --screenshot-all

# 并行运行（需要 pytest-xdist）
python run_tests.py --parallel 4

# 指定测试地址（覆盖环境配置）
python run_tests.py --test-url "http://172.16.1.165:3200/"

# 清理超过7天的旧报告
python run_tests.py --clean-old --keep-days 7
```

### 4. 查看报告

测试完成后自动生成 Allure HTML 报告：

```bash
allure serve reports/allure-results
```

或手动生成：

```bash
allure generate reports/allure-results -o reports/html --clean
```

也可使用自定义报告生成器：

```bash
python generate_report.py
```

## 架构特点

### 1. Page Object Model（POM）

- 每个页面一个 Page 类，封装元素定位和业务操作
- 测试用例只调用 Page 方法，不直接写 locator
- 页面元素变化只需修改对应 Page 类
- `BasePage` 提供通用操作：点击、输入、等待、截图、断言、弹窗处理

### 2. 配置管理

- 集中管理多环境（dev/staging/prod）
- 支持 `.env` 文件和命令行参数覆盖
- `pydantic-settings` 提供类型校验和默认值
- 配置项包括：浏览器类型、视口、超时、重试、截图策略等

### 3. 测试数据管理

- `data/test_data.yaml` 管理测试数据（环境URL、测试用户、筛选关键词、页面标题）
- `conftest.py` 在 fixture 加载时自动读取 YAML 数据
- 支持多环境数据隔离

### 4. 失败重试

- `pytest-rerunfailures` 自动重试偶发失败
- 在 `pytest.ini` 中配置重试次数（默认 1 次）和间隔（默认 2 秒）

### 5. 并行执行

- `pytest-xdist` 支持多进程并行
- `--parallel N` 参数控制并行数

### 6. 截图与报告

- 失败自动截图并附加到 Allure 报告
- 支持全部测试截图模式（`--screenshot-all`）
- Allure 报告自动记录环境信息、执行时长、截图
- `generate_report.py` 生成自定义 HTML 报告（全局统计、用例明细、失败截图、分类筛选）
- `scripts/generate_bug_list.py` 从 Allure 结果生成缺陷清单（Markdown）

### 7. 自动化缺陷追踪

- 在测试用例中内置 `pytest.xfail` 标记已知缺陷
- 覆盖范围包括：路由不一致、alt 文本缺失、ICP 链接缺失、占位符内容、轮播图缺少导航箭头、缺少返回顶部按钮等

### 8. 测试用例管理

- `scripts/export_test_cases_xlsx.py` 自动从测试代码提取用例信息并导出为 Excel
- 用例编号、模块、页面、标题、Story、严重程度、测试步骤等自动生成

## 环境配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `TEST_ENV` | 环境名称 | `dev` |
| `TEST_BASE_URL` | 测试地址 | `http://172.16.1.165:3200/` |
| `BROWSER_HEADLESS` | 无头模式 | `false` |
| `BROWSER_SLOW_MO` | 慢动作（ms） | `500` |
| `BROWSER_TIMEOUT` | 超时时间（ms） | `30000` |
| `VIEWPORT_WIDTH` | 视口宽度 | `1920` |
| `VIEWPORT_HEIGHT` | 视口高度 | `1080` |
| `BROWSER_TYPE` | 浏览器类型 | `chromium` |
| `SCREENSHOT_ON_FAILURE` | 失败截图 | `true` |
| `RERUNS` | 重试次数 | `1` |
| `RERUNS_DELAY` | 重试间隔（秒） | `2` |
| `PARALLEL_WORKERS` | 并行数 | `1` |
| `TESTER` | 测试人员 | (空) |
| `REMARK` | 测试备注 | (空) |

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--env` | 选择环境：dev / staging / prod |
| `--tester` | 测试人员姓名 |
| `--remark` | 测试备注 |
| `--screenshot-all` | 对所有测试截图（包括通过的） |
| `--headless` | 无头模式运行 |
| `--parallel N` | 并行运行数 |
| `--test-url` | 指定测试地址（覆盖环境配置） |
| `--viewport-width` | 浏览器视口宽度 |
| `--viewport-height` | 浏览器视口高度 |
| `--clean-old` | 清理超过 N 天的旧文件 |
| `--keep-days` | 旧文件保留天数（默认 7） |
| `--no-clean` | 不清理旧报告 |
| `--no-open` | 不自动打开报告 |

## 优先级说明

| 优先级 | 说明 | Allure 标记 |
|--------|------|-------------|
| P0 | 核心流程、阻断性功能 | CRITICAL |
| P1 | 重要分支、主要功能 | NORMAL |
| P2 | 次要场景、边界情况 | MINOR |

## 测试执行顺序

`conftest.py` 中定义了自定义执行顺序，确保首页测试（单页快速模式）优先执行：

```
1. test_homepage_full.py      # 单页快速模式，必须第一个
2. test_key_projects.py
3. test_industry_news.py
4. test_industry_demand.py
5. test_achievement_transformation.py
6. test_cloud_service.py
7. test_all_products.py
8. test_supply_hall.py
```

## 注意事项

1. **选择器稳定性**：优先使用 `data-testid`、`aria-label` 等稳定属性，避免依赖动态 class
2. **等待策略**：统一使用 Playwright 自动等待，避免硬编码 sleep
3. **测试隔离**：每个测试用例独立，不依赖其他用例的执行结果
4. **数据清理**：避免在测试中创建持久化数据，或确保测试结束后清理
5. **敏感信息**： `.env` 文件已加入 `.gitignore`，不会被提交；测试数据中的用户密码为测试用虚拟数据，请在生产环境替换

## 项目依赖

详见 `requirements.txt`：

| 依赖 | 版本 | 用途 |
|------|------|------|
| playwright | 1.45.0 | 浏览器自动化 |
| pytest | 7.4.4 | 测试框架 |
| pytest-playwright | 0.4.0 | Playwright-pytest 集成 |
| allure-pytest | 2.13.2 | Allure 报告 |
| pydantic | 2.9.0 | 数据校验 |
| pydantic-settings | 2.5.0 | 配置管理 |
| pyyaml | 6.0.2 | YAML 解析 |
| pytest-xdist | 3.6.0 | 并行执行 |
| pytest-rerunfailures | 13.0 | 失败重试 |
