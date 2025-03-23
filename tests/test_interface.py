import pytest
from unittest.mock import patch, Mock
from src.file_saver import JSONSaver
from src.headhunter_api import HeadHunterAPI
from src.vacancy_handler import VacancyHandler
import os

# Ваш исходный код
from src.interface import user_interaction

# Подмена функций для симуляции взаимодействия с пользователем
def mocked_input(prompt):
    inputs = ['search query', '50000', 'RUR', 'factor', '10']
    return inputs.pop(0)

# Подготовка тестовых данных
sample_vacancies = [
    {
        "name": "Test Vacancy 1",
        "alternate_url": "http://example.com/job1",
        "salary": {"from": 60000, "to": 70000, "currency": "RUR"},
        "snippet": {"requirement": "Test Requirement"}
    },
    {
        "name": "Test Vacancy 2",
        "alternate_url": "http://example.com/job2",
        "salary": {"from": 40000, "to": 50000, "currency": "USD"},
        "snippet": {"requirement": "Test Requirement"}
    },
    {
        "name": "Test Vacancy 3",
        "alternate_url": "http://example.com/job3",
        "salary": {"from": 30000, "to": 40000, "currency": "EUR"},
        "snippet": {"requirement": "Test Requirement"}
    }
]

# Определение фикстур
@pytest.fixture
def mock_input(monkeypatch):
    monkeypatch.setattr('builtins.input', mocked_input)

@pytest.fixture
def mock_hh_api():
    with patch('src.headhunter_api.HeadHunterAPI.get_vacancies', return_value=sample_vacancies) as mock:
        yield mock

@pytest.fixture
def mock_json_saver():
    with patch('src.file_saver.JSONSaver.add_vacancy'), \
         patch('src.file_saver.JSONSaver.save_data'):
        yield

# Класс для тестов

def test_user_interaction_flow(self, mock_input, mock_hh_api, mock_json_saver):
    result = user_interaction()

    # Проверка, что были вызваны нужные методы
    mock_hh_api.assert_called_once_with('search query')
    mock_json_saver.assert_has_calls([
        Mock().add_vacancy(sample_vacancies[0]),
        Mock().add_vacancy(sample_vacancies[1]),
        Mock().add_vacancy(sample_vacancies[2])
    ])

    # Проверка результата
    expected_result = [
        ('Test Vacancy 1', 'http://example.com/job1', {'from': 60000, 'to': 70000, 'currency': 'RUR'}, 'Test Requirement')
    ]
    assert result == expected_result

def test_no_vacancies_found(self, mock_input, mock_hh_api, mock_json_saver):
    mock_hh_api.return_value = []
    result = user_interaction()

    # Проверка, что результат пуст
    assert result == []

def test_error_in_vacancies(self, mock_input, mock_hh_api, mock_json_saver):
    mock_hh_api.return_value = [{"error": "Some error"}]
    result = user_interaction()

    # Проверка, что результатом является сообщение об ошибке
    assert result == [{'error': 'Some error'}]

