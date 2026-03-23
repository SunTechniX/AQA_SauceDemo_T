#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check_structure.py
Проверка структуры проекта — вывод: PASS или FAIL
"""

import sys
from pathlib import Path

def main():
    required = {
        "pages/": "Папка с Page Objects",
        "tests/": "Папка с тестами",
        "conftest.py": "Фикстуры pytest",
        "pytest.ini": "Конфигурация pytest",
        "requirements.txt": "Зависимости проекта"
    }
    
    all_exist = True
    for path in required.keys():
        if not Path(path).exists():
            all_exist = False
    
    # Проверяем файлы в pages/
    pages_dir = Path("pages")
    if pages_dir.exists():
        if not (pages_dir / "base_page.py").exists():
            all_exist = False
        if not (pages_dir / "login_page.py").exists():
            all_exist = False
    
    # Проверяем файлы в tests/
    tests_dir = Path("tests")
    if tests_dir.exists():
        if not (tests_dir / "test_auth.py").exists():
            all_exist = False
        if not (tests_dir / "test_checkout.py").exists():
            all_exist = False
    
    # Выводим ТОЛЬКО PASS или FAIL (для bash-проверки)
    print("PASS" if all_exist else "FAIL")
    sys.exit(0)

if __name__ == "__main__":
    main()