from database.pull_data import get_new_data
import pandas as pd
from database.pull_data import db_conn
import pytest

@pytest.fixture
def data():
  data = get_new_data()
  return data.head(2)


@pytest.fixture
def conn():
  connnection = db_conn()
  return connnection


def test_database(data):
  test_data = data 

  assert len(test_data) == 2


def test_columns(data):

  test = data

  assert len(test.columns) > 10