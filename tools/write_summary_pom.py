#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_pom.py
Вывод красивого отчёта о Page Object Pattern в GitHub Step Summary
"""

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    result_path = Path("tools/output/pom_result.txt")
    score_path = Path("tools/output/pom_score.txt")
    
    score = 0
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🏗️ Page Object Pattern\n\n")
        
        if score == 10:
            s.write("✅ **Page Object Pattern используется корректно!**\n\n")
            
            # Найдём классы
            pages_dir = Path("pages")
            if pages_dir.exists():
                import re
                classes = []
                for py_file in pages_dir.glob("*.py"):
                    if py_file.name == "__init__.py":
                        continue
                    content = py_file.read_text(encoding="utf-8")
                    found = re.findall(r'class\s+(\w+Page)\s*\(', content)
                    classes.extend(found)
                
                if classes:
                    s.write("**Найдены классы:**\n\n")
                    for c in classes:
                        s.write(f"- `{c}`\n")
                    s.write("\n")
        else:
            s.write("❌ **Page Object Pattern требует доработки**\n\n")
            s.write("💡 **Совет:** Создайте классы в `pages/` с суффиксом `Page`.\n\n")
        
        s.write(f"**Баллы:** `{score} / 10`\n\n")

if __name__ == "__main__":
    main()