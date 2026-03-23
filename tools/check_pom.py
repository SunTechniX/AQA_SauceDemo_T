#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check_pom.py
Проверка Page Object Pattern — вывод: PASS или FAIL
"""

import sys
import re
from pathlib import Path

def main():
    pages_dir = Path("pages")
    tests_dir = Path("tests")
    
    found_classes = False
    found_imports = False
    
    # Поиск классов Page
    if pages_dir.exists():
        for py_file in pages_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            content = py_file.read_text(encoding="utf-8")
            if re.search(r'class\s+\w+Page\s*\(', content):
                found_classes = True
                break
    
    # Проверка импортов в тестах
    if tests_dir.exists():
        for test_file in tests_dir.glob("*.py"):
            content = test_file.read_text(encoding="utf-8")
            if "from pages" in content or "import pages" in content:
                found_imports = True
                break
    
    # PASS если найдены и классы, и импорты
    passed = found_classes and found_imports
    print("PASS" if passed else "FAIL")
    sys.exit(0)

if __name__ == "__main__":
    main()