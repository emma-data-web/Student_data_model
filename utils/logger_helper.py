import logging


from logging.handlers import TimedRotatingFileHandler


def set_logger(name, log_file, level=logging.DEBUG):
  logger = logging.getLogger(name)
  logger.setLevel(level)
  if not logger.hasHandlers():
    file_handler = TimedRotatingFileHandler(
      filename=log_file,
              when='midnight',     
              interval=1,          
              backupCount=7
    )

    file_handler.setLevel(level=logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(format)
    stream_handler.setFormatter(format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
  return logger