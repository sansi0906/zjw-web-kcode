# 测试用例清单

- 用例总数：514
- 模块数：25
- 生成方式：`python scripts/export_test_cases.py`（pytest --collect-only 枚举 + AST 解析元数据，不执行用例）

## 模块统计

| 模块 | 用例数 |
|------|--------|
| 首页 | 83 |
| 重点项目 | 38 |
| 产业资讯 | 35 |
| 成果转化 | 28 |
| 云服务 | 25 |
| 供应大厅 | 40 |
| 可访问性 | 6 |
| 产业需求 | 31 |
| 异常与404 | 3 |
| 会展活动 | 11 |
| TestFinance | 15 |
| TestFinanceFonts | 10 |
| TestFinanceH5 | 13 |
| H5-列表页 | 21 |
| 首页-H5 | 50 |
| 首页-导航与搜索 | 5 |
| 产业化服务 | 13 |
| 产业协会 | 27 |
| 智能建造 | 31 |
| 登录 | 4 |
| 通用交互 | 5 |
| 注册 | 6 |
| 异常与韧性 | 2 |
| 供应大厅-搜索结果 | 10 |
| 视觉回归 | 2 |

## 用例明细

### 首页（83）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-001 | TestHomePage.test_logo_display | Logo显示 | 严重 |
| TC-002 | TestHomePage.test_logo_click | Logo点击返回首页 | 严重 |
| TC-003 | TestHomePage.test_nav_home | 首页链接跳转 | 严重 |
| TC-004 | TestHomePage.test_section_title_font_consistency | 首页区块标题字体一致性 | 轻微 |
| TC-005 | TestHomePage.test_service_card_title_font_consistency | 首页服务卡片标题字体一致性 | 轻微 |
| TC-006 | TestHomePage.test_button_font_consistency | 首页按钮字体一致性 | 轻微 |
| TC-007 | TestHomePage.test_body_desc_font_consistency | 首页描述文字字体一致性 | 轻微 |
| TC-008 | TestHomePage.test_footer_nav_font_consistency | 首页页脚导航链接字体一致性 | 轻微 |
| TC-009 | TestHomePage.test_footer_service_font_consistency | 页脚服务链接字体一致性 | 轻微 |
| TC-010 | TestHomePage.test_jzys_tab_font_consistency | 津筑云商Tab字体一致性 | 轻微 |
| TC-011 | TestHomePage.test_login_button | 登录按钮点击 | 严重 |
| TC-012 | TestHomePage.test_register_button | 注册按钮点击 | 严重 |
| TC-013 | TestHomePage.test_register_submit_guard | 注册页提交按钮默认受限（必填校验） | 一般 |
| TC-014 | TestHomePage.test_search_input | 搜索框输入 | 一般 |
| TC-015 | TestHomePage.test_search_button | 搜索按钮点击 | 一般 |
| TC-016 | TestHomePage.test_hot_search_display | 热搜词展示 | 一般 |
| TC-017 | TestHomePage.test_hot_search_click | 热搜词点击 | 轻微 |
| TC-018 | TestHomePage.test_carousel_loaded | 轮播图加载 | 严重 |
| TC-019 | TestHomePage.test_carousel_auto_play | 轮播图自动轮换 | 严重 |
| TC-020 | TestHomePage.test_carousel_image_loading | 轮播图图片加载 | 一般 |
| TC-021 | TestHomePage.test_carousel_dot_switch | 轮播图 dots 切换 | 一般 |
| TC-022 | TestHomePage.test_carousel_image_link_jump | 轮播图点击图片跳转配置链接 | 一般 |
| TC-023 | TestHomePage.test_service_stats_display | 统计数字展示 | 一般 |
| TC-024 | TestHomePage.test_industry_service_load | 产业服务区加载 | 严重 |
| TC-025 | TestHomePage.test_service_card_titles | 服务子分类卡片展示 | 严重 |
| TC-026 | TestHomePage.test_detail_button_click | 了解详情按钮点击 | 一般 |
| TC-027 | TestHomePage.test_tjdigital_load | 津筑云商区加载 | 严重 |
| TC-028 | TestHomePage.test_merchant_tabs_display | 生态标签展示 | 一般 |
| TC-029 | TestHomePage.test_merchant_images_load | 企业图片加载 | 一般 |
| TC-030 | TestHomePage.test_exhibition_load | 会展活动区加载 | 严重 |
| TC-031 | TestHomePage.test_activity_cards_display | 活动卡片展示 | 一般 |
| TC-032 | TestHomePage.test_activity_detail_click | 活动详情跳转 | 轻微 |
| TC-033 | TestHomePage.test_view_all_exhibition | 会展活动查看全部跳转 | 严重 |
| TC-034 | TestHomePage.test_demand_load | 产业需求区加载 | 严重 |
| TC-035 | TestHomePage.test_demand_items_display | 需求条目展示 | 一般 |
| TC-036 | TestHomePage.test_demand_item_detail | 需求条目详情信息 | 一般 |
| TC-037 | TestHomePage.test_view_all_demand | 查看全部跳转 | 严重 |
| TC-038 | TestHomePage.test_policy_load | 产业政策区加载 | 严重 |
| TC-039 | TestHomePage.test_policy_tabs_switch | 政策标签页切换 | 一般 |
| TC-040 | TestHomePage.test_news_items_display | 政策新闻条目展示 | 一般 |
| TC-041 | TestHomePage.test_view_all_policy | 政策查看全部跳转 | 严重 |
| TC-042 | TestHomePage.test_footer_phone | 服务电话显示 | 轻微 |
| TC-043 | TestHomePage.test_footer_icp | ICP备案号 | 轻微 |
| TC-044 | TestHomePage.test_footer_copyright | 版权信息 | 轻微 |
| TC-045 | TestHomePage.test_footer_nav_links | 页脚导航链接 | 轻微 |
| TC-046 | TestHomePage.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-047 | TestHomePage.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-048 | TestHomePage.test_merchant_tab_hover | 生态标签hover效果 | 轻微 |
| TC-049 | TestHomePage.test_float_button_hover | 悬浮按钮hover效果 | 轻微 |
| TC-050 | TestHomePage.test_page_scroll_performance | 页面滚动流畅性 | 轻微 |
| TC-051 | TestHomePage.test_carousel_images_load | 轮播图图片加载 | 一般 |
| TC-052 | TestHomePage.test_merchant_images_alt | 企业图片alt文本检查 | 轻微 |
| TC-053 | TestHomePage.test_page_refresh | F5刷新测试 | 严重 |
| TC-054 | TestHomePage.test_page_load_performance | 页面加载性能 | 一般 |
| TC-055 | TestHomePage.test_no_console_errors | 检查JS控制台错误 | 一般 |
| TC-056 | TestHomePage.test_policy_nav_route | 产业政策导航路由检查 | 一般 |
| TC-057 | TestHomePage.test_images_alt_text | 图片alt文本检查 | 轻微 |
| TC-058 | TestHomePage.test_footer_icp_is_link | 页脚ICP链接检查 | 轻微 |
| TC-059 | TestHomePage.test_no_placeholder_content | 检查测试占位符内容 | 一般 |
| TC-060 | TestHomePage.test_nav_link_font_consistency | 首页顶部导航链接字体一致性 | 轻微 |
| TC-061 | TestHomePage.test_float_button_font_consistency | 首页悬浮按钮字体一致性 | 轻微 |
| TC-282 | TestHomePageFonts.test_section_title_font_consistency | 首页区块标题字体一致性 | 轻微 |
| TC-283 | TestHomePageFonts.test_service_card_title_font_consistency | 首页服务卡片标题字体一致性 | 轻微 |
| TC-284 | TestHomePageFonts.test_button_font_consistency | 首页按钮字体一致性 | 轻微 |
| TC-285 | TestHomePageFonts.test_body_desc_font_consistency | 首页描述文字字体一致性 | 轻微 |
| TC-286 | TestHomePageFonts.test_footer_nav_font_consistency | 首页页脚导航链接字体一致性 | 轻微 |
| TC-287 | TestHomePageFonts.test_hot_search_font_consistency | 热搜词字体一致性 | 轻微 |
| TC-288 | TestHomePageFonts.test_news_title_font_consistency | 新闻标题字体一致性 | 轻微 |
| TC-289 | TestHomePageFonts.test_supply_item_font_consistency | 供应品目字体一致性 | 轻微 |
| TC-290 | TestHomePageFonts.test_footer_service_font_consistency | 页脚服务链接字体一致性 | 轻微 |
| TC-291 | TestHomePageFonts.test_jzys_tab_font_consistency | 津筑云商Tab字体一致性 | 轻微 |
| TC-292 | TestHomePageFonts.test_nav_link_font_consistency | 首页顶部导航链接字体一致性 | 轻微 |
| TC-293 | TestHomePageFonts.test_exhibition_info_font_consistency | 首页会展信息字体一致性 | 轻微 |
| TC-294 | TestHomePageFonts.test_demand_contact_font_consistency | 首页产业需求联系人字体一致性 | 轻微 |
| TC-295 | TestHomePageFonts.test_demand_count_font_consistency | 首页产业需求数量字体一致性 | 轻微 |
| TC-296 | TestHomePageFonts.test_news_date_font_consistency | 首页新闻日期字体一致性 | 轻微 |
| TC-297 | TestHomePageFonts.test_news_desc_font_consistency | 首页新闻描述字体一致性 | 轻微 |
| TC-298 | TestHomePageFonts.test_float_button_font_consistency | 首页悬浮按钮字体一致性 | 轻微 |
| TC-299 | TestHomePage.test_page_load | 页面正常加载 | 严重 |
| TC-300 | TestHomePage.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-301 | TestHomePage.test_nav_active_state | 链接高亮 | 一般 |
| TC-302 | TestHomePage.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-303 | TestHomePage.test_no_broken_images | 图片加载正常 | 一般 |

