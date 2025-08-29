import pandas as pd
import joblib
from database.pull_data import get_new_data
from utils.config_helper import get_config
from utils.logger_helper import set_logger
from database.pull_data import db_conn
from datetime import datetime
import time

df = get_new_data()



config = get_config()

logger = set_logger(config["log_name"]["automated_loop_log"], config["log_paths"]["automated_loop_path"])

model = joblib.load(config["trained_models_filename"]["student_model"])

def get_new_rows():
  try:
    logger.info(f"strting the backgroup loop!!!")

    engine= db_conn()

    query = """
      select * from  `students performance dataset` s
      where s.Student_ID not in
      (select student_id  from student_grade_pred) 
          """

    df_new = pd.read_sql(query, con=engine)

    if df_new.empty:
      logger.info(f"No new rows founds!!")
      return 
    
    data = df_new.drop("Total_Score", axis=1, errors="ignore")

    prediction = model.predict(data)

    preds = pd.DataFrame({
      "student_id": df["Student_ID"],
      "total_score": prediction,
      "time": datetime.now()
    })

    preds.to_sql("student_grade_pred", con=engine, if_exists="append", index=False)
    logger.info(f"{len(df_new)} new rows were found!!")

  except Exception as e:
    logger.exception(e)



if __name__ == "__main__":
  while True:
    wait_time = config.get("wait_time", 60)

    logger.info(f"waiting for {wait_time} to get new rows!")

    start_time = datetime.now()

    logger.info(f"beggininig to get new rows at {start_time}")

    get_new_rows()

    logger.info(f"waiting for {wait_time}")

    time.sleep(60)


