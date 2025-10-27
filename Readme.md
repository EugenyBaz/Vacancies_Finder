# Название проекта
Vacancies_Finder
Программа, которая получает информацию о вакансиях с платформы hh.ru по
заданным параметрам.

## Содержание

- [Технологии](#технологии)  
- [Разработка](#разработка)  
- [Требования](#требования)  
- [Установка зависимостей](#установка-зависимостей)  
- [Запуск Development сервера](#запуск-development-сервера)  
- [Тестирование](#тестирование)  
- [Deploy и CI/CD](#deploy-и-cicd)  
- [Команда проекта](#команда-проекта)  
- [Источники](#источники) 


## 🛠 Технологии

- Python 3.13  
- requests  
- pandas  
- openpyxl  
- python-dotenv  
- pytest  

Инструменты для разработки и линтинга: flake8, black, isort, mypy 


## ⚙ Разработка
- Взаимодействие с API hh.ru
- Используется метод __slots__ для оптимизации памяти
- Методы сравнения вакансий по зарплате и валидации данных
- Методы работы с файлами (получение, сохранение)
- По запрашиваемым параметрам выводит список вакансий.
- Консольный интерфейс для удобного взаимодействия

## 📋 Требования
-Python 3.13 или выше

## 📦 Установка зависимостей
[tool.poetry]
name = "vacancies-finder"
version = "0.1.0"
description = ""
authors = ["Bazavod <eugeny.bazavod@list.ru>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.13"
requests = "^2.32.3"
pandas = "^2.2.3"
openpyxl = "^3.1.5"
python-dotenv = "^1.0.1"
pytest = "^8.3.5"
pytest-cov = "^6.0.0"


[tool.poetry.group.lint.dependencies]
flake8 = "^7.1.2"
black = "^25.1.0"
isort = "^6.0.1"
mypy = "^1.15.0"


[tool.poetry.group.dev.dependencies]
coverage = "^7.6.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 119
exclude = '''(\.git)'''

[tool.isort]
line_length = 119

[tool.mypy]
disallow_untyped_defs = true
warn_return_any = true
exclude = 'venv'

## Запуск Development сервера
poetry run python main.py



## Тестирование
Покрытие тестами: 70%

Используем pytest и pytest -cov

## Deploy и CI/CD


## Команда проекта

- [Евгений Базавод]  back-end developer

## Источники