### 重点项目（38）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-062 | TestKeyProjects.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-063 | TestKeyProjects.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-064 | TestKeyProjects.test_images_alt_text | 图片alt文本检查 | 轻微 |
| TC-065 | TestKeyProjects.test_project_card_display | 项目卡片展示 | 严重 |
| TC-066 | TestKeyProjects.test_project_click | 项目点击跳转 | 严重 |
| TC-067 | TestKeyProjects.test_project_detail_info | 项目详情信息 | 严重 |
| TC-068 | TestKeyProjects.test_view_all_projects | 点击查看全部项目 | 一般 |
| TC-069 | TestKeyProjects.test_publish_project | 发布项目按钮 | 一般 |
| TC-070 | TestKeyProjects.test_publish_demand | 发布需求按钮 | 一般 |
| TC-071 | TestKeyProjects.test_filter_房建项目 | 房建项目筛选 | 严重 |
| TC-072 | TestKeyProjects.test_filter_市政项目 | 市政项目筛选 | 严重 |
| TC-073 | TestKeyProjects.test_filter_其他项目 | 其他项目筛选 | 严重 |
| TC-074 | TestKeyProjects.test_filter_then_pagination | 筛选后翻页列表变化 | 一般 |
| TC-075 | TestKeyProjects.test_pagination_jump | 分页跳转 | 一般 |
| TC-076 | TestKeyProjects.test_pagination_pages_display | 分页页码展示 | 一般 |
| TC-077 | TestKeyProjects.test_pagination_switches_content | 翻页后列表内容变化 | 严重 |
| TC-078 | TestKeyProjects.test_pagination_back_to_first | 返回第一页 | 一般 |
| TC-451 | TestKeyProjectFonts.test_page_load | 页面正常加载 | 严重 |
| TC-452 | TestKeyProjectFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-453 | TestKeyProjectFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-454 | TestKeyProjectFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-455 | TestKeyProjectFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-456 | TestKeyProjectFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-457 | TestKeyProjectFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-458 | TestKeyProjectFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-459 | TestKeyProjectFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-460 | TestKeyProjectFonts.test_kp_project_title_font_consistency | 重点项目标题字体一致性 | 轻微 |
| TC-461 | TestKeyProjectFonts.test_kp_filter_tab_font_consistency | 重点项目筛选Tab字体一致性 | 轻微 |
| TC-462 | TestKeyProjectFonts.test_kp_desc_font_consistency | 重点项目描述字体一致性 | 轻微 |
| TC-463 | TestKeyProjects.test_page_load | 页面正常加载 | 严重 |
| TC-464 | TestKeyProjects.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-465 | TestKeyProjects.test_nav_active_state | 链接高亮 | 一般 |
| TC-466 | TestKeyProjects.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-467 | TestKeyProjects.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-468 | TestKeyProjects.test_footer_phone | 服务电话链接 | 轻微 |
| TC-469 | TestKeyProjects.test_footer_icp | 备案号链接 | 轻微 |
| TC-470 | TestKeyProjects.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-471 | TestKeyProjects.test_no_broken_images | 图片加载正常 | 一般 |

