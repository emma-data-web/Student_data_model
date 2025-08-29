import pandas as pd
from database.pull_data import get_new_data
from utils.config_helper import get_config
from utils.logger_helper import set_logger

df = get_new_data()

config = get_config()

logger = set_logger(config["log_name"]["automated_loop_log"], config["log_paths"]["automated_loop_path"])