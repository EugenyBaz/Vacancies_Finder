from abc import ABC, abstractmethod
import json

class SAVER(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy_factor(self, factor):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass

class JSONSaver(SAVER):

    def __init__(self, filename='default.json'):
        self.__filename = filename
        self.data = {}
        self.load = ()

    def load_data(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.save_data()

    def save_data(self):
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}
        existing_data.update(self.data)
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4)


    def add_vacancy(self, vacancy):
        vacancy_id = vacancy.get('id')
        if vacancy_id not in self.data:
            self.data[vacancy_id] = vacancy
            self.save_data()

        else:
            print(f"Вакансия с id={vacancy_id} уже существует.")

    def get_vacancy_factor(self, factor):
        results = []
        for vacancy in self.data.values():
            if all(f in vacancy.items() for f in factor.items()):
                results.append(vacancy)
        return results

    def delete_vacancy(self, vacancy_id):
        if vacancy_id in self.data:
            del self.data[vacancy_id]
            self.save_data()
        else:
            print(f"Вакансия с id={vacancy_id} не найдена.")