### 产业资讯（35）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-079 | TestIndustryNews.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-080 | TestIndustryNews.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-081 | TestIndustryNews.test_images_alt_text | 图片alt文本检查 | 轻微 |
| TC-082 | TestIndustryNews.test_news_card_display | 新闻卡片展示 | 严重 |
| TC-083 | TestIndustryNews.test_news_images_load | 新闻图片加载 | 一般 |
| TC-084 | TestIndustryNews.test_news_click | 新闻点击跳转 | 严重 |
| TC-085 | TestIndustryNews.test_news_detail_content | 新闻详情内容 | 严重 |
| TC-086 | TestIndustryNews.test_tab_detail_title_consistent | 分类切换后详情标题一致 | 一般 |
| TC-087 | TestIndustryNews.test_tab_行业动态 | 行业动态Tab切换 | 严重 |
| TC-088 | TestIndustryNews.test_tab_政策资讯 | 政策资讯Tab切换 | 严重 |
| TC-089 | TestIndustryNews.test_tab_政策解读 | 政策解读Tab切换 | 严重 |
| TC-090 | TestIndustryNews.test_pagination_jump | 分页跳转 | 一般 |
| TC-091 | TestIndustryNews.test_pagination_pages_display | 分页页码展示 | 一般 |
| TC-092 | TestIndustryNews.test_pagination_switches_content | 翻页后列表内容变化 | 严重 |
| TC-399 | TestIndustryNews.test_page_load | 页面正常加载 | 严重 |
| TC-400 | TestIndustryNews.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-401 | TestIndustryNews.test_nav_active_state | 链接高亮 | 一般 |
| TC-402 | TestIndustryNews.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-403 | TestIndustryNews.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-404 | TestIndustryNews.test_footer_phone | 服务电话链接 | 轻微 |
| TC-405 | TestIndustryNews.test_footer_icp | 备案号链接 | 轻微 |
| TC-406 | TestIndustryNews.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-407 | TestIndustryNews.test_no_broken_images | 图片加载正常 | 一般 |
| TC-408 | TestIndustryNewsFonts.test_page_load | 页面正常加载 | 严重 |
| TC-409 | TestIndustryNewsFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-410 | TestIndustryNewsFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-411 | TestIndustryNewsFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-412 | TestIndustryNewsFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-413 | TestIndustryNewsFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-414 | TestIndustryNewsFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-415 | TestIndustryNewsFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-416 | TestIndustryNewsFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-417 | TestIndustryNewsFonts.test_news_title_font_consistency | 产业新闻卡片标题字体一致性 | 轻微 |
| TC-418 | TestIndustryNewsFonts.test_news_desc_font_consistency | 产业新闻描述字体一致性 | 轻微 |
| TC-419 | TestIndustryNewsFonts.test_news_time_font_consistency | 产业新闻发布时间字体一致性 | 轻微 |

### 成果转化（28）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-093 | TestAchievementTransformation.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-094 | TestAchievementTransformation.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-095 | TestAchievementTransformation.test_filter_课题 | 科技创新成果筛选 | 严重 |
| TC-096 | TestAchievementTransformation.test_filter_成果 | 成果筛选 | 严重 |
| TC-097 | TestAchievementTransformation.test_achievement_cards_display | 成果卡片展示 | 严重 |
| TC-098 | TestAchievementTransformation.test_achievement_click | 成果卡片点击跳转 | 严重 |
| TC-136 | TestAchievementTransformation.test_page_load | 页面正常加载 | 严重 |
| TC-137 | TestAchievementTransformation.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-138 | TestAchievementTransformation.test_nav_active_state | 链接高亮 | 一般 |
| TC-139 | TestAchievementTransformation.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-140 | TestAchievementTransformation.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-141 | TestAchievementTransformation.test_footer_phone | 服务电话链接 | 轻微 |
| TC-142 | TestAchievementTransformation.test_footer_icp | 备案号链接 | 轻微 |
| TC-143 | TestAchievementTransformation.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-144 | TestAchievementTransformation.test_no_broken_images | 图片加载正常 | 一般 |
| TC-145 | TestAchievementTransformationFonts.test_page_load | 页面正常加载 | 严重 |
| TC-146 | TestAchievementTransformationFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-147 | TestAchievementTransformationFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-148 | TestAchievementTransformationFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-149 | TestAchievementTransformationFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-150 | TestAchievementTransformationFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-151 | TestAchievementTransformationFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-152 | TestAchievementTransformationFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-153 | TestAchievementTransformationFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-154 | TestAchievementTransformationFonts.test_at_project_title_font_consistency | 成果转化项目标题字体一致性 | 轻微 |
| TC-155 | TestAchievementTransformationFonts.test_at_institution_name_font_consistency | 成果转化机构名称字体一致性 | 轻微 |
| TC-156 | TestAchievementTransformationFonts.test_at_company_font_consistency | 成果转化研发单位字体一致性 | 轻微 |
| TC-157 | TestAchievementTransformationFonts.test_at_tech_tag_font_consistency | 成果转化技术方向标签字体一致性 | 轻微 |

### 云服务（25）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-099 | TestCloudService.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-100 | TestCloudService.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-101 | TestCloudService.test_service_cards_display | 全部服务筛选 | 严重 |
| TC-102 | TestCloudService.test_service_click | 服务卡片点击跳转 | 严重 |
| TC-103 | TestCloudService.test_view_all_button | 查看全部服务按钮 | 一般 |
| TC-158 | TestCloudService.test_page_load | 页面正常加载 | 严重 |
| TC-159 | TestCloudService.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-160 | TestCloudService.test_nav_active_state | 链接高亮 | 一般 |
| TC-161 | TestCloudService.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-162 | TestCloudService.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-163 | TestCloudService.test_footer_phone | 服务电话链接 | 轻微 |
| TC-164 | TestCloudService.test_footer_icp | 备案号链接 | 轻微 |
| TC-165 | TestCloudService.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-166 | TestCloudService.test_no_broken_images | 图片加载正常 | 一般 |
| TC-167 | TestCloudServiceFonts.test_page_load | 页面正常加载 | 严重 |
| TC-168 | TestCloudServiceFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-169 | TestCloudServiceFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-170 | TestCloudServiceFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-171 | TestCloudServiceFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-172 | TestCloudServiceFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-173 | TestCloudServiceFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-174 | TestCloudServiceFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-175 | TestCloudServiceFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-176 | TestCloudServiceFonts.test_cs_service_name_font_consistency | 云服务名称字体一致性 | 轻微 |
| TC-177 | TestCloudServiceFonts.test_cs_service_desc_font_consistency | 云服务服务描述字体一致性 | 轻微 |

