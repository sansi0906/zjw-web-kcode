# 近 7 日处理内容

## 提交记录
- 224dab7 refactor: base_page拆分为mixin、删除废弃测试、ICP用例修正
- a04b2e2 chore: remove stray _report_gen_class.py temp file
- d5790d7 refactor: 整合测试报告与缺陷清单生成
- 98218f3 refactor: 清理无用代码
- becb484 feat: 环境配置优化 + 筛选/分页强断言 + 缺陷清单
- 049d01d feat: 完善新版官网测试覆盖
- d7cc8d7 ci: 添加 GitHub Actions UI 测试工作流
- 41cde4b refactor: conftest移除废弃页面fixture，清理pytest.ini BOM
- 9d2921c ci: 集成 allure 结果上传
- d8f3217 feat: 增加 broken image 断言与 console error 收集 fixture

## 主要调整
1. base_page 拆分为 Navigation/Filter/Pagination/Swipe/Assertion 五个 mixin
2. 删除废弃测试文件（all_products、supply_chain_map、supply_hall_page）
3. 修复 ICP 用例：改为点击验证跳转工信部备案页
4. conftest 移除废弃页面 fixture，清理 pytest.ini BOM
5. CI 集成 GitHub Actions + allure 结果上传
6. 新增 assert_no_broken_images 与 console_errors fixture
7. 测试覆盖：9 主页 + H5，字体一致性 62 cases，筛选/分页强断言
