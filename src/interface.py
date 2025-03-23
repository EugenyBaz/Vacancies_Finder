from src.file_saver import JSONSaver
from src.headhunter_api import HeadHunterAPI
from src.vacancy_handler import VacancyHandler
import os
current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path = os.path.join(project_root, "data", "vacancy_data.json")


def user_interaction():
    filtered_vacancies = []
    total_vacancy = []
    search_query = input("Введите поисковый запрос: ").strip()
    while True:
        try:
            min_salary = float(input("Введите минимальную зарплату: "))
            break
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")
    user_currency = input("Введите валюту, если рубли то введи RUR:").upper().strip()
    factor_user = input ("Введите параметр").strip()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies(search_query)
    json_handler = JSONSaver(filename=data_file_path)
    for v in vacancies:
        json_handler.add_vacancy(v)
    json_handler.save_data()


    sorted_vacancies = sorted(
        vacancies,
        key=lambda x: x['salary']['to'] if x.get('salary') and x['salary'].get('to') else float('-inf'),
        reverse=True
    )

    # filtered_list = [i for i in sorted_vacancies if i.get('salary') and i['salary'].get('currency') == user_currency]

    json_saver = JSONSaver()
    filtered_list = json_saver.get_vacancy_currency(user_currency, sorted_vacancies)

    filtered_word = json_saver.get_vacancy_factor(factor_user, filtered_list)


    for vacancy in filtered_word:
        salary_data = vacancy.get("salary",{})
        if not salary_data:
            continue
        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")

        if ((salary_from is not None and salary_to is not None and salary_from <= min_salary <= salary_to) or
                (salary_from is not None and salary_to is None and min_salary <= salary_from) or
                (salary_from is None and salary_to is not None and min_salary <= salary_to)):
            filtered_vacancies.append(
                        VacancyHandler(
                            name=vacancy["name"],
                            vacancies_url=vacancy["alternate_url"],
                            salary=salary_data,
                            requirement=vacancy.get('snippet', {}).get("requirement", "")
                        )
                    )

    vacancy_list = [(vacancy.name, vacancy.vacancies_url, vacancy.salary, vacancy.requirement) for vacancy in
                    filtered_vacancies]

    for vac in vacancy_list[:top_n]:
        total_vacancy.append(vac)
    return total_vacancy