### 供应大厅（40）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-104 | TestSupplyHall.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-105 | TestSupplyHall.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-106 | TestSupplyHall.test_images_alt_text | 图片alt文本检查 | 轻微 |
| TC-107 | TestSupplyHall.test_supply_hall_page_load | 供应大厅页面正常加载 | 严重 |
| TC-108 | TestSupplyHall.test_supply_items_display | 供应商品卡片展示 | 严重 |
| TC-109 | TestSupplyHall.test_supply_item_images_load | 商品图片加载 | 一般 |
| TC-110 | TestSupplyHall.test_supply_item_price_display | 价格信息展示 | 一般 |
| TC-111 | TestSupplyHall.test_supply_item_click | 供应商品点击跳转 | 严重 |
| TC-112 | TestSupplyHall.test_supply_item_detail_consistency | 商品详情与列表一致性 | 严重 |
| TC-113 | TestSupplyHall.test_publish_button | 发布商品按钮 | 一般 |
| TC-114 | TestSupplyHall.test_inquiry_button | 求购询价按钮 | 一般 |
| TC-115 | TestSupplyHall.test_customer_service_button | 联系客服按钮 | 一般 |
| TC-116 | TestSupplyHall.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-117 | TestSupplyHall.test_pagination | 分页功能 | 轻微 |
| TC-118 | TestSupplyHall.test_nav_to_intelligent_construction | 导航到智能建造页面 | 一般 |
| TC-119 | TestSupplyHall.test_nav_to_key_project | 导航到重点项目页面 | 一般 |
| TC-120 | TestSupplyHall.test_filter_建筑材料 | 建筑材料分类筛选 | 严重 |
| TC-121 | TestSupplyHall.test_filter_水电暖通 | 水电暖通分类筛选 | 严重 |
| TC-122 | TestSupplyHall.test_filter_机械设备 | 机械设备分类筛选 | 严重 |
| TC-123 | TestSupplyHall.test_filter_工程机械 | 工程机械分类筛选 | 严重 |
| TC-124 | TestSupplyHall.test_filter_劳务用工 | 劳务用工分类筛选 | 严重 |
| TC-125 | TestSupplyHall.test_filter_sub_土建 | 土建子分类筛选 | 一般 |
| TC-126 | TestSupplyHall.test_filter_sub_装饰装修 | 装饰装修子分类筛选 | 一般 |
| TC-127 | TestSupplyHall.test_filter_sub_电气 | 电气子分类筛选 | 一般 |
| TC-128 | TestSupplyHall.test_search | 搜索商品 | 一般 |
| TC-129 | TestSupplyHall.test_reset | 重置搜索 | 一般 |
| TC-489 | TestSupplyHall.test_page_load | 页面正常加载 | 严重 |
| TC-490 | TestSupplyHall.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-491 | TestSupplyHall.test_nav_active_state | 链接高亮 | 一般 |
| TC-492 | TestSupplyHall.test_footer_phone | 服务电话链接 | 轻微 |
| TC-493 | TestSupplyHall.test_footer_icp | 备案号链接 | 轻微 |
| TC-494 | TestSupplyHall.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-495 | TestSupplyHall.test_no_broken_images | 图片加载正常 | 一般 |
| TC-496 | TestSupplyHallFonts.test_supply_hall_category_title_font_consistency | 供应大厅分类标题字体一致性 | 轻微 |
| TC-497 | TestSupplyHallFonts.test_supply_hall_subcategory_title_font_consistency | 供应大厅子分类标题字体一致性 | 轻微 |
| TC-498 | TestSupplyHallFonts.test_supply_hall_view_all_font_consistency | 供应大厅查看全部按钮字体一致性 | 轻微 |
| TC-499 | TestSupplyHallFonts.test_supply_hall_stats_number_font_consistency | 供应大厅统计数字字体一致性 | 轻微 |
| TC-500 | TestSupplyHallFonts.test_supply_hall_stats_label_font_consistency | 供应大厅统计标签字体一致性 | 轻微 |
| TC-501 | TestSupplyHallFonts.test_supply_hall_category_desc_font_consistency | 供应大厅分类描述字体一致性 | 轻微 |
| TC-502 | TestSupplyHallFonts.test_supply_hall_service_tag_font_consistency | 供应大厅服务标签字体一致性 | 轻微 |

### 可访问性（6）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-130 | TestA11yBasic.test_home_lang_and_headings | Web 首页语言与标题结构 | 轻微 |
| TC-131 | TestA11yBasic.test_home_buttons_accessible_name | Web 首页按钮具备可访问名称 | 轻微 |
| TC-132 | TestA11yBasic.test_home_inputs_labelled | Web 首页输入框具备标签/占位 | 轻微 |
| TC-133 | TestA11yBasic.test_home_images_alt | Web 首页图片 alt（复用 ui_quality 配置） | 轻微 |
| TC-134 | TestA11yBasic.test_h5_viewport_and_buttons | H5 首页 viewport 与按钮名称 | 轻微 |
| TC-135 | TestA11yBasic.test_supply_hall_search_labelled | 供应大厅搜索框具备标签 | 轻微 |

### 产业需求（31）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-178 | TestDemandPage.test_page_load | 页面正常加载 | 严重 |
| TC-179 | TestDemandPage.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-180 | TestDemandPage.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-181 | TestDemandPage.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-182 | TestDemandPage.test_footer_phone | 服务电话链接 | 轻微 |
| TC-183 | TestDemandPage.test_footer_icp | 备案号链接 | 轻微 |
| TC-184 | TestDemandPage.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-185 | TestDemandPage.test_no_broken_images | 图片加载正常 | 一般 |
| TC-186 | TestDemandPage.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-187 | TestDemandPage.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-188 | TestDemandPage.test_filter_建筑建材 | 建筑建材分类筛选 | 严重 |
| TC-189 | TestDemandPage.test_filter_机械设备 | 机械设备分类筛选 | 严重 |
| TC-190 | TestDemandPage.test_filter_劳务用工 | 劳务用工分类筛选 | 严重 |
| TC-191 | TestDemandPage.test_filter_技术服务 | 技术服务分类筛选 | 严重 |
| TC-192 | TestDemandPage.test_search | 搜索功能 | 一般 |
| TC-193 | TestDemandPage.test_reset | 重置功能 | 一般 |
| TC-194 | TestDemandPage.test_search_no_result_hint | 无结果空态提示 | 一般 |
| TC-195 | TestDemandPage.test_demand_detail_consistency | 需求详情与列表一致 | 严重 |
| TC-196 | TestDemandPage.test_stats_display | 统计数据展示 | 一般 |
| TC-197 | TestDemandPage.test_pagination_jump | 分页跳转 | 一般 |
| TC-198 | TestDemandPageFonts.test_page_load | 页面正常加载 | 严重 |
| TC-199 | TestDemandPageFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-200 | TestDemandPageFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-201 | TestDemandPageFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-202 | TestDemandPageFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-203 | TestDemandPageFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-204 | TestDemandPageFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-205 | TestDemandPageFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-206 | TestDemandPageFonts.test_demand_desc_font_consistency | 产业需求描述字体一致性 | 轻微 |
| TC-207 | TestDemandPageFonts.test_demand_amount_font_consistency | 产业需求金额字体一致性 | 轻微 |
| TC-208 | TestDemandPageFonts.test_demand_big_amount_font_consistency | 产业需求大号金额字体一致性 | 轻微 |

