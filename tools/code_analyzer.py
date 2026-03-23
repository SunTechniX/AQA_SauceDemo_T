#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/code_analyzer.py
Анализатор кода студенческого проекта для GitHub Classroom
Проверка структуры, Page Object Pattern, качества кода

Использование:
    python tools/code_analyzer.py --check-structure
    python tools/code_analyzer.py --check-pom
    python tools/code_analyzer.py --all
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class Colors:
    """Цвета для вывода в консоль (отключаются в CI)"""
    _use_colors = not os.environ.get("CI", "").lower() == "true"
    
    GREEN = '\033[92m' if _use_colors else ''
    RED = '\033[91m' if _use_colors else ''
    YELLOW = '\033[93m' if _use_colors else ''
    BLUE = '\033[94m' if _use_colors else ''
    BOLD = '\033[1m' if _use_colors else ''
    RESET = '\033[0m' if _use_colors else ''


class CodeAnalyzer:
    """Анализатор кода студенческого проекта"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.results: Dict = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "score": 0,
            "max_score": 100
        }
    
    def check_structure(self) -> bool:
        """Проверка обязательной структуры проекта"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}📁 Проверка структуры проекта{Colors.RESET}")
        print("=" * 60)
        
        required_structure = {
            "pages/": "Папка с Page Objects",
            "tests/": "Папка с тестами",
            "conftest.py": "Фикстуры pytest",
            "pytest.ini": "Конфигурация pytest",
            "requirements.txt": "Зависимости проекта"
        }
        
        required_files_in_pages = [
            "base_page.py",
            "login_page.py"
        ]
        
        required_files_in_tests = [
            "test_auth.py",
            "test_checkout.py"
        ]
        
        all_passed = True
        checks = []
        missing_items = []
        
        # Проверка основных папок и файлов
        for path, description in required_structure.items():
            full_path = self.project_path / path
            exists = full_path.exists()
            status = f"{Colors.GREEN}✓{Colors.RESET}" if exists else f"{Colors.RED}✗{Colors.RESET}"
            print(f"  {status} {description:35} [{path}]")
            checks.append({"name": path, "passed": exists, "description": description})
            if not exists:
                all_passed = False
                missing_items.append(path)
        
        # Проверка файлов в pages/
        pages_dir = self.project_path / "pages"
        if pages_dir.exists():
            print(f"\n  {Colors.BOLD}Файлы в pages/:{Colors.RESET}")
            for file in required_files_in_pages:
                full_path = pages_dir / file
                exists = full_path.exists()
                status = f"{Colors.GREEN}✓{Colors.RESET}" if exists else f"{Colors.RED}✗{Colors.RESET}"
                print(f"    {status} {file}")
                checks.append({"name": f"pages/{file}", "passed": exists})
                if not exists:
                    all_passed = False
                    missing_items.append(f"pages/{file}")
        
        # Проверка файлов в tests/
        tests_dir = self.project_path / "tests"
        if tests_dir.exists():
            print(f"\n  {Colors.BOLD}Файлы в tests/:{Colors.RESET}")
            for file in required_files_in_tests:
                full_path = tests_dir / file
                exists = full_path.exists()
                status = f"{Colors.GREEN}✓{Colors.RESET}" if exists else f"{Colors.RED}✗{Colors.RESET}"
                print(f"    {status} {file}")
                checks.append({"name": f"tests/{file}", "passed": exists})
                if not exists:
                    all_passed = False
                    missing_items.append(f"tests/{file}")
        
        # Подсчёт количества тест-файлов
        test_files_count = 0
        if tests_dir.exists():
            test_files = list(tests_dir.glob("test_*.py"))
            test_files_count = len(test_files)
            print(f"\n  {Colors.BOLD}Всего тест-файлов:{Colors.RESET} {test_files_count}")
            checks.append({"name": "test_files_count", "value": test_files_count})
            if test_files_count < 3:
                print(f"  {Colors.YELLOW}⚠ Рекомендуется минимум 3 тест-файла{Colors.RESET}")
                missing_items.append(f"Мало тест-файлов: {test_files_count} < 3")
        
        self.results["checks"]["structure"] = {
            "passed": all_passed,
            "details": checks,
            "missing": missing_items,
            "score": 10 if all_passed else 0
        }
        
        print("\n" + "=" * 60)
        if all_passed:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ Структура проекта корректна{Colors.RESET}")
            print("PASS")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Структура проекта требует доработки{Colors.RESET}")
            print(f"   Отсутствуют: {', '.join(missing_items)}")
            print("FAIL")
        
        return all_passed
    
    def check_pom(self) -> bool:
        """Проверка использования Page Object Pattern"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}🏗️  Проверка Page Object Pattern{Colors.RESET}")
        print("=" * 60)
        
        pages_dir = self.project_path / "pages"
        tests_dir = self.project_path / "tests"
        
        checks = []
        all_passed = True
        score = 0
        pom_classes_found = []
        missing_items = []
        
        # Проверка наличия классов Page
        if pages_dir.exists():
            for py_file in pages_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                content = py_file.read_text(encoding="utf-8")
                
                # Поиск классов с суффиксом Page
                classes = re.findall(r'class\s+(\w+Page)\s*\(', content)
                if classes:
                    pom_classes_found.extend(classes)
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Найден класс: {classes[0]} [{py_file.name}]")
                    checks.append({"file": py_file.name, "classes": classes, "passed": True})
                else:
                    checks.append({"file": py_file.name, "classes": [], "passed": False})
        
        if pom_classes_found:
            print(f"\n  {Colors.BOLD}Всего Page Object классов:{Colors.RESET} {len(pom_classes_found)}")
            score += 5
        else:
            print(f"  {Colors.RED}✗{Colors.RESET} Не найдены Page Object классы")
            all_passed = False
            missing_items.append("Page Object классы не найдены")
        
        # Проверка импортов в тестах
        pom_imports_found = False
        if tests_dir.exists():
            for test_file in tests_dir.glob("*.py"):
                content = test_file.read_text(encoding="utf-8")
                if "from pages" in content or "import pages" in content:
                    pom_imports_found = True
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Тест импортирует Page Objects [{test_file.name}]")
                    break
            
            if not pom_imports_found:
                print(f"  {Colors.RED}✗{Colors.RESET} Тесты не импортируют Page Objects")
                all_passed = False
                missing_items.append("Тесты не импортируют Page Objects")
            else:
                score += 5
        
        # Проверка наследования от базового класса
        base_page_found = False
        base_page_path = pages_dir / "base_page.py"
        if base_page_path.exists():
            content = base_page_path.read_text(encoding="utf-8")
            if "class BasePage" in content or "class Base" in content:
                base_page_found = True
                print(f"  {Colors.GREEN}✓{Colors.RESET} Найден базовый класс страницы")
                score += 3
            else:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} Базовый класс не найден (рекомендуется)")
        
        self.results["checks"]["pom"] = {
            "passed": all_passed,
            "classes_found": pom_classes_found,
            "imports_found": pom_imports_found,
            "base_page_found": base_page_found,
            "score": score,
            "details": checks,
            "missing": missing_items
        }
        
        print("\n" + "=" * 60)
        if all_passed:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ Page Object Pattern используется корректно{Colors.RESET}")
            print("PASS")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Page Object Pattern требует доработки{Colors.RESET}")
            print(f"   Проблемы: {', '.join(missing_items)}")
            print("FAIL")
        
        return all_passed
    
    def check_test_count(self) -> Dict:
        """Подсчёт количества тестов"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}📊 Подсчёт тестов{Colors.RESET}")
        print("=" * 60)
        
        tests_dir = self.project_path / "tests"
        test_count = 0
        test_names = []
        
        if tests_dir.exists():
            for test_file in tests_dir.glob("test_*.py"):
                content = test_file.read_text(encoding="utf-8")
                tests = re.findall(r'def\s+(test_\w+)\s*\(', content)
                test_count += len(tests)
                test_names.extend(tests)
                print(f"  📝 {test_file.name}: {len(tests)} тестов")
        
        print(f"\n  {Colors.BOLD}Всего тестов:{Colors.RESET} {test_count}")
        
        self.results["checks"]["test_count"] = {
            "total": test_count,
            "test_names": test_names
        }
        
        return {"total": test_count, "names": test_names}
    
    def get_score(self) -> int:
        """Подсчёт общего балла"""
        score = 0
        for check_name, check_data in self.results["checks"].items():
            if isinstance(check_data, dict) and "score" in check_data:
                score += check_data["score"]
        return score


