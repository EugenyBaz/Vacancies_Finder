import requests


class HeadHunterAPI:
    """Класс работы с API"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def get_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 2:
            response = requests.get(self.url, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies

hh_api = HeadHunterAPI()
hh_api.get_vacancies("python developer")
print(len(hh_api.vacancies))
print(hh_api.vacancies)