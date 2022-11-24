import logging

DEBUG_LOG_FILE = "debug.log"
INFO_LOG_FILE = "info.log"

logger = logging.getLogger("root")


formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s')

logger.setLevel(logging.DEBUG)

stream_handler = logging.FileHandler(INFO_LOG_FILE, 'w+')
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(DEBUG_LOG_FILE, 'w+')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)