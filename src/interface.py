from src.headhunter_api import HeadHunterAPI
from src.vacancy_handler import VacancyHandler


def user_interaction():
    filtered_vacancies = []
    search_query = input("Введите поисковый запрос: ").strip()
    while True:
        try:
            min_salary = float(input("Введите минимальную зарплату: "))
            break
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")
    user_currency = input("Введите валюту, если рубли то введи RUR:").upper().strip()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies(search_query)
    sorted_vacancies = sorted(
        vacancies,
        key=lambda x: x['salary']['to'] if x.get('salary') and x['salary'].get('to') else float('-inf'),
        reverse=True
    )
    filtered_list = [i for i in sorted_vacancies if i.get('salary') and i['salary'].get('currency') == user_currency]

    for vacancy in filtered_list:
        salary_data = vacancy.get("salary",{})
        # print(salary_data)
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
        print(vac)



    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    #
    #
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)





# def salary_range():
#
#
#
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()