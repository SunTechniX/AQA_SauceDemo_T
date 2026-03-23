#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_e2e.py
Вывод красивого отчёта о E2E тесте в GitHub Step Summary
"""

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    output_path = Path("tools/output/e2e_output.txt")
    score_path = Path("tools/output/e2e_score.txt")
    
    score = 0
    passed = False
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
        passed = (score == 25)
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 💳 E2E тест (полный цикл покупки)\n\n")
        
        if passed:
            s.write("✅ **Тест пройден!** Полный цикл покупки работает корректно.\n\n")
        else:
            s.write("❌ **Тест не пройден**\n\n")
            
            if output_path.exists():
                content = output_path.read_text(encoding="utf-8")
                errors = [l for l in content.split('\n') if 'FAILED' in l or 'AssertionError' in l][:5]
                if errors:
                    s.write("### Ошибка:\n\n```")
                    s.write('\n'.join(errors))
                    s.write("\n```\n\n")
            
            s.write("💡 **Совет:** Проверьте каждый шаг: авторизация → товар → корзина → чекаут → подтверждение.\n\n")
        
        s.write(f"**Баллы:** `{score} / 25`\n\n")

if __name__ == "__main__":
    main()