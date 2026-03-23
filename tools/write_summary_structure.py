#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_structure.py
Вывод красивого отчёта о структуре в GitHub Step Summary
"""

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    required = {
        "pages/": False,
        "tests/": False,
        "conftest.py": False,
        "pytest.ini": False,
        "requirements.txt": False
    }
    
    for path in required.keys():
        required[path] = Path(path).exists()
    
    all_ok = all(required.values())
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 📁 Структура проекта\n\n")
        
        if all_ok:
            s.write("✅ **Все обязательные файлы на месте**\n\n")
        else:
            missing = [k for k, v in required.items() if not v]
            s.write(f"❌ **Отсутствуют:** `{', '.join(missing)}`\n\n")
        
        s.write("| Компонент | Статус |\n")
        s.write("|-----------|--------|\n")
        for component, exists in required.items():
            icon = "✅" if exists else "❌"
            s.write(f"| `{component}` | {icon} |\n")
        s.write("\n")

if __name__ == "__main__":
    main()