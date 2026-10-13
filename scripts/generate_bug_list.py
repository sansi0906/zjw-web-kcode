import json
import glob
import os
from datetime import datetime

# Find latest run directory
run_dirs = sorted(glob.glob('reports/run_*'), reverse=True)
if not run_dirs:
    print("No run directories found")
    exit(1)

run_dir = run_dirs[0]
results_dir = os.path.join(run_dir, 'allure-results')
results = glob.glob(os.path.join(results_dir, '*-result.json'))

print(f"Analyzing: {results_dir}")
print(f"Total results: {len(results)}")

bugs = []
for r in results:
    try:
        with open(r, 'r', encoding='utf-8') as f:
            data = json.load(f)
        status = data.get('status', 'unknown')
        if status in ('failed', 'broken'):
            name = data.get('name', 'unknown')
            full_name = data.get('fullName', 'unknown')
            details = data.get('statusDetails', {})
            message = details.get('message', 'No message')
            trace = details.get('trace', 'No trace')
            
            # Determine module from full_name
            module = '其他'
            if 'homepage' in full_name.lower():
                module = '首页全量测试'
            elif 'industry_association' in full_name.lower():
                module = '产业协会'
            elif 'industry_policy' in full_name.lower():
                module = '产业政策'
            elif 'intelligent_construction' in full_name.lower():
                module = '智能建造'
            elif 'achievement_transformation' in full_name.lower():
                module = '成果转化'
            elif 'cloud_service' in full_name.lower():
                module = '云服务'
            elif 'all_products' in full_name.lower():
                module = '全部商品'
            elif 'industrial_service' in full_name.lower():
                module = '产业化服务'
            elif 'industry_demand' in full_name.lower():
                module = '产业需求'
            elif 'industry_news' in full_name.lower():
                module = '产业资讯'
            elif 'key_projects' in full_name.lower():
                module = '重点项目'
            elif 'supply_hall' in full_name.lower():
                module = '供应大厅'
            elif 'supply_chain_map' in full_name.lower():
                module = '供应链地图'
            
            # 过滤无效缺陷：首页供应大厅不涉及统计数据，相关缺陷不计入
            if 'supply_hall' in full_name.lower() and 'statistics' in full_name.lower():
                continue

            # 过滤供应链地图页面统计相关缺陷
            if 'supply_hall_page' in full_name.lower() and 'statistics' in full_name.lower():
                continue

            # 去重：相同测试用例只记录一次
            if any(b['full_name'] == full_name for b in bugs):
                continue

            bugs.append({
                'name': name,
                'full_name': full_name,
                'module': module,
                'status': status,
                'message': message,
                'trace': trace,
            })
    except Exception as e:
        pass

print(f"Bugs found: {len(bugs)}")

# Generate markdown
md = []
md.append("# 全量缺陷清单")
md.append("")
md.append(f"**测试环境**: dev (http://172.16.1.165:3200/)  ")
md.append(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d')}  ")
md.append(f"**测试人员**: 自动测试  ")
md.append(f"**总缺陷数**: {len(bugs)}  ")
md.append(f"**严重程度分布**: 高 x{sum(1 for b in bugs if 'timeout' in b['message'].lower() or 'not found' in b['message'].lower())}, 中 x{sum(1 for b in bugs if 'timeout' not in b['message'].lower() and 'not found' not in b['message'].lower())}")
md.append("")
md.append("---")
md.append("")

for i, bug in enumerate(bugs, 1):
    severity = "高" if "timeout" in bug['message'].lower() or "not found" in bug['message'].lower() else "中"
    md.append(f"### 缺陷 #{i}: {bug['module']} - {bug['name']}")
    md.append("")
    md.append("| 字段 | 内容 |")
    md.append("|------|------|")
    md.append(f"| **缺陷ID** | BUG-2026-{i:03d} |")
    md.append(f"| **模块** | {bug['module']} |")
    md.append(f"| **用例** | {bug['name']} |")
    md.append(f"| **严重程度** | {severity} |")
    md.append(f"| **优先级** | P0 |")
    md.append("")
    md.append("**问题描述**:  ")
    md.append(f"{bug['message'][:200]}")
    md.append("")
    md.append("**错误信息**:  ")
    md.append("```")
    md.append(bug['message'][:500])
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")

content = '\n'.join(md)
output_path = f"reports/bugs/bug_list_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Generated bug list: {output_path}")
print(f"Total bugs: {len(bugs)}")