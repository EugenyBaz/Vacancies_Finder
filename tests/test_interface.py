import pytest
from src.file_saver import JSONSaver
from src.headhunter_api import HeadHunterAPI
from src.vacancy_handler import VacancyHandler
from src.interface import user_interaction
import os
import json

current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path = os.path.join(project_root, "data", "vacancy_data.json")

# Параметры для тестирования
@pytest.mark.parametrize(
    "search_query, min_salary, user_currency, factor_user, top_n, expected_results",
    [
        (
            "Python разработчик",     # Поисковый запрос
            80000,                   # Минимальная зарплата
            "RUR",                   # Валюта
            "опыт работы",           # Дополнительный параметр
            2,                       # Количество вакансий для вывода
            [                         # Ожидаемые результаты
                {
                    'name': 'Python Developer',
                    'url': 'https://example.com/job/12345',
                    'salary': {'from': 90000, 'to': 110000, 'currency': 'RUR'},
                    'requirements': 'Опыт работы от 3 лет'
                },
                {
                    'name': 'Senior Python Engineer',
                    'url': 'https://example.com/job/67890',
                    'salary': {'from': 95000, 'to': 120000, 'currency': 'RUR'},
                    'requirements': 'Опыт работы от 5 лет'
                }
            ]
        ),
        (
            "Java разработчик",       # Другой поисковый запрос
            70000,                   # Менее строгий фильтр по зарплате
            "USD",                   # Другая валюта
            "английский язык",       # Другой фактор
            2,                       # Количество вакансий для вывода
            [                         # Ожидаемый результат для другого набора фильтров
                {
                    'name': 'Java Developer',
                    'url': 'https://example.com/job/98765',
                    'salary': {'from': 75000, 'to': 85000, 'currency': 'USD'},
                    'requirements': 'Английский язык на уровне B2'
                },
                {
                    'name': 'Senior Java Engineer',
                    'url': 'https://example.com/job/54321',
                    'salary': {'from': 80000, 'to': 95000, 'currency': 'USD'},
                    'requirements': 'Английский язык на уровне C1'
                }
            ]
        )
    ]
)
def test_user_interaction(search_query, min_salary, user_currency, factor_user, top_n, expected_results):
    """
    Тестирует фильтрацию вакансий по различным параметрам.
    """


    # Генерация тестовых вакансий
    test_vacancies = user_interaction()  # Предположительно, эта функция генерирует список вакансий

    # Эмуляция API-запросов и сохранения данных
    with open(data_file_path, 'w') as file:
        json.dump(test_vacancies, file)

    # Загрузка сохраненных вакансий
    json_saver = JSONSaver(data_file_path)
    saved_vacancies = json_saver.load_data()

    # Имитация обработки запросов
    sorted_vacancies = sorted(
        saved_vacancies,
        key=lambda x: x['salary']['to'] if x.get('salary') and x['salary'].get('to') else float('-inf'),
        reverse=True
    )

    filtered_list = [i for i in sorted_vacancies if i.get('salary') and i['salary'].get('currency') == user_currency]

    filtered_word = json_saver.get_vacancy_factor(factor_user, filtered_list)

    # Фильтрация по минимальной зарплате
    filtered_vacancies = []
    for vacancy in filtered_word:
        salary_data = vacancy.get("salary", {})
        if not salary_data:
            continue
        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")

        if ((salary_from is not None and salary_to is not None and salary_from >= min_salary) or
                (salary_from is not None and salary_to is None and salary_from >= min_salary) or
                (salary_from is None and salary_to is not None and salary_to >= min_salary)):
            filtered_vacancies.append(
                VacancyHandler(
                    name=vacancy["name"],
                    vacancies_url=vacancy["alternate_url"],
                    salary=salary_data,
                    requirement=vacancy.get('snippet', {}).get("requirement", "")
                )
            )

    # Сравнение полученных результатов с ожидаемыми
    actual_results = [(vacancy.name, vacancy.vacancies_url, vacancy.salary, vacancy.requirement) for vacancy in filtered_vacancies][:top_n]

    assert len(actual_results) == len(expected_results), f"Количество вакансий не совпадает: {len(actual_results)} != {len(expected_results)}"
    for index, result in enumerate(actual_results):
        assert result[0] == expected_results[index]['name'], f"Название вакансии не совпадает: {result[0]} != {expected_results[index]['name']}"
        assert result[1] == expected_results[index]['url'], f"URL вакансии не совпадает: {result[1]} != {expected_results[index]['url']}"
        assert result[2] == expected_results[index]['salary'], f"Сведения о зарплате не совпадают: {result[2]} != {expected_results[index]['salary']}"
        assert result[3] == expected_results[index]['requirements'], f"Требования к вакансии не совпадают: {result[3]} != {expected_results[index]['requirements']}"
