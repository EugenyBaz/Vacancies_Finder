import pytest
from src.vacancy_handler import VacancyHandler

# Тесты для инициализации и валидаторов

def test_valid_init(vacancy_list):

    assert vacancy_list.name == "Test Job"
    assert vacancy_list.vacancies_url == "http://example.com/job"
    assert vacancy_list.salary == " от 50000 до 80000"
    assert vacancy_list.requirement == "Requirements here"

def test_empty_string_values(vacancy_list_invalid_name):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_name)

    # with pytest.raises(ValueError):
    #     VacancyHandler("Test Job", "",
    #                    {"from": 50000, "to": 80000}, "Requirements here")

def test_invalid_types(vacancy_list_invalid_name_type):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_name_type)

    # with pytest.raises(ValueError):
    #     VacancyHandler("Test Job", 123,
    #                    {"from": 50000, "to": 80000}, "Requirements here")

def test_non_dict_salary(self):
    with pytest.raises(ValueError):
        VacancyHandler("Test Job", "http://example.com/job",
                       "string instead of dict", "Requirements here")

def test_salary_formats(self):
    handler = VacancyHandler("Test Job", "http://example.com/job",
                             50000, "Requirements here")
    assert handler.salary == "50000.00"
    handler = VacancyHandler("Test Job", "http://example.com/job",
                             "75000", "Requirements here")
    assert handler.salary == "75000.00"
    handler = VacancyHandler("Test Job", "http://example.com/job",
                             {"from": 50000, "to": 80000}, "Requirements here")
    assert handler.salary == " от 50000 до 80000"

def test_empty_requirements(self):
    handler = VacancyHandler("Test Job", "http://example.com/job",
                             {"from": 50000, "to": 80000}, "")
    assert handler.requirement == ""

# Тесты для метода __gt__
class TestSalaryComparison:
    def test_gt_salary_comparison(self):
        handler1 = VacancyHandler("Job A", "http://example.com/job1",
                                  {"from": 50000, "to": 80000})
        handler2 = VacancyHandler("Job B", "http://example.com/job2",
                                  {"from": 40000, "to": 60000})
        assert handler1 > handler2

    def test_salary_not_specified(self):
        handler1 = VacancyHandler("Job A", "http://example.com/job1",
                                  "Зарплата не указана")
        handler2 = VacancyHandler("Job B", "http://example.com/job2",
                                  {"from": 40000, "to": 60000})
        assert not handler1 > handler2

    def test_equal_salaries(self):
        handler1 = VacancyHandler("Job A", "http://example.com/job1",
                                  {"from": 50000, "to": 80000})
        handler2 = VacancyHandler("Job B", "http://example.com/job2",
                                  {"from": 50000, "to": 80000})
        assert not handler1 > handler2

    def test_unparseable_salary(self):
        handler1 = VacancyHandler("Job A", "http://example.com/job1",
                                  "Invalid salary format")
        handler2 = VacancyHandler("Job B", "http://example.com/job2",
                                  {"from": 40000, "to": 60000})
        assert not handler1 > handler2