### 异常与404（3）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-209 | TestErrorPages.test_web_not_found_page | Web 未匹配路由显示 404 并可返回首页 | 一般 |
| TC-210 | TestErrorPages.test_not_found_detection | 页面对象可识别 404 路由 | 一般 |
| TC-211 | TestErrorPages.test_h5_not_found_page | H5 未匹配路由显示 404 | 一般 |

### 会展活动（11）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-212 | TestExhibition.test_page_load | 页面正常加载 | 严重 |
| TC-213 | TestExhibition.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-214 | TestExhibition.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-215 | TestExhibition.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-216 | TestExhibition.test_footer_phone | 服务电话链接 | 轻微 |
| TC-217 | TestExhibition.test_footer_icp | 备案号链接 | 轻微 |
| TC-218 | TestExhibition.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-219 | TestExhibition.test_no_broken_images | 图片加载正常 | 一般 |
| TC-220 | TestExhibition.test_exhibition_list_load | 会展活动列表加载 | 严重 |
| TC-221 | TestExhibition.test_exhibition_detail_consistency | 活动详情跳转与标题一致 | 严重 |
| TC-222 | TestExhibition.test_exhibition_detail_no_overflow | 详情页无横向溢出 | 轻微 |

### TestFinance（15）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-223 | TestFinance.test_page_load | 页面正常加载 | 严重 |
| TC-224 | TestFinance.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-225 | TestFinance.test_nav_active_state | 链接高亮 | 一般 |
| TC-226 | TestFinance.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-227 | TestFinance.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-228 | TestFinance.test_footer_phone | 服务电话链接 | 轻微 |
| TC-229 | TestFinance.test_footer_icp | 备案号链接 | 轻微 |
| TC-230 | TestFinance.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-231 | TestFinance.test_no_broken_images | 图片加载正常 | 一般 |
| TC-232 | TestFinance.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-233 | TestFinance.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-234 | TestFinance.test_finance_cards_display | 金融卡片展示 | 严重 |
| TC-235 | TestFinance.test_finance_card_click | 金融卡片点击跳转 | 严重 |
| TC-236 | TestFinance.test_hero_apply_button | 申请融资按钮 | 一般 |
| TC-237 | TestFinance.test_top_buttons | 顶部功能按钮 | 一般 |

### TestFinanceFonts（10）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-238 | TestFinanceFonts.test_page_load | 页面正常加载 | 严重 |
| TC-239 | TestFinanceFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-240 | TestFinanceFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-241 | TestFinanceFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-242 | TestFinanceFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-243 | TestFinanceFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-244 | TestFinanceFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-245 | TestFinanceFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-246 | TestFinanceFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-247 | TestFinanceFonts.test_finance_title_font_consistency | 产业金融卡片标题字体一致性 | 轻微 |

### TestFinanceH5（13）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-248 | TestFinanceH5.test_page_load | 页面正常加载 | 严重 |
| TC-249 | TestFinanceH5.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-250 | TestFinanceH5.test_nav_active_state | 链接高亮 | 一般 |
| TC-251 | TestFinanceH5.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-252 | TestFinanceH5.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-253 | TestFinanceH5.test_footer_phone | 服务电话链接 | 轻微 |
| TC-254 | TestFinanceH5.test_footer_icp | 备案号链接 | 轻微 |
| TC-255 | TestFinanceH5.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-256 | TestFinanceH5.test_no_broken_images | 图片加载正常 | 一般 |
| TC-257 | TestFinanceH5.test_h5_finance_cards_display | H5 金融卡片展示 | 严重 |
| TC-258 | TestFinanceH5.test_h5_finance_card_click | H5 金融卡片点击跳转 | 严重 |
| TC-259 | TestFinanceH5.test_h5_hero_apply_button | H5 申请融资按钮 | 一般 |
| TC-260 | TestFinanceH5.test_h5_top_buttons | H5 顶部功能按钮 | 一般 |

### H5-列表页（21）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-261 | TestH5SupplyHall.test_h5_supply_hall_load | H5-供应大厅页面加载与核心内容可见 | 严重 |
| TC-262 | TestH5SupplyHall.test_h5_supply_hall_filter | H5-供应大厅一级分类可切换 | 一般 |
| TC-263 | TestH5SupplyHall.test_h5_supply_hall_subcategory_navigates | H5-供应大厅子类筛选触发结果刷新 | 一般 |
| TC-264 | TestH5SupplyHall.test_h5_supply_hall_open_detail | H5-供应大厅商品可进入详情页 | 严重 |
| TC-265 | TestH5KeyProject.test_h5_key_project_load | H5-重点项目页面加载与列表可见 | 严重 |
| TC-266 | TestH5KeyProject.test_h5_key_project_controls | H5-重点项目分类/分页控件可见 | 一般 |
| TC-267 | TestH5KeyProject.test_h5_key_project_filter_changes_list | H5-重点项目筛选切换影响列表内容 | 严重 |
| TC-268 | TestH5KeyProject.test_h5_key_project_pagination | H5-重点项目分页切换内容并可返回 | 严重 |
| TC-269 | TestH5IndustryNews.test_h5_industry_news_load | H5-产业新闻页面加载与核心内容可见 | 严重 |
| TC-270 | TestH5IndustryNews.test_h5_industry_news_controls | H5-产业新闻Tab/分页可见 | 一般 |
| TC-271 | TestH5IndustryNews.test_h5_industry_news_tab_switch | H5-产业新闻Tab切换可响应 | 一般 |
| TC-272 | TestH5IndustryNews.test_h5_industry_news_pagination | H5-产业新闻分页切换内容 | 严重 |
| TC-273 | TestH5DemandPage.test_h5_demand_page_load | H5-产业需求页面加载与核心内容可见 | 严重 |
| TC-274 | TestH5DemandPage.test_h5_demand_page_controls | H5-产业需求筛选与搜索控件可见 | 一般 |
| TC-275 | TestH5DemandPage.test_h5_demand_page_filter_switch | H5-产业需求筛选切换可响应 | 一般 |
| TC-276 | TestH5DemandPage.test_h5_demand_page_pagination | H5-产业需求分页切换可响应 | 一般 |
| TC-277 | TestH5AchievementTransformation.test_h5_achievement_load | H5-成果转化页面加载与核心内容可见 | 严重 |
| TC-278 | TestH5IndustryAssociation.test_h5_industry_association_load | H5-产业协会页面加载与核心内容可见 | 严重 |
| TC-279 | TestH5CloudService.test_h5_cloud_service_load | H5-云服务页面加载与核心内容可见 | 严重 |
| TC-280 | TestH5IntelligentConstruction.test_h5_intelligent_construction_load | H5-智能建造页面加载与核心内容可见 | 严重 |
| TC-281 | TestH5IndustrialService.test_h5_industrial_service_route | H5-产业化服务路由按当前环境可用性处理 | 一般 |

