# Not my code - taken from https://gist.github.com/nguyenkims/e92df0f8bd49973f0c94bddf36ed7fd0
# after reading the article https://www.toptal.com/python/in-depth-python-logging

# TO USE:
# import log
# logger = log.get_logger("any_name")
# logger.debug("this is a debug message")
# logger.info("this is a debug message")

import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s %(name)s %(levelname)s : %(message)s")
LOG_FILE = "api.log"

def _get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

def _get_file_handler():
	file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
	file_handler.setFormatter(FORMATTER)
	return file_handler

def get_logger(logger_name : str) -> logging.Logger:
	logger = logging.getLogger(logger_name)

	logger.setLevel(logging.DEBUG) # better to have too much log than not enough

	logger.addHandler(_get_console_handler())
	logger.addHandler(_get_file_handler())

	# with this pattern, it's rarely necessary to propagate the error up to parent
	logger.propagate = False

	return logger