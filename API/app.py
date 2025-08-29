from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from database.pull_data import get_new_data
import joblib
from utils.config_helper import get_config

config = get_config()

model = joblib.load(config["trained_models_filename"]["student_model"])

app = Flask(__name__)

@app.route('/test', methods =['GET'])

def show():
   return 'server is running, ada'


@app.route("/predict", methods= ["POST"])

def get_predictions():
    try:
      data = request.get_json()

      inputed_data =pd.DataFrame([data], columns=['Gender', 'Age',
          'Department', 'Attendance (%)', 'Midterm_Score',
          'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score',
          'Projects_Score', 'Study_Hours_per_Week',
          'Extracurricular_Activities', 'Internet_Access_at_Home',
          'Parent_Education_Level', 'Family_Income_Level', 'Stress_Level (1-10)',
          'Sleep_Hours_per_Night']) 
      predictions = model.predict(inputed_data)
      
      prediction = np.array(predictions).tolist()
      return jsonify({'prediction': prediction[0]})
    
    except Exception as e:
       return jsonify({f"the error -- {e}"}), 400
    




if __name__ == "__main__":
    app.run(debug=True)