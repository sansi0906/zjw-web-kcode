# 字体一致性测试用例

> 测试环境：http://172.16.1.165:3200/
> Web 端 viewport：1920x1080；H5 端 viewport：390x844
> 对比属性统一为：fontFamily、fontSize、fontWeight、color
> 当前字体一致性用例总数：**62 个**（全部通过）

---

## 一、首页 Web 端（`tests/test_homepage_full.py`，18 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_section_title_font_consistency` | H2 区块标题：产业服务、津筑云商、会展活动、产业需求、产业政策 | 34px / 500 / rgb(23, 26, 29) | ✅ |
| 2 | `test_service_card_title_font_consistency` | H3 服务卡片标题：供应大厅、劳务对接、AI+工具集、金融服务、建筑机器人、智慧工地 | 26px / 500 / rgb(23, 26, 29) | ✅ |
| 3 | `test_button_font_consistency` | Tab 按钮：行业动态、政策资讯、政策解读 | 16px / 600（颜色随激活态变化，已排除） | ✅ |
| 4 | `test_jzys_tab_font_consistency` | 津筑云商 Tab：产业生态全景图、建筑服务业、建筑制造业、建筑建造业 | 16px / 400（颜色随激活态变化，已排除） | ✅ |
| 5 | `test_body_desc_font_consistency` | 描述文字：全方位服务产业链、平台优质企业，精准商务对接、聚焦建筑行业各类活动 | 18px / 400 / rgb(111, 122, 155) | ✅ |
| 6 | `test_footer_nav_font_consistency` | 页脚导航：供应大厅、产业政策、智能建造、重点项目 | 16px / 500 / rgb(255, 255, 255) | ✅ |
| 7 | `test_footer_service_font_consistency` | 页脚服务链接：建材出售、建材出租、设备出售、设备出租、劳务用工、产业需求 | 14px / 400 / rgba(255, 255, 255, 0.7) | ✅ |
| 8 | `test_view_all_font_consistency` | 所有"查看全部"按钮 | 14px / 400 / rgb(22, 83, 255) | ✅（站点已修复 14px/16px 混用） |
| 9 | `test_hot_search_font_consistency` | 热搜词：热搜词名称一 ~ 热搜词名称六 | 14px / 400 / rgb(22, 83, 255) | ✅ |
| 10 | `test_news_title_font_consistency` | 新闻标题：云南石材建材产业发展峰会、绿色建筑新浪潮来袭！2027广州住博会！ | 18px / 500 / rgb(18, 69, 214) | ✅ |
| 11 | `test_supply_item_font_consistency` | 供应品目：施工电梯、配电箱、灯具、开关面板、PVC管材、管件、门窗工程 | 16px / 500 / rgb(23, 26, 29) | ✅ |
| 12 | `test_nav_link_font_consistency` | 顶部导航链接：供应大厅、智能建造、重点项目、产业政策 | 16px / 400 / rgb(51, 51, 51) | ✅ |
| 13 | `test_exhibition_info_font_consistency` | 会展时间/地点：2026-10-06—2026-10-27、昆明世纪城国际会议中心、2026-10-01—2026-11-10 | 12px / 400 / rgb(116, 118, 119) | ✅ |
| 14 | `test_demand_contact_font_consistency` | 需求联系人：董经理、刘经理 | 16px / 500 / rgb(23, 26, 29) | ✅ |
| 15 | `test_demand_count_font_consistency` | 需求数量：150、195、170 | 32px / 400 / rgb(255, 49, 24) | ✅ |
| 16 | `test_news_date_font_consistency` | 新闻日期：2026-10-10、2026-10-08 | 14px / 400 / rgb(23, 26, 29) | ✅ |
| 17 | `test_news_desc_font_consistency` | 新闻描述：微风范围分为访问范围、范围分为访问范围、时代大厦… | 12px / 400 / rgb(116, 118, 119) | ✅ |
| 18 | `test_float_button_font_consistency` | 悬浮按钮：在线客服、意向填报 | 12px / 400 / rgb(22, 83, 255) | ✅ |

---

## 二、首页 H5 移动端（`tests/test_homepage_h5_fonts.py`，15 个用例）

