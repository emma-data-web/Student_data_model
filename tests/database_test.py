from database.pull_data import get_new_data
import pytest

@pytest.fixture
def data():
  yield df = get_new_data()