from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
from utils.logger_helper import set_logger

load_dotenv()

logger = set_logger("pull_logger","logs/logs.txt")


def get_new_data():
  try:
    logger.info("pulling data from the database")
    db_url = f"mysql+pymysql://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_database')}"

    engine = create_engine(db_url)
    query = ("select * from `students performance dataset`")

    df = pd.read_sql(query, con=engine)
    logger.info(f"sucessfully pulled {len(df)}")
    return df
  except Exception as e:
    logger.exception(e)
    