| # | 用例名 | 测试元素 | 结果 |
|---|--------|---------|------|
| 1 | `test_h5_section_title_font_consistency` | H2 区块标题 | ✅ |
| 2 | `test_h5_service_card_title_font_consistency` | H3 服务卡片标题 | ✅ |
| 3 | `test_h5_body_desc_font_consistency` | 描述文字 | ✅ |
| 4 | `test_h5_footer_nav_font_consistency` | 页脚导航链接 | ✅ |
| 5 | `test_h5_hot_search_font_consistency` | 热搜词 | ✅ |
| 6 | `test_h5_news_title_font_consistency` | 新闻标题 | ✅ |
| 7 | `test_h5_supply_item_font_consistency` | 供应品目 | ✅ |
| 8 | `test_h5_footer_service_font_consistency` | 页脚服务链接 | ✅ |
| 9 | `test_h5_nav_link_font_consistency` | 顶部导航链接 | ✅ |
| 10 | `test_h5_exhibition_info_font_consistency` | 会展时间/地点 | ✅ |
| 11 | `test_h5_demand_contact_font_consistency` | 需求联系人 | ✅ |
| 12 | `test_h5_demand_count_font_consistency` | 需求数量 | ✅ |
| 13 | `test_h5_news_date_font_consistency` | 新闻日期 | ✅ |
| 14 | `test_h5_news_desc_font_consistency` | 新闻描述 | ✅ |
| 15 | `test_h5_float_button_font_consistency` | 悬浮按钮 | ✅ |

> H5 端字号为 PC 端的等比缩放值（如 34px → 17.2656px），用例只做同组元素之间的一致性比对。

---

## 三、供应大厅（`tests/test_supply_hall_fonts.py`，7 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_supply_hall_category_title_font_consistency` | H2 分类标题：建筑材料、水电暖通、机械设备、工程机械、劳务用工 | 24px / 500 / rgb(23, 26, 29) | ✅ |
| 2 | `test_supply_hall_subcategory_title_font_consistency` | H3 子分类标题：土建、装饰装修、给排水、电气、智能设备、专业设备、起重机械、混凝土机械 | 20px / 500 / rgb(0, 28, 111) | ✅ |
| 3 | `test_supply_hall_view_all_font_consistency` | "查看全部"按钮 | 14px / 400 | ✅ |
| 4 | `test_supply_hall_stats_number_font_consistency` | 统计数字：500+、10万+、3分钟、1万+ | 24px / 600 / rgb(22, 83, 255) | ✅ |
| 5 | `test_supply_hall_stats_label_font_consistency` | 统计标签：商品种类、在售商品、求购响应、供需对接 | 20px / 500 / rgb(23, 26, 29) | ✅ |
| 6 | `test_supply_hall_category_desc_font_consistency` | 分类描述：覆盖项目主体与装饰全流程的各类建材供应等 | 16px / 400 / rgb(116, 118, 119) | ✅ |
| 7 | `test_supply_hall_service_tag_font_consistency` | 服务标签：服务好、老师傅、性价比高、效率高 | 13px / 400 / rgb(23, 26, 29) | ✅ |

---

## 四、产业新闻（`tests/test_industry_news_fonts.py`，3 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_news_title_font_consistency` | H2 新闻标题：饿飞飞飞我分为、测试新增、开幕！2025第五届国际工程建设供应链博览会！ | 16px / 500 / rgb(23, 26, 29) | ✅ |
| 2 | `test_news_desc_font_consistency` | P 新闻描述：微风范围分为访问范围、范围分为访问范围、时代大厦… | 12px / 400 / rgb(116, 118, 119) | ✅ |
| 3 | `test_news_time_font_consistency` | TIME 发布时间：2026-10-10、2026-10-08、2025-09-23 | 14px / 400 / rgb(23, 26, 29) | ✅ |

---

## 五、产业需求（`tests/test_demand_page_fonts.py`，3 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_demand_desc_font_consistency` | 需求描述：住宅配套系列，含专票卸车。 等 | 14px / 400 / rgb(116, 118, 119) | ✅ |
| 2 | `test_demand_amount_font_consistency` | 需求金额：150万元、19万元、15万元、22万元 | 14px / 400 / rgb(255, 49, 24) | ✅ |
| 3 | `test_demand_big_amount_font_consistency` | 大号金额：150万、19万、15万、22万 | 32px / 400 / rgb(255, 49, 24) | ✅ |

---

## 六、重点项目（`tests/test_key_project_fonts.py`，3 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_kp_project_title_font_consistency` | 项目标题：胡家园学校校舍修缮工程施工 等 | 24px / 500 / rgb(23, 26, 29) | ✅ |
| 2 | `test_kp_filter_tab_font_consistency` | 筛选 Tab：房建项目、市政项目、其他项目 | 24px / 400 / rgb(51, 51, 51) | ✅ |
| 3 | `test_kp_desc_font_consistency` | 项目描述：招标施工天津市、天津市、胡家园学校… | 14px / 400 / rgb(51, 54, 57) | ✅ |

---

## 七、智能建造（`tests/test_intelligent_construction_fonts.py`，3 个用例）

