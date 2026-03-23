#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_lint.py
Вывод красивого отчёта о линтинге в GitHub Step Summary
"""

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    report_path = Path("tools/output/flake8_report.txt")
    score_path = Path("tools/output/lint_score.txt")
    
    error_count = 0
    score = 0
    
    if report_path.exists():
        content = report_path.read_text(encoding="utf-8")
        error_count = content.count(":") if content.strip() else 0
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🧹 Линтинг (flake8)\n\n")
        
        if error_count == 0:
            s.write("✅ **Ошибок не найдено!** Код соответствует стандартам.\n\n")
        else:
            s.write(f"⚠️ **Найдено ошибок:** `{error_count}`\n\n")
            
            if report_path.exists():
                content = report_path.read_text(encoding="utf-8")
                lines = [l for l in content.split('\n') if l.strip()][:10]
                if lines:
                    s.write("### Примеры ошибок:\n\n```")
                    s.write('\n'.join(lines))
                    s.write("\n```\n\n")
            
            s.write("💡 **Совет:** Исправьте ошибки по порядку.\n\n")
        
        s.write(f"**Баллы:** `{score} / 15`\n\n")

if __name__ == "__main__":
    main()