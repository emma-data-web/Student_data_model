from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
from utils.logger_helper import set_logger
from utils.config_helper import get_config

load_dotenv()

config = get_config()

logger = set_logger(config["log_paths"]["pull_data_path"],config["log_name"]["pull_data_log"])

print(logger)


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
    

