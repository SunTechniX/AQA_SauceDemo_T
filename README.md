# 🧪 Ваш проект SauceDemo Playwright

## 📋 Задание

Реализуйте автотесты для сайта [SauceDemo](https://www.saucedemo.com/) используя Playwright и Page Object Pattern.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# С зеркалом для РФ
pip install -r requirements.txt \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

# Установка браузеров
playwright install chromium
```

### 2. Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# Конкретный файл
pytest tests/test_auth.py -v

# С отчётом
pytest tests/ --html=output/reports/report.html

# Только smoke-тесты
pytest tests/ -m smoke -v
```

### 3. Проверка перед отправкой

```bash
# Проверка структуры
python ../tools/code_analyzer.py --all

# Линтинг
flake8 pages/ tests/ --config=../tools/flake8_config.cfg --show-source
```

## 📁 Структура проекта

```
student_template/
├── pages/           # Page Objects
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/           # Тесты
│   ├── test_auth.py
│   ├── test_cart.py
│   └── test_checkout.py
├── conftest.py      # Фикстуры
├── pytest.ini       # Конфиг pytest
└── output/          # Артефакты (скриншоты, отчёты)
```

## ✅ Критерии оценки

| Критерий | Баллы |
|----------|-------|
| Структура проекта | 10 |
| Линтинг (flake8) | 15 |
| Тесты авторизации | 25 |
| Тесты корзины | 25 |
| E2E тест | 25 |
| Page Object Pattern | 10 |
| **ИТОГО** | **110** |

### Шкала оценок

| Баллы | Оценка | Статус |
|-------|--------|--------|
| 90–110 | 🟢 Отлично | Зачтено |
| 70–89 | 🟡 Хорошо | Зачтено |
| 50–69 | 🟠 Удовлетворительно | Зачтено |
| <50 | 🔴 Требуется доработка | Не зачтено |

## 💡 Советы

1. Используйте `page.pause()` для отладки
2. Делайте частые коммиты — автопроверка запускается на каждый пуш
3. Смотрите Summary после каждого запуска — там подробный отчёт
4. Скриншоты при ошибках сохраняются в `output/screenshots/`
5. Изучите готовые Page Objects в `pages/` — они содержат полезные методы