### 首页-H5（50）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-304 | TestHomePageH5Fonts.test_h5_section_title_font_consistency | H5 区块标题字体一致性 | 轻微 |
| TC-305 | TestHomePageH5Fonts.test_h5_service_card_title_font_consistency | H5 服务卡片标题字体一致性 | 轻微 |
| TC-306 | TestHomePageH5Fonts.test_h5_body_desc_font_consistency | H5 描述文字字体一致性 | 轻微 |
| TC-307 | TestHomePageH5Fonts.test_h5_footer_nav_font_consistency | H5 页脚导航链接字体一致性 | 轻微 |
| TC-308 | TestHomePageH5Fonts.test_h5_hot_search_font_consistency | H5 热搜词字体一致性 | 轻微 |
| TC-309 | TestHomePageH5Fonts.test_h5_news_title_font_consistency | H5 新闻标题字体一致性 | 轻微 |
| TC-310 | TestHomePageH5Fonts.test_h5_supply_item_font_consistency | H5 供应品目字体一致性 | 轻微 |
| TC-311 | TestHomePageH5Fonts.test_h5_footer_service_font_consistency | H5 页脚服务链接字体一致性 | 轻微 |
| TC-312 | TestHomePageH5Fonts.test_h5_nav_link_font_consistency | H5 顶部导航链接字体一致性 | 轻微 |
| TC-313 | TestHomePageH5Fonts.test_h5_exhibition_info_font_consistency | H5 会展信息字体一致性 | 轻微 |
| TC-314 | TestHomePageH5Fonts.test_h5_demand_contact_font_consistency | H5 产业需求联系人字体一致性 | 轻微 |
| TC-315 | TestHomePageH5Fonts.test_h5_demand_count_font_consistency | H5 产业需求数量字体一致性 | 轻微 |
| TC-316 | TestHomePageH5Fonts.test_h5_news_date_font_consistency | H5 新闻日期字体一致性 | 轻微 |
| TC-317 | TestHomePageH5Fonts.test_h5_news_desc_font_consistency | H5 新闻描述字体一致性 | 轻微 |
| TC-318 | TestHomePageH5Fonts.test_h5_float_button_font_consistency | H5 悬浮按钮字体一致性 | 轻微 |
| TC-319 | TestHomePageH5Smoke.test_h5_home_loads_without_overflow | H5-首页正常加载且无横向溢出 | 严重 |
| TC-320 | TestHomePageH5Smoke.test_h5_core_sections_visible | H5-首页核心模块可见 | 严重 |
| TC-321 | TestHomePageH5Smoke.test_h5_quick_entry_to_supply_hall | H5-分类入口可达供应大厅 | 严重 |
| TC-322 | TestHomePageH5Smoke.test_h5_home_search | H5-首页搜索可跳转搜索结果页 | 严重 |
| TC-323 | TestHomePageH5Smoke.test_h5_login_register_and_float_visible | H5-登录注册与悬浮入口可见 | 一般 |
| TC-324 | TestHomePageH5Smoke.test_h5_no_console_errors | H5-首页控制台无未知错误 | 一般 |
| TC-325 | TestHomePageH5Smoke.test_h5_no_placeholder_content | H5-首页无未知测试占位符内容 | 一般 |
| TC-326 | TestHomePageH5Smoke.test_h5_swipe_left_carousel | H5-首页向左滑动轮播图 | 轻微 |
| TC-327 | TestHomePageH5Smoke.test_h5_swipe_up_page | H5-首页向上滑动浏览 | 轻微 |
| TC-328 | TestHomePageH5Smoke.test_h5_pull_to_refresh | H5-首页下拉刷新 | 轻微 |
| TC-329 | TestHomePageH5Smoke.test_h5_view_all_exhibition | H5-首页查看全部-会展活动跳转 | 严重 |
| TC-330 | TestHomePageH5Smoke.test_h5_view_all_demand | H5-首页查看全部-产业需求跳转 | 严重 |
| TC-331 | TestHomePageH5Smoke.test_h5_view_all_policy | H5-首页查看全部-产业政策跳转 | 严重 |
| TC-332 | TestHomePageH5Smoke.test_h5_login_entry | H5-首页登录入口可触发登录交互 | 严重 |
| TC-333 | TestHomePageH5Smoke.test_h5_register_entry | H5-首页注册入口可跳转注册页 | 严重 |
| TC-334 | TestHomePageH5Smoke.test_h5_carousel_visible | H5-首页轮播图与圆点可见 | 一般 |
| TC-335 | TestHomePageH5Smoke.test_h5_carousel_dot_clickable | H5-首页轮播指示器可点击切换 | 轻微 |
| TC-336 | TestHomePageH5Smoke.test_h5_footer_info_visible | H5-首页页脚与备案信息可见 | 一般 |
| TC-337 | TestHomePageH5Smoke.test_h5_menu_open_next_to_register | H5-注册旁菜单可呼出并显示导航项 | 严重 |
| TC-338 | TestHomePageH5Smoke.test_h5_menu_nav_supply_hall | H5-菜单跳转-供应大厅 | 严重 |
| TC-339 | TestHomePageH5Smoke.test_h5_menu_nav_intelligent_construction | H5-菜单跳转-智能建造 | 严重 |
| TC-340 | TestHomePageH5Smoke.test_h5_menu_nav_key_project | H5-菜单跳转-重点项目 | 严重 |
| TC-341 | TestHomePageH5Smoke.test_h5_menu_nav_policy | H5-菜单跳转-产业政策 | 严重 |
| TC-342 | TestHomePageH5Smoke.test_h5_menu_nav_industry_association | H5-菜单跳转-产业协会 | 严重 |
| TC-343 | TestHomePageH5Smoke.test_h5_menu_nav_achievement | H5-菜单跳转-成果转化 | 严重 |
| TC-344 | TestHomePageH5Smoke.test_h5_menu_nav_cloud_service | H5-菜单跳转-云服务 | 严重 |
| TC-345 | TestHomePageH5Smoke.test_h5_menu_close_and_reopen | H5-注册旁菜单可关闭并再次呼出 | 一般 |
| TC-346 | TestHomePageH5Smoke.test_h5_login_form_visible | H5-登录弹窗展示账号与验证码输入 | 一般 |
| TC-347 | TestHomePageH5Smoke.test_h5_register_submit_guard | H5-注册页提交按钮默认禁用（必填校验） | 一般 |
| TC-348 | TestHomePageH5Smoke.test_h5_register_invalid_phone | H5-注册页非法手机号提示 | 一般 |
| TC-349 | TestHomePageH5Smoke.test_h5_menu_available_on_secondary_page | H5-二级页面可用注册旁菜单并打开导航 | 一般 |
| TC-350 | TestHomePageH5Smoke.test_h5_menu_mask_close | H5-点击遮罩关闭菜单 | 一般 |
| TC-351 | TestHomePageH5Smoke.test_h5_menu_escape_close | H5-Esc 关闭菜单 | 轻微 |
| TC-352 | TestHomePageH5Smoke.test_h5_menu_active_highlight_on_secondary_page | H5-二级页面菜单当前项高亮 | 一般 |
| TC-353 | TestHomePageH5Smoke.test_h5_menu_nav_from_secondary_page | H5-二级页面菜单可跳转 | 一般 |

