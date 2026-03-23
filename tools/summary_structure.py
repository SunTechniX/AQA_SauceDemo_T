#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/summary_structure.py
Вывод результата проверки структуры в GitHub Summary
"""

import json
import sys
from pathlib import Path

def main():
    report_path = Path("tools/output/structure_result.json")
    
    if not report_path.exists():
        print("⚠️ Отчёт структуры не найден")
        return 0
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        checks = data.get('checks', {}).get('structure', {})
        
        if checks.get('passed'):
            print("✅ Все обязательные файлы на месте")
        else:
            missing = checks.get('missing', [])
            if missing:
                print(f"❌ Отсутствуют: {', '.join(missing)}")
            else:
                print("❌ Проверка не пройдена")
        
        # Детали
        details = checks.get('details', [])
        if details:
            print("")
            print("| Компонент | Статус |")
            print("|-----------|--------|")
            for d in details:
                name = d.get('name', 'Unknown')
                passed = d.get('passed', False)
                icon = "✅" if passed else "❌"
                print(f"| `{name}` | {icon} |")
        
        return 0
    except Exception as e:
        print(f"⚠️ Ошибка чтения отчёта: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())