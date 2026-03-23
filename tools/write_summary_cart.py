#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_cart.py
Вывод красивого отчёта о тестах корзины в GitHub Step Summary
"""

COUNT_TESTS = 10

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    passed_path = Path("tools/output/cart_passed.txt")
    score_path = Path("tools/output/cart_score.txt")
    
    passed = 0
    score = 0
    
    if passed_path.exists():
        passed = int(passed_path.read_text().strip() or "0")
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🛒 Тесты корзины\n\n")
        
        if passed >= COUNT_TESTS:
            s.write(f"✅ **Все тесты пройдены!** ({passed}/{COUNT_TESTS})\n\n")
        else:
            s.write(f"⚠️ **Пройдено тестов:** `{passed}/{COUNT_TESTS}`\n\n")
            s.write("💡 **Совет:** Проверьте работу с корзиной.\n\n")
        
        s.write(f"**Баллы:** `{score} / 25`\n\n")

if __name__ == "__main__":
    main()