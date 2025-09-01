from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from utils.logger_helper import set_logger
from database.pull_data import get_new_data
import joblib
from utils.config_helper import get_config

config = get_config()

logger = set_logger(config["log_name"]["API_log"], config["log_paths"]["API_path"])

model = joblib.load(config["trained_models_filename"]["student_model"])

app = Flask(__name__)

@app.route('/test', methods =['GET'])

def show():
   return 'server is running alright'


@app.route("/predict", methods= ["POST"])

def get_predictions():
    try:
      logger.info(f"starting to predict!!")
      data = request.get_json() 
      logger.info(f"{len(data)} keys recieved!")
      inputed_data =pd.DataFrame([data], columns=['Gender', 'Age',
          'Department', 'Attendance (%)', 'Midterm_Score',
          'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score',
          'Projects_Score', 'Study_Hours_per_Week',
          'Extracurricular_Activities', 'Internet_Access_at_Home',
          'Parent_Education_Level', 'Family_Income_Level', 'Stress_Level (1-10)',
          'Sleep_Hours_per_Night']) 
      predictions = model.predict(inputed_data)
      
      logger.info("predictions is ready!")
      
      prediction = np.array(predictions).tolist()
      
      return jsonify({'prediction': prediction[0]})
      
    except Exception as e:
       return jsonify({f"the error -- {e}"}), 400
    




if __name__ == "__main__":
    app.run(debug=True)