import joblib
import numpy as np
import pandas as pd
import pytest
from utils.config_helper import get_config

config = get_config()

@pytest.fixture
def get_model():
  model = joblib.load(config["trained_models_filename"]["student_model"])
  return model


@pytest.fixture
def datas():
    return pd.DataFrame([{
        "Gender": "Male",
        "Age": 21,
        "Department": "Engineering",
        "Attendance (%)": 85,
        "Midterm_Score": 72,
        "Assignments_Avg": 80,
        "Quizzes_Avg": 75,
        "Participation_Score": 60,
        "Projects_Score": 70,
        "Study_Hours_per_Week": 12,
        "Extracurricular_Activities": "Yes",
        "Internet_Access_at_Home": "Yes",
        "Parent_Education_Level": "College",
        "Family_Income_Level": "Medium",
        "Stress_Level (1-10)": 5,
        "Sleep_Hours_per_Night": 7
    }])


def test_model(get_model,datas):
  model = get_model
  data = datas
  predictions = model.predict(data)
  assert predictions is not None
  assert predictions[0] > 73
  assert isinstance(predictions,np.ndarray)



   