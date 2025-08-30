# logging.py
import logging
import getpass
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
	def format(self, record):
		user = getpass.getuser()
		record.user = user
		record.module_name = record.module
		record.func_name = record.funcName
		return super().format(record)

LOG_FORMAT = "%(asctime)s - %(user)s - [%(module_name)s] - [%(func_name)s] - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name=None):
	logger = logging.getLogger(name)
	if not logger.hasHandlers():
		# Create log directory if it doesn't exist
		log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		log_filename = datetime.now().strftime("%Y-%m-%d_Log")
		log_path = os.path.join(log_dir, log_filename)
		file_handler = logging.FileHandler(log_path, encoding="utf-8")
		file_handler.setFormatter(CustomFormatter(LOG_FORMAT, DATE_FORMAT))
		logger.addHandler(file_handler)
		logger.setLevel(logging.INFO)
	return logger
