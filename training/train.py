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

logger = set_logger()

config = get_config

df = get_new_data

caterogical_features = ["Gender","Department","Extracurricular_Activities","Internet_Access_at_Home","Parent_Education_Level","Family_Income_Level"]

num = ['Student_ID','Age','Attendance (%)','Midterm_Score','Final_Score','Assignments_Avg','Quizzes_Avg','Participation_Score',
      'Projects_Score','Study_Hours_per_Week','Stress_Level (1-10)','Sleep_Hours_per_Night']