### 首页-导航与搜索（5）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-354 | TestHomePageNavSearch.test_nav_links_complete | 导航链接完整性 | 严重 |
| TC-355 | TestHomePageNavSearch.test_nav_jump | test_nav_jump | 严重 |
| TC-356 | TestHomePageNavSearch.test_search_navigates_to_result_page | 搜索跳转到搜索结果页 | 严重 |
| TC-357 | TestHomePageNavSearch.test_search_result_matches_keyword | 搜索结果与关键词相关 | 严重 |
| TC-358 | TestHomePageNavSearch.test_search_empty_state_hint | 无结果关键词展示空状态提示 | 一般 |

### 产业化服务（13）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-359 | TestIndustrialService.test_page_load | 页面正常加载 | 严重 |
| TC-360 | TestIndustrialService.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-361 | TestIndustrialService.test_nav_active_state | 链接高亮 | 一般 |
| TC-362 | TestIndustrialService.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-363 | TestIndustrialService.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-364 | TestIndustrialService.test_footer_phone | 服务电话链接 | 轻微 |
| TC-365 | TestIndustrialService.test_footer_icp | 备案号链接 | 轻微 |
| TC-366 | TestIndustrialService.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-367 | TestIndustrialService.test_no_broken_images | 图片加载正常 | 一般 |
| TC-368 | TestIndustrialService.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-369 | TestIndustrialService.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-370 | TestIndustrialService.test_industrial_service_module_exists | 产业化服务模块存在 | 严重 |
| TC-371 | TestIndustrialService.test_service_items_display | 服务项展示 | 一般 |

### 产业协会（27）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-372 | TestIndustryAssociation.test_page_load | 页面正常加载 | 严重 |
| TC-373 | TestIndustryAssociation.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-374 | TestIndustryAssociation.test_nav_active_state | 链接高亮 | 一般 |
| TC-375 | TestIndustryAssociation.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-376 | TestIndustryAssociation.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-377 | TestIndustryAssociation.test_footer_phone | 服务电话链接 | 轻微 |
| TC-378 | TestIndustryAssociation.test_footer_icp | 备案号链接 | 轻微 |
| TC-379 | TestIndustryAssociation.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-380 | TestIndustryAssociation.test_no_broken_images | 图片加载正常 | 一般 |
| TC-381 | TestIndustryAssociation.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-382 | TestIndustryAssociation.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-383 | TestIndustryAssociation.test_association_cards_display | 全部协会筛选 | 严重 |
| TC-384 | TestIndustryAssociation.test_association_click | 协会卡片点击跳转 | 严重 |
| TC-385 | TestIndustryAssociation.test_view_all_button | 查看全部协会按钮 | 一般 |
| TC-386 | TestIndustryAssociation.test_search | 协会入驻筛选 | 严重 |
| TC-387 | TestIndustryAssociation.test_pagination_jump | 分页跳转 | 一般 |
| TC-388 | TestIndustryAssociationFonts.test_page_load | 页面正常加载 | 严重 |
| TC-389 | TestIndustryAssociationFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-390 | TestIndustryAssociationFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-391 | TestIndustryAssociationFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-392 | TestIndustryAssociationFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-393 | TestIndustryAssociationFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-394 | TestIndustryAssociationFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-395 | TestIndustryAssociationFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-396 | TestIndustryAssociationFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-397 | TestIndustryAssociationFonts.test_ia_association_name_font_consistency | 产业协会名称字体一致性 | 轻微 |
| TC-398 | TestIndustryAssociationFonts.test_ia_demo_news_title_font_consistency | 产业协会示范企业标题字体一致性 | 轻微 |

