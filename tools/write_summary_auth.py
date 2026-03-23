#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_auth.py
Вывод красивого отчёта о тестах авторизации в GitHub Step Summary
"""

COUNT_TESTS = 10

import os
import json
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    results_path = Path("tools/output/auth_results.json")
    output_path = Path("tools/output/auth_output.txt")
    score_path = Path("tools/output/auth_score.txt")
    passed_path = Path("tools/output/auth_passed.txt")
    
    passed = 0
    score = 0
    
    if passed_path.exists():
        passed = int(passed_path.read_text().strip() or "0")
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🔐 Тесты авторизации\n\n")
        
        if passed >= COUNT_TESTS:
            s.write(f"✅ **Все тесты пройдены!** ({passed}/{COUNT_TESTS})\n\n")
        else:
            s.write(f"⚠️ **Пройдено тестов:** `{passed}/{COUNT_TESTS}`\n\n")
            
            if output_path.exists():
                content = output_path.read_text(encoding="utf-8")
                errors = [l for l in content.split('\n') if 'FAILED' in l or 'ERROR' in l][:5]
                if errors:
                    s.write("### Ошибки:\n\n```")
                    s.write('\n'.join(errors))
                    s.write("\n```\n\n")
            
            s.write("💡 **Совет:** Проверьте локаторы и ожидания.\n\n")
        
        s.write(f"**Баллы:** `{score} / 25`\n\n")

if __name__ == "__main__":
    main()