import joblib
import pandas as pd
from utils.config_helper import get_config
from database.pull_data import get_new_data

config = get_config()
model = joblib.load(config["trained_models_filename"]["student_model"])

df = get_new_data()

def test_prediction(model, df):
   data = df.copy()
   
   new_data = data.drop(["Total_Score"], axis=1)
   predictions = model.predict(new_data)
   return predictions




if __name__ == "__main__":
   print(test_prediction(model,df))
   