### 智能建造（31）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-420 | TestIntelligentConstruction.test_page_load | 页面正常加载 | 严重 |
| TC-421 | TestIntelligentConstruction.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-422 | TestIntelligentConstruction.test_nav_active_state | 链接高亮 | 一般 |
| TC-423 | TestIntelligentConstruction.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-424 | TestIntelligentConstruction.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-425 | TestIntelligentConstruction.test_footer_phone | 服务电话链接 | 轻微 |
| TC-426 | TestIntelligentConstruction.test_footer_icp | 备案号链接 | 轻微 |
| TC-427 | TestIntelligentConstruction.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-428 | TestIntelligentConstruction.test_no_broken_images | 图片加载正常 | 一般 |
| TC-429 | TestIntelligentConstruction.test_no_console_errors | 控制台无未知错误 | 一般 |
| TC-430 | TestIntelligentConstruction.test_no_placeholder_content | 无未知测试占位符内容 | 一般 |
| TC-431 | TestIntelligentConstruction.test_construction_cards_display | 全部建造筛选 | 严重 |
| TC-432 | TestIntelligentConstruction.test_construction_click | 建造卡片点击跳转 | 严重 |
| TC-433 | TestIntelligentConstruction.test_view_all_button | 查看全部建造按钮 | 一般 |
| TC-434 | TestIntelligentConstruction.test_pagination_jump | 分页跳转 | 一般 |
| TC-435 | TestIntelligentConstruction.test_declaration_new_tech | 智能建造新技术新产品申报 | 一般 |
| TC-436 | TestIntelligentConstruction.test_declaration_seed_enterprise | 智能建造种子企业申报 | 一般 |
| TC-437 | TestIntelligentConstruction.test_view_standard_京津冀 | 查看京津冀标准 | 一般 |
| TC-438 | TestIntelligentConstruction.test_view_bim_product | 查看BIM产品 | 一般 |
| TC-439 | TestIntelligentConstructionFonts.test_page_load | 页面正常加载 | 严重 |
| TC-440 | TestIntelligentConstructionFonts.test_nav_completeness | 导航栏完整性 | 严重 |
| TC-441 | TestIntelligentConstructionFonts.test_nav_active_state | 链接高亮 | 一般 |
| TC-442 | TestIntelligentConstructionFonts.test_customer_service_button | 在线客服按钮 | 一般 |
| TC-443 | TestIntelligentConstructionFonts.test_intent_form_button | 意向填报按钮 | 一般 |
| TC-444 | TestIntelligentConstructionFonts.test_footer_phone | 服务电话链接 | 轻微 |
| TC-445 | TestIntelligentConstructionFonts.test_footer_icp | 备案号链接 | 轻微 |
| TC-446 | TestIntelligentConstructionFonts.test_no_horizontal_overflow | 无横向溢出 | 一般 |
| TC-447 | TestIntelligentConstructionFonts.test_no_broken_images | 图片加载正常 | 一般 |
| TC-448 | TestIntelligentConstructionFonts.test_ic_demo_project_title_font_consistency | 智能建造示范项目标题字体一致性 | 轻微 |
| TC-449 | TestIntelligentConstructionFonts.test_ic_project_card_title_font_consistency | 智能建造项目卡片标题字体一致性 | 轻微 |
| TC-450 | TestIntelligentConstructionFonts.test_ic_standard_name_font_consistency | 智能建造标准名称字体一致性 | 轻微 |

### 登录（4）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-472 | TestLoginFlow.test_login_modal_fields | 登录弹窗包含账号与验证码输入 | 严重 |
| TC-473 | TestLoginFlow.test_login_empty_submit_validation | 空表单登录被拦截并提示 | 严重 |
| TC-474 | TestLoginFlow.test_login_requires_agreement | 未勾选协议登录被拦截 | 一般 |
| TC-475 | TestLoginFlow.test_login_invalid_code_fails | 错误验证码登录失败且不跳转 | 一般 |

### 通用交互（5）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-476 | TestFilterSwitch.test_filter_switch_changes_list | 切换筛选项后列表内容必须变化 | 严重 |
| TC-477 | TestFilterSwitch.test_active_filter_is_detectable | 选中项高亮状态可识别 | 一般 |
| TC-478 | TestPagination.test_pagination_switches_content | 点击第 2 页后列表内容必须变化 | 严重 |
| TC-479 | TestPagination.test_pagination_back_to_first | 翻到第 2 页后可返回第 1 页 | 一般 |
| TC-480 | TestPagination.test_pagination_default_active_page | 分页页码默认选中第 1 页 | 一般 |

### 注册（6）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-481 | TestRegisterValidation.test_register_page_load_and_submit_disabled | 注册页加载且提交按钮默认禁用 | 严重 |
| TC-482 | TestRegisterValidation.test_register_required_markers | 必填项标记完整 | 一般 |
| TC-483 | TestRegisterValidation.test_register_invalid_phone_error | 非法手机号给出字段级错误 | 严重 |
| TC-484 | TestRegisterValidation.test_register_empty_submit_blocked | 空表单提交被拦截 | 严重 |
| TC-485 | TestRegisterValidation.test_register_agreement_required | 协议勾选校验 | 一般 |
| TC-486 | TestRegisterValidation.test_register_field_coverage | 注册字段完整性 | 一般 |

### 异常与韧性（2）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-487 | TestResilience.test_home_survives_api_failure | 接口不可用时首页仍渲染静态内容 | 一般 |
| TC-488 | TestResilience.test_list_survives_api_failure | 接口异常时列表给出空态而非崩溃 | 一般 |

### 供应大厅-搜索结果（10）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-503 | TestSupplyHallSearchResult.test_web_no_console_errors | Web-控制台无未知错误 | 一般 |
| TC-504 | TestSupplyHallSearchResult.test_web_no_placeholder_content | Web-无未知测试占位符内容 | 一般 |
| TC-505 | TestSupplyHallSearchResult.test_web_search_result_loads | Web-关键词搜索结果页加载与关键词回显 | 严重 |
| TC-506 | TestSupplyHallSearchResult.test_web_search_result_can_search_again | Web-搜索结果页可再次搜索 | 一般 |
| TC-507 | TestSupplyHallSearchResult.test_h5_no_console_errors | H5-控制台无未知错误 | 一般 |
| TC-508 | TestSupplyHallSearchResult.test_h5_no_placeholder_content | H5-无未知测试占位符内容 | 一般 |
| TC-509 | TestSupplyHallSearchResult.test_h5_search_result_loads | H5-关键词搜索结果页加载与展示 | 严重 |
| TC-510 | TestSupplyHallSearchResult.test_h5_search_result_controls | H5-搜索结果页重置/筛选控件可见性（如存在） | 一般 |
| TC-511 | TestSupplyHallSearchResult.test_web_search_result_no_result_hint | Web-无结果关键词展示空状态或推荐 | 一般 |
| TC-512 | TestSupplyHallSearchResult.test_h5_search_result_no_result_hint | H5-无结果关键词展示空状态或推荐 | 一般 |

### 视觉回归（2）

| 编号 | 用例名称 | 用例标题 | 严重程度 |
|------|----------|----------|----------|
| TC-513 | TestVisualRegression.test_home_visual | Web 首页首屏视觉基线 | 轻微 |
| TC-514 | TestVisualRegression.test_home_visual_h5 | H5 首页首屏视觉基线 | 轻微 |
