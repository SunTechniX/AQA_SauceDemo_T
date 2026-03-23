#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/summary_generator.py
Генератор красивого Summary отчёта для GitHub Actions

Использование:
    python tools/summary_generator.py >> $GITHUB_STEP_SUMMARY
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json
import re


class SummaryGenerator:
    """Генератор красивого Summary отчёта для GitHub Actions"""
    
    def __init__(self):
        self.project_path = Path(".")
        self.tools_output = Path("tools/output")
    
    def generate_header(self) -> str:
        """Генерация заголовка отчёта"""
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        repo = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
        run_id = os.environ.get("GITHUB_RUN_ID", "N/A")
        branch = os.environ.get("GITHUB_REF_NAME", "unknown")
        
        return f"""
# 🎓 Отчёт о проверке проекта SauceDemo Playwright

| Параметр | Значение |
|----------|----------|
| 📦 Репозиторий | `{repo}` |
| 🔢 Run ID | `{run_id}` |
| 🌿 Ветка | `{branch}` |
| 🕐 Дата проверки | `{now}` |
| 🌍 Регион | Россия (адаптировано) |

---
"""
    
    def generate_structure_section(self) -> str:
        """Секция со структурой проекта"""
        section = "## 📁 Структура проекта\n\n"
        
        required = {
            "pages/": False,
            "tests/": False,
            "conftest.py": False,
            "pytest.ini": False,
            "requirements.txt": False
        }
        
        missing = []
        for path in required.keys():
            full_path = self.project_path / path
            exists = full_path.exists()
            required[path] = exists
            if not exists:
                missing.append(path)
        
        all_ok = all(required.values())
        
        section += "| Компонент | Статус |\n"
        section += "|-----------|--------|\n"
        for component, exists in required.items():
            icon = "✅" if exists else "❌"
            section += f"| `{component}` | {icon} |\n"
        
        if missing:
            section += f"\n⚠️ **Отсутствуют:** `{', '.join(missing)}`\n"
            section += "\n💡 **Совет:** Создайте недостающие файлы и папки согласно шаблону.\n"
        
        section += f"\n**Общий статус:** {'✅ Все компоненты на месте' if all_ok else '❌ Требуются исправления'}\n\n"
        return section
    
    def generate_linting_section(self) -> str:
        """Секция с результатами линтинга"""
        section = "## 🧹 Линтинг (flake8)\n\n"
        
        flake8_report = self.tools_output / "flake8_report.txt"
        
        if flake8_report.exists():
            content = flake8_report.read_text(encoding="utf-8")
            
            # Подсчёт ошибок по типам
            error_counts = {}
            errors_list = []
            for line in content.split('\n'):
                if line.strip() and ':' in line and not line.startswith(' '):
                    errors_list.append(line)
                    match = re.search(r'\b([A-Z]\d+)\b', line)
                    if match:
                        code = match.group(1)
                        error_counts[code] = error_counts.get(code, 0) + 1
            
            total_errors = len(errors_list)
            
            if total_errors == 0:
                section += "✅ **Ошибок не найдено!** Код соответствует стандартам PEP8.\n\n"
            else:
                section += f"⚠️ **Найдено ошибок:** `{total_errors}`\n\n"
                
                if error_counts:
                    section += "| Код ошибки | Описание | Количество |\n"
                    section += "|------------|----------|------------|\n"
                    error_descriptions = {
                        "E501": "Длина строки > 120 символов",
                        "E302": "Ожидается 2 пустых строки",
                        "E305": "Ожидается 2 пустых строки в конце",
                        "F401": "Импортировано, но не используется",
                        "F403": "Wildcard import",
                        "W291": "Лишний пробел в конце строки",
                        "W293": "Лишняя пустая строка",
                        "N801": "Имя класса должно быть в CamelCase",
                        "N802": "Имя функции должно быть в lowercase"
                    }
                    for code, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                        desc = error_descriptions.get(code, "Другая ошибка")
                        section += f"| `{code}` | {desc} | {count} |\n"
                    section += "\n"
                
                # Первые 10 ошибок для примера
                if errors_list:
                    section += "### Примеры ошибок для исправления:\n\n```"
                    section += '\n'.join(errors_list[:10])
                    section += "\n```\n\n"
                
                section += "💡 **Как исправить:**\n"
                section += "```bash\n"
                section += "# Запустите локально с подробным выводом\n"
                section += "flake8 student_template/ --config=tools/flake8_config.cfg --show-source\n"
                section += "```\n\n"
        else:
            section += "⚠️ Отчёт flake8 не найден. Проверьте, что линтинг прошёл успешно.\n\n"
        
        return section
    
    def generate_tests_section(self) -> str:
        """Секция с результатами тестов"""
        section = "## 🧪 Результаты тестов\n\n"
        
        # Поиск отчётов pytest
        reports_found = []
        if self.tools_output.exists():
            for report in self.tools_output.glob("*_results.json"):
                reports_found.append(report.name)
        
        # Подсчёт тестов
        test_count = 0
        test_files = []
        tests_dir = self.project_path / "tests"
        if tests_dir.exists():
            for test_file in tests_dir.glob("test_*.py"):
                content = test_file.read_text(encoding="utf-8")
                tests = re.findall(r'def\s+(test_\w+)\s*\(', content)
                test_count += len(tests)
                test_files.append({"file": test_file.name, "tests": len(tests)})
        
        section += f"**Всего тестов найдено:** `{test_count}`\n\n"
        
        if test_files:
            section += "| Файл | Количество тестов |\n"
            section += "|------|-------------------|\n"
            for tf in test_files:
                section += f"| `{tf['file']}` | {tf['tests']} |\n"
            section += "\n"
        
        if test_count < 5:
            section += "⚠️ **Рекомендация:** Добавьте больше тестов (минимум 5 для зачёта).\n\n"
        
        return section
    
    def generate_pom_section(self) -> str:
        """Секция с проверкой Page Object Pattern"""
        section = "## 🏗️ Page Object Pattern\n\n"
        
        pages_dir = self.project_path / "pages"
        pom_classes = []
        
        if pages_dir.exists():
            for py_file in pages_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                content = py_file.read_text(encoding="utf-8")
                classes = re.findall(r'class\s+(\w+Page)\s*\(', content)
                if classes:
                    pom_classes.append({"file": py_file.name, "classes": classes})
        
        if pom_classes:
            section += "✅ **Page Object классы найдены:**\n\n"
            section += "| Файл | Классы |\n"
            section += "|------|--------|\n"
            for pom in pom_classes:
                classes_str = ", ".join(pom["classes"])
                section += f"| `{pom['file']}` | `{classes_str}` |\n"
            section += "\n"
        else:
            section += "❌ **Page Object классы не найдены.**\n\n"
            section += "💡 **Совет:** Создайте классы в `pages/` с суффиксом `Page`:\n"
            section += "```python\n"
            section += "class LoginPage(BasePage):\n"
            section += "    def login(self, username, password):\n"
            section += "        self.page.fill('#user-name', username)\n"
            section += "        self.page.fill('#password', password)\n"
            section += "        self.page.click('#login-button')\n"
            section += "```\n\n"
        
        # Проверка импортов в тестах
        tests_dir = self.project_path / "tests"
        pom_imports = False
        if tests_dir.exists():
            for test_file in tests_dir.glob("*.py"):
                content = test_file.read_text(encoding="utf-8")
                if "from pages" in content or "import pages" in content:
                    pom_imports = True
                    break
        
        if pom_imports:
            section += "✅ Тесты импортируют Page Objects\n\n"
        else:
            section += "⚠️ Тесты не импортируют Page Objects\n\n"
            section += "💡 **Совет:** Добавьте импорт в тесты:\n"
            section += "```python\n"
            section += "from pages.login_page import LoginPage\n"
            section += "```\n\n"
        
        return section
    
    def generate_recommendations(self) -> str:
        """Секция с рекомендациями"""
        section = "## 💡 Рекомендации по улучшению\n\n"
        
        recommendations = []
        
        # Проверка структуры
        if not (self.project_path / "pages").exists():
            recommendations.append("📁 Создайте папку `pages/` для Page Objects")
        
        if not (self.project_path / "conftest.py").exists():
            recommendations.append("🔧 Добавьте `conftest.py` с фикстурами")
        
        # Проверка тестов
        tests_dir = self.project_path / "tests"
        test_count = 0
        if tests_dir.exists():
            for test_file in tests_dir.glob("test_*.py"):
                content = test_file.read_text(encoding="utf-8")
                test_count += len(re.findall(r'def\s+(test_\w+)\s*\(', content))
        
        if test_count < 5:
            recommendations.append(f"🧪 Добавьте ещё тестов (сейчас: {test_count}, рекомендуется: 5+)")
        
        # Проверка скриншотов
        screenshots_dir = self.project_path / "output" / "screenshots"
        if not screenshots_dir.exists():
            recommendations.append("📸 Настройте сохранение скриншотов при падении тестов")
        
        # Проверка отчётов
        reports_dir = self.project_path / "output" / "reports"
        if not reports_dir.exists():
            recommendations.append("📊 Настройте генерацию HTML-отчётов pytest")
        
        if recommendations:
            for rec in recommendations:
                section += f"- {rec}\n"
        else:
            section += "✅ Все базовые требования выполнены! Отличная работа!\n"
        
        section += "\n---\n\n"
        return section
    
    def generate_footer(self) -> str:
        """Подвал отчёта"""
        return f"""
## 📎 Артефакты

Артефакты этой проверки доступны для скачивания в разделе **Actions → Artifacts**.

| Тип | Путь |
|-----|------|
| 📸 Скриншоты | `student_template/output/screenshots/` |
| 📄 HTML отчёты | `student_template/output/reports/` |
| 📊 JSON результаты | `tools/output/` |
| 🧹 Линтинг отчёт | `tools/output/flake8_report.txt` |

---

*Отчёт сгенерирован автоматически GitHub Classroom Autograder*  
*Версия: 2026.03 (адаптировано для РФ)*
"""
    
    def generate_full_summary(self) -> str:
        """Генерация полного Summary"""
        summary = ""
        summary += self.generate_header()
        summary += self.generate_structure_section()
        summary += self.generate_linting_section()
        summary += self.generate_tests_section()
        summary += self.generate_pom_section()
        summary += self.generate_recommendations()
        summary += self.generate_footer()
        
        return summary
    
    def save_summary(self):
        """Сохранение Summary в файл"""
        self.tools_output.mkdir(parents=True, exist_ok=True)
        summary_path = self.tools_output / "summary.txt"
        
        summary = self.generate_full_summary()
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary


def main():
    generator = SummaryGenerator()
    
    # Сохранение в файл
    summary = generator.save_summary()
    
    # Вывод для GitHub Actions
    print("\n---\n")
    print(summary)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