def main():
    parser = argparse.ArgumentParser(
        description="Анализатор кода для GitHub Classroom",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
    python tools/code_analyzer.py --check-structure
    python tools/code_analyzer.py --check-pom
    python tools/code_analyzer.py --all
        """
    )
    
    parser.add_argument("--check-structure", action="store_true", 
                       help="Проверить структуру проекта")
    parser.add_argument("--check-pom", action="store_true",
                       help="Проверить Page Object Pattern")
    parser.add_argument("--test-count", action="store_true",
                       help="Подсчитать количество тестов")
    parser.add_argument("--all", action="store_true",
                       help="Запустить все проверки")
    parser.add_argument("--json", action="store_true",
                       help="Вывод результатов в JSON")
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    
    if args.all or (not args.check_structure and not args.check_pom and not args.test_count):
        args.check_structure = True
        args.check_pom = True
        args.test_count = True
    
    results = []
    
    if args.check_structure:
        results.append(analyzer.check_structure())
    
    if args.check_pom:
        results.append(analyzer.check_pom())
    
    if args.test_count:
        analyzer.check_test_count()
    
    # Итоговый вывод
    total_score = analyzer.get_score()
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}ИТОГОВЫЙ БАЛЛ: {total_score} / 100{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    
    if args.json:
        print(json.dumps(analyzer.results, ensure_ascii=False, indent=2))
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
