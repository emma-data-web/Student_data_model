import requests

url = "http://127.0.0.1:5000/predict"

datas = {
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
}

response = requests.post(url, json=datas)

print("Status code:", response.status_code)
print("Response text:", response.text)