import pytest
import os
from src.file_saver import JSONSaver

# Фиктивная вакансия
VACANCY_1 = {"id": 1, "name": "Тестовая вакансия"}
VACANCY_2 = {"id": 2, "name": "Вторая вакансия"}
VACANCY_WITH_SALARY = {"id": 3, "name": "Третья вакансия", "salary": {"currency": "RUB"}}

# Путь к временному файлу данных
TEST_DATA_FILE_PATH = "temp_test_data.json"

# Фикстуры для временных данных
@pytest.fixture(scope="session")
def temp_data_file():
    """Создание временного файла данных"""
    yield TEST_DATA_FILE_PATH
    # Удаляем файл после завершения тестов
    os.remove(TEST_DATA_FILE_PATH)

@pytest.fixture
def saver(temp_data_file):
    """Создание экземпляра JSONSaver с временным файлом"""
    return JSONSaver(filename=temp_data_file)

# ТЕСТЫ

def test_add_vacancy(saver):
    """Тестирование добавления вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.save_data()

    # Загружаем сохранённые данные
    saver.load_data()
    assert VACANCY_1 in saver.data

def test_delete_vacancy(saver):
    """Тестирование удаления вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.delete_vacancy(1)

    # Проверяем, что вакансия была удалена
    saver.load_data()
    assert VACANCY_1 not in saver.data

def test_get_vacancy_factor(saver):
    """Тестирование поиска по фактору"""
    saver.add_vacancy(VACANCY_1)
    saver.add_vacancy({"id": 4, "name": "Четвертая вакансия", "area": "Москва"})

    # Поиск по фактору "Москва"
    result = saver.get_vacancy_factor("Москва")
    assert {"id": 4, "name": "Четвертая вакансия", "area": "Москва"} in result

def test_get_vacancy_currency(saver):
    """Тестирование поиска по валюте зарплаты"""
    saver.add_vacancy(VACANCY_WITH_SALARY)

    # Поиск вакансий с зарплатой в рублях
    result = saver.get_vacancy_currency("RUB")
    assert VACANCY_WITH_SALARY in result

def test_save_empty_data(saver):
    """Тестирование сохранения пустых данных"""
    saver.save_data()

    # Проверяем, что файл был создан
    assert os.path.exists(saver.filename)

def test_load_nonexistent_file(saver):
    """Тестирование загрузки несуществующего файла"""
    saver.load_data()
    assert saver.data == []

def test_duplicate_vacancy(saver):
    """Тестирование попытки добавления дублирующей вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.add_vacancy(VACANCY_1)

    # Проверяем, что добавлена только одна вакансия
    saver.load_data()
    assert len(saver.data) == 1