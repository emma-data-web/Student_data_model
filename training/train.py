import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
import joblib
from database.pull_data import get_new_data
from utils.config_helper import get_config
from utils.logger_helper import set_logger
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_squared_error, r2_score

config = get_config()

logger = set_logger(config["log_name"]["train_log"],config["log_paths"]["train_path"])


df = get_new_data()






def grade_trained_model(filename=config["trained_models_filename"]["student_model"]):
  try:
    logger.info(f"starting to train model!!!")
    caterogical_features = ["Gender","Department","Extracurricular_Activities","Internet_Access_at_Home","Parent_Education_Level","Family_Income_Level"]

    numerical_features = ['Age','Attendance (%)','Midterm_Score','Assignments_Avg','Quizzes_Avg','Participation_Score',
          'Projects_Score','Study_Hours_per_Week','Stress_Level (1-10)','Sleep_Hours_per_Night']

    features = ['Gender', 'Age',
          'Department', 'Attendance (%)', 'Midterm_Score',
          'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score',
          'Projects_Score', 'Study_Hours_per_Week',
          'Extracurricular_Activities', 'Internet_Access_at_Home',
          'Parent_Education_Level', 'Family_Income_Level', 'Stress_Level (1-10)',
          'Sleep_Hours_per_Night']
    
    for col in caterogical_features:
      df[col] = df[col].astype("category")

    target = 'Total_Score'


    logger.info(f"starting the process of training!")

    numerical_pipeline = Pipeline(steps=[
      ("num_impute", SimpleImputer(strategy="mean"))
    ])

    caterogical_pipeline = Pipeline(steps=[
      ("cat_impute", SimpleImputer(strategy="most_frequent")),
      ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))
    ])

    processed_features = ColumnTransformer(transformers=[
      ("numerical_features",numerical_pipeline,numerical_features),
      ("categorical_features",caterogical_pipeline,caterogical_features)
    ], verbose=True, remainder="drop")

    model = LGBMRegressor()

    final_pipeline = Pipeline(steps=[
      ("preprocesing",processed_features),
      ("model",model)
    ])

    param_dist = {
    'model__num_leaves': [31, 50, 100],       # controls complexity
    'model__max_depth': [-1, 5, 10],          # -1 means unlimited
    'model__learning_rate': [0.01, 0.05, 0.1],
    'model__n_estimators': [100, 500, 1000],  # number of boosting rounds
    'model__feature_fraction': [0.8, 0.9, 1.0],
    'model__bagging_fraction': [0.8, 1.0],
    'model__bagging_freq': [0, 5]             # 0 = no bagging
    }

    grid = RandomizedSearchCV(
      estimator=final_pipeline,
      param_distributions=param_dist,
      cv=4,
      scoring='neg_mean_squared_error',
      n_jobs=-1
    )

    x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.3, random_state=101)

    logger.info(f"returned a total of {len(x_train)} for x_train, {len(x_test)} for x_test,{len(y_train)} for y_train and {len(y_test)} for y_test")

    grid.fit(x_train, y_train)

    grade_model =grid.best_estimator_

    logger.info(f"the model best estimator = {grade_model}")

    y_pred = grade_model.predict(x_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    r2 = r2_score(y_test, y_pred)

    logger.info(f"Test RMSE: {rmse:.3f}")
    logger.info(f"Test R²: {r2:.3f}")

    joblib.dump(grade_model, filename)

  except Exception as e:
    logger.exception(e)
    return None



if __name__ == "__main__":
  grade_trained_model()
  
  