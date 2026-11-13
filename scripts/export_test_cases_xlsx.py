"""兼容入口：原 xlsx 导出脚本，现统一由 export_test_cases.py 实现。

用法：
    python scripts/export_test_cases_xlsx.py            # 生成 md + csv + xlsx
    python scripts/export_test_cases.py --format xlsx   # 仅 Excel
"""
from export_test_cases import main

if __name__ == "__main__":
    main()