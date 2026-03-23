#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_final_summary.py
Генерация итогового Summary с таблицей и прогресс-баром
"""

import os
from pathlib import Path

def read_score(file_path, default=0):
    try:
        return int(Path(file_path).read_text().strip() or default)
    except:
        return default

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    # Считываем баллы
    structure = read_score("tools/output/structure_score.txt", 0)
    lint = read_score("tools/output/lint_score.txt", 0)
    auth = read_score("tools/output/auth_score.txt", 0)
    cart = read_score("tools/output/cart_score.txt", 0)
    e2e = read_score("tools/output/e2e_score.txt", 0)
    pom = read_score("tools/output/pom_score.txt", 0)
    
    total = structure + lint + auth + cart + e2e + pom
    max_score = 110
    percentage = (total * 100) // max_score if max_score > 0 else 0
    
    # Оценка
    if total >= 90:
        grade = "🟢 Отлично"
        status = "Зачтено"
    elif total >= 70:
        grade = "🟡 Хорошо"
        status = "Зачтено"
    elif total >= 50:
        grade = "🟠 Удовлетворительно"
        status = "Зачтено"
    else:
        grade = "🔴 Требуется доработка"
        status = "Не зачтено"
    
    # Прогресс-бар
    filled = percentage // 5
    empty = 20 - filled
    progress = "🟩" * filled + "⬜" * empty
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n---\n\n")
        s.write("# 🏆 ИТОГОВАЯ ОЦЕНКА\n\n")
        
        s.write("| Параметр | Значение |\n")
        s.write("|----------|----------|\n")
        s.write(f"| 💯 Баллы | **{total} / {max_score}** |\n")
        s.write(f"| 📈 Процент | **{percentage}%** |\n")
        s.write(f"| 🎓 Оценка | **{grade}** |\n")
        s.write(f"| ✅ Статус | **{status}** |\n")
        s.write("\n")
        
        s.write("## Прогресс\n\n")
        s.write(f"`[{progress}]` {percentage}%\n\n")
        
        s.write("## 📋 Детализация по критериям\n\n")
        s.write("| Критерий | Баллы | Статус |\n")
        s.write("|----------|-------|--------|\n")
        
        s1 = "✅" if structure == 10 else "❌"
        s2 = "✅" if lint >= 12 else "⚠️"
        s3 = "✅" if auth >= 20 else "⚠️"
        s4 = "✅" if cart >= 20 else "⚠️"
        s5 = "✅" if e2e == 25 else "❌"
        s6 = "✅" if pom == 10 else "❌"
        
        s.write(f"| 📁 Структура | {structure} / 10 | {s1} |\n")
        s.write(f"| 🧹 Линтинг | {lint} / 15 | {s2} |\n")
        s.write(f"| 🔐 Авторизация | {auth} / 25 | {s3} |\n")
        s.write(f"| 🛒 Корзина | {cart} / 25 | {s4} |\n")
        s.write(f"| 💳 E2E тест | {e2e} / 25 | {s5} |\n")
        s.write(f"| 🏗️ POM | {pom} / 10 | {s6} |\n")
        s.write("\n")
        
        s.write("## 📎 Артефакты\n\n")
        s.write("Все артефакты доступны в разделе **Actions → Artifacts**.\n\n")
        
        s.write("| Тип | Путь |\n")
        s.write("|-----|------|\n")
        s.write("| 📸 Скриншоты | `output/screenshots/` |\n")
        s.write("| 📄 Отчёты | `output/reports/` |\n")
        s.write("| 📊 JSON | `tools/output/` |\n")
        s.write("\n")
        
        s.write("---\n\n")
        s.write(f"**💪 ИТОГО: {total} баллов из {max_score}**\n\n")
        s.write("*Отчёт сгенерирован автоматически GitHub Classroom Autograder*  \n")
        s.write("*Версия: 2026.03 (адаптировано для РФ)*\n")

if __name__ == "__main__":
    main()