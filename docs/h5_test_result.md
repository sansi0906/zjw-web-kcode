# H5首页测试结论（iPhone 12 设备仿真）

## 测试环境
- **设备仿真**：Playwright 内置设备 `iPhone 12`（375×812，User-Agent、DPR、触摸等均模拟真实移动端）
- **测试地址**：http://172.16.1.165:3200/
- **测试框架**：pytest + playwright + allure
- **执行时间**：116.07s

## 测试结果

**62 个测试用例执行结果：**
- **通过（PASSED）**：54 个
- **预期失败（XFAIL）**：6 个（与复核结论一致，均为可优化项或已确认忽略的非Bug）
- **失败（FAILED）**：2 个

## 核心功能测试验证

在 H5 设备仿真下，核心功能均正常：

| 功能模块 | 测试用例 | 结果 | 备注 |
|---|---|---|---|
| Logo 显示与点击 | `test_logo_display`、`test_logo_click` | PASS | 正常 |
| 顶部导航 | `test_nav_links_complete`、各导航跳转用例 | PASS | 导航跳转正常 |
| 轮播图 | 加载、自动播放、图片加载、dots切换 | PASS | 正常 |
| 登录/注册 | `test_login_button`、`test_register_button` | PASS | 均能正常打开相应页面 |
| 搜索框 | `test_search_input`、`test_search_button` | PASS | 正常 |
| 热门搜索 | 展示、点击 | PASS | 正常 |
| 产业服务区 | 加载、卡片展示、了解详情 | PASS | 正常 |
| 津筑云商、会展活动、产业需求、产业政策 | 各相关用例 | PASS | 正常 |
| 页脚 | 电话、ICP、版权、导航 | PASS | 正常 |
| 悬浮按钮（在线客服、意向填报） | 点击及hover | PASS | 正常 |
| 刷新与性能 | `test_page_refresh`、`test_page_load_performance` | PASS | 正常 |

## XFAIL 用例（符合复核结论）

以下 6 个用例按复核结论标记为预期失败（`xfail`）：

| 测试用例 | 对应问题 | 结论 |
|---|---|---|
| `test_policy_nav_route` | 导航“产业政策”路由不一致（BUG-002） | 已复核为“忽略” |
| `test_images_alt_text` | 图片缺少 alt 属性（BUG-003） | 已复核为“忽略” |
| `test_merchant_images_alt` | 津筑云商图片缺少 alt 属性（BUG-003） | 已复核为“忽略” |
| `test_footer_icp_is_link` | 页脚 ICP 未添加超链接（BUG-004） | 经复核认为“实际已可跳转”（非Bug） |
| `test_carousel_has_nav_arrows` | 轮播图缺少前后箭头（BUG-007） | 设计如此（非Bug） |
| `test_back_to_top_exists` | 缺少返回顶部按钮（BUG-008） | 可优化项（OPT-001） |

## FAILED 用例（需关注）

仅 2 个失败用例，均与页面实际情况一致：

| 测试用例 | 原因 | 说明 |
|---|---|---|
| `test_no_console_errors` | 控制台存在微信分享配置报错 `TypeError: Cannot destructure property 'timestamp' of '(intermediate value)' as it is undefined`（BUG-001） | 已复核为“忽略” |
| `test_no_placeholder_content` | 产业政策区存在“测试新增”等测试占位文本（BUG-006）；服务链接区存在“哇哦哇哦哇哦哇哦”等占位文本（BUG-005） | BUG-005、BUG-006 经复核为“非Bug”（设计如此/测试环境原因） |

## 结论

使用 **iPhone 12 设备仿真** 方式对 H5 首页进行测试，结果与 PC 端测试结论一致。

**核心功能在 H5 环境下运行正常。** 上述失败与预期失败均已在 `bug_review_homepage.md` 中复核并明确结论，不影响主业务流程的可用性。