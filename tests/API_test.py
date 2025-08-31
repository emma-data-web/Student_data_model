

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  



@pytest.fixture
def stacked_json():
    return {
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
        "Sleep_Hours_per_Night": 7,
    }


# ----------- TESTS -----------
def test_server_running():
    resp = requests.get(f"{BASE_URL}/test")
    assert resp.status_code == 200
    assert "server is running alright" in resp.text


def test_single_prediction(stacked_json):
    resp = requests.post(f"{BASE_URL}/predict", json=stacked_json)
    assert resp.status_code == 200
    json_data = resp.json()
    assert "prediction" in json_data
    assert isinstance(json_data["prediction"], (int, float))


def test_batch_prediction(stacked_json):
    batch_data = [stacked_json, stacked_json]  # 2 rows
    resp = requests.post(f"{BASE_URL}/predict", json=batch_data)
    assert resp.status_code == 200
    json_data = resp.json()
    assert "prediction" in json_data
    assert isinstance(json_data["prediction"], list)
    assert len(json_data["prediction"]) == 2


def test_invalid_request():
    bad_payload = {"wrong": "data"}
    resp = requests.post(f"{BASE_URL}/predict", json=bad_payload)
    assert resp.status_code == 400