| # | 用例名 | 测试元素 | 结果 |
|---|--------|---------|------|
| 1 | `test_ic_demo_project_title_font_consistency` | 示范项目标题 | ✅ |
| 2 | `test_ic_project_card_title_font_consistency` | 项目卡片标题 | ✅ |
| 3 | `test_ic_standard_name_font_consistency` | 标准名称 | ✅ |

---

## 八、产业协会（`tests/test_industry_association_fonts.py`，2 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_ia_association_name_font_consistency` | 协会名称：天津市建筑业协会、天津市钢结构幕墙和门窗协会 等 | 20px / 500 / rgb(23, 26, 29) | ✅ |
| 2 | `test_ia_demo_news_title_font_consistency` | 示范企业新闻标题：【津造未来】… | 24px / 500 / rgba(0, 0, 0, 0.9) | ✅ |

---

## 九、成果转化（`tests/test_achievement_transformation_fonts.py`，4 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_at_project_title_font_consistency` | 成果标题：复杂环境下适应性深基坑智能建造技术的研发与应用 等 | 24px / 500 / rgb(0, 51, 129) | ✅ |
| 2 | `test_at_institution_name_font_consistency` | 机构名称：天津城建大学、天津大学、国土学院、河北工业大学 | 24px / 500 / rgba(0, 0, 0, 0.9) | ✅ |
| 3 | `test_at_company_font_consistency` | 研发单位：中国建筑第六工程局有限公司、中国铁建大桥局集团有限公司 等 | 14px / 400 / rgb(116, 118, 119) | ✅ |
| 4 | `test_at_tech_tag_font_consistency` | 技术方向标签：装配式建筑智能BIM设计与优化、建筑智能数字化设计 等 | 14px / 400 / rgb(99, 110, 128) | ✅ |

---

## 十、云服务（`tests/test_cloud_service_fonts.py`，2 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_cs_service_name_font_consistency` | 服务名称：项目管理、设计生产协同、智慧工地系统 等 | 24px / 500 / rgb(0, 58, 140) | ✅ |
| 2 | `test_cs_service_desc_font_consistency` | 服务描述：经营数据可视化，动态监控项目经营 等 | 14px / 400 / rgb(0, 58, 140) | ✅ |

---

## 十一、产业政策（`tests/test_industry_policy_fonts.py`，2 个用例）

| # | 用例名 | 测试元素 | 预期值 | 结果 |
|---|--------|---------|--------|------|
| 1 | `test_ip_filter_tab_font_consistency` | 筛选 Tab：政策资讯、政策解读、行业动态 | 24px / 400 / rgb(51, 51, 51) | ✅ |
| 2 | `test_ip_policy_title_font_consistency` | 政策标题：中共中央办公厅 国务院办公厅… 等 | 24px / 500 / rgb(29, 33, 41) | ✅ |

---

## 测试文件清单

| 测试文件 | 页面 | 用例数 |
|---------|------|--------|
| `tests/test_homepage_full.py` | 首页 Web | 18 |
| `tests/test_homepage_h5_fonts.py` | 首页 H5 | 15 |
| `tests/test_supply_hall_fonts.py` | 供应大厅 | 7 |
| `tests/test_industry_news_fonts.py` | 产业新闻 | 3 |
| `tests/test_demand_page_fonts.py` | 产业需求 | 3 |
| `tests/test_key_project_fonts.py` | 重点项目 | 3 |
| `tests/test_intelligent_construction_fonts.py` | 智能建造 | 3 |
| `tests/test_industry_association_fonts.py` | 产业协会 | 2 |
| `tests/test_achievement_transformation_fonts.py` | 成果转化 | 4 |
| `tests/test_cloud_service_fonts.py` | 云服务 | 2 |
| `tests/test_industry_policy_fonts.py` | 产业政策 | 2 |
| **总计** | | **62** |

---

## 覆盖策略说明

1. **同组比对**：针对同一视觉分组内的多个同类元素（标题组、描述组、标签组、统计组等）比对 fontFamily / fontSize / fontWeight / color，避免逐个元素写死期望值。
2. **状态色排除**：Tab 类元素因激活/非激活态颜色不同，比对时排除 color，仅比对字体族、字号、字重。
3. **最少 2 个元素**：每个用例至少要求找到 2 个可见元素才进行比对，避免页面改版后用例空跑。
4. **PC / H5 对照**：H5 字号为等比缩放值，不与 PC 端硬比较，仅在 H5 内部做组内一致性校验。
5. **文本脆弱性**：部分新闻标题/描述为测试环境占位内容，站点文案调整时需同步更新用例中的定位文本。
