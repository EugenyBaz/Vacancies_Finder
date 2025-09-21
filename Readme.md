# Название проекта
Программа, которая получает информацию о вакансиях с платформы hh.ru по
заданным параметрам.

## Содержание


## Технологии


## Использование


## Разработка
Реализовано взаимодействие с API
Предусмотрен метод __slots__, а так же методы сравнения вакансий по зарплате, валидации 
Реализованы методы работы с файлами (получение, сохранение)
Предусмотрен отдельный интерфейс взаимодействия с пользователем через консоль
По запрашиваемым параметрам выводит список вакансий.

### Требования


### Установка зависимостей
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

### Запуск Development сервера


### Создание билда

## Тестирование
Покрытие тестами на 70%

## Deploy и CI/CD


## Команда проекта

- [Евгений Базавод]  back-end developer

## Источники
