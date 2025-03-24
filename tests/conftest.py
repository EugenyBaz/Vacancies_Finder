import pytest
from src.vacancy_handler import VacancyHandler





@pytest.fixture
def vacancy_list():
  return VacancyHandler("Test Job", "http://example.com/job",
                                 {"from": 50000, "to": 80000}, "Requirements here")

@pytest.fixture
def vacancy_list_invalid_name():
  return ({'name':"",'vacancies_url':"http://example.com/job",
          'salary':{"from": 50000, "to": 80000}, 'requirement' :"Requirements here"})


@pytest.fixture
def vacancy_list_invalid_name_type():
  return {'name': 123,'vacancies_url':"http://example.com/job",
          'salary':{"from": 50000, "to": 80000}, 'requirement' :"Requirements here"}
