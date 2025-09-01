from database.pull_data import get_new_data
import pandas as pd
from database.pull_data import get_new_data
import pytest

@pytest.fixture
def data():
  data = get_new_data()
  return data.head(2)


def conn():
  connnection = 