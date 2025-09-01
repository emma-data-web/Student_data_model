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

  assert len(test_data) == 2, "expects two rows from test_data"


def test_columns(data):

  test = data

  expected_columns = ['Student_ID', 'First_Name', 'Last_Name', 'Email', 'Gender', 'Age',
       'Department', 'Attendance (%)', 'Midterm_Score', 'Final_Score',
       'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score',
       'Projects_Score', 'Total_Score', 'Grade', 'Study_Hours_per_Week',
       'Extracurricular_Activities', 'Internet_Access_at_Home',
       'Parent_Education_Level', 'Family_Income_Level', 'Stress_Level (1-10)',
       'Sleep_Hours_per_Night']
  
  for col in test:
    assert col in expected_columns, f"{col} is missing if test fails"


def test_conn(conn):
  db_conn = conn

  assert db_conn is not None, "if none, database isnt connected